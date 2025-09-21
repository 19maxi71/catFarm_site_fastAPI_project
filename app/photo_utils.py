import os
import uuid
import aiofiles
import base64
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageOps
from fastapi import UploadFile, HTTPException
from typing import Tuple
from io import BytesIO

# Configuration
UPLOAD_DIR = Path("static/uploads")
CATS_DIR = UPLOAD_DIR / "cats"
ARTICLES_DIR = UPLOAD_DIR / "articles"
THUMBNAILS_DIR = UPLOAD_DIR / "thumbnails"
TEMP_DIR = UPLOAD_DIR / "temp"

# Ensure directories exist
CATS_DIR.mkdir(parents=True, exist_ok=True)
ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
THUMBNAILS_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Image settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
THUMBNAIL_SIZE = (300, 300)
FULL_SIZE = (1200, 1200)


async def save_uploaded_photo(file: UploadFile, cat_name: str = None, article_image: bool = False) -> Tuple[str, str]:
    """
    Save uploaded photo with compression and create thumbnail.
    Returns: (full_image_path, thumbnail_path)
    """
    # Validate file type
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, detail=f"File type {file_ext} not allowed")

    # Validate file size
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400, detail="File too large (max 10MB)")

    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]

    if article_image:
        base_name = f"article_{timestamp}_{unique_id}"
        target_dir = ARTICLES_DIR
    else:
        base_name = f"{cat_name}_{timestamp}_{unique_id}" if cat_name else f"cat_{timestamp}_{unique_id}"
        target_dir = CATS_DIR

    # Save original file temporarily
    temp_path = TEMP_DIR / f"{base_name}_original{file_ext}"
    async with aiofiles.open(temp_path, 'wb') as f:
        await f.write(file_content)

    try:
        # Process and optimize image
        full_path, thumb_path = await process_image(temp_path, base_name, file_ext, target_dir)

        # Clean up temp file
        temp_path.unlink(missing_ok=True)

        # Return relative paths for database storage
        return str(full_path.relative_to("static")), str(thumb_path.relative_to("static"))

    except Exception as e:
        # Clean up on error
        temp_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=500, detail=f"Error processing image: {str(e)}")


async def process_image(temp_path: Path, base_name: str, file_ext: str, target_dir: Path = CATS_DIR) -> Tuple[Path, Path]:
    """Process image: compress, resize, and create thumbnail."""
    try:
        # Open image
        with Image.open(temp_path) as img:
            # Auto-rotate based on EXIF orientation data
            img = ImageOps.exif_transpose(img)

            # Convert to RGB if necessary (for PNG with transparency)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()
                                 [-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Create full-size optimized image
            full_path = target_dir / f"{base_name}_full.jpg"
            img_resized = resize_image(img, FULL_SIZE)
            img_resized.save(full_path, 'JPEG', quality=85, optimize=True)

            # Create thumbnail
            thumb_path = THUMBNAILS_DIR / f"{base_name}_thumb.jpg"
            img.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
            img.save(thumb_path, 'JPEG', quality=80, optimize=True)

            return full_path, thumb_path

    except Exception as e:
        raise Exception(f"Image processing failed: {str(e)}")


def resize_image(img: Image.Image, max_size: Tuple[int, int]) -> Image.Image:
    """Resize image maintaining aspect ratio."""
    img_ratio = img.width / img.height
    max_ratio = max_size[0] / max_size[1]

    if img_ratio > max_ratio:
        # Image is wider than max ratio
        new_width = max_size[0]
        new_height = int(max_size[0] / img_ratio)
    else:
        # Image is taller than max ratio
        new_height = max_size[1]
        new_width = int(max_size[1] * img_ratio)

    # Only resize if image is larger than max_size
    if img.width > max_size[0] or img.height > max_size[1]:
        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    return img


def get_image_info(image_path: str) -> dict:
    """Get image metadata."""
    try:
        full_path = Path("static") / image_path
        with Image.open(full_path) as img:
            return {
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "size_bytes": full_path.stat().st_size
            }
    except Exception:
        return {}


def cleanup_old_temp_files():
    """Clean up temporary files older than 1 hour."""
    import time
    current_time = time.time()

    for temp_file in TEMP_DIR.glob("*"):
        if temp_file.is_file():
            file_age = current_time - temp_file.stat().st_mtime
            if file_age > 3600:  # 1 hour
                temp_file.unlink()


async def convert_image_to_base64(file: UploadFile, max_width: int = 800, max_height: int = 600) -> str:
    """
    Convert uploaded image to base64 with compression for database storage.
    Returns base64 encoded string with data URL prefix.
    """
    # Validate file type
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, detail=f"File type {file_ext} not allowed")

    # Validate file size
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400, detail="File too large (max 10MB)")

    try:
        # Open and process the image
        with Image.open(BytesIO(file_content)) as img:
            # Apply EXIF orientation correction
            img = ImageOps.exif_transpose(img)

            # Convert to RGB if necessary (for JPEG compatibility)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # Resize if too large (to keep database storage reasonable)
            if img.width > max_width or img.height > max_height:
                img.thumbnail((max_width, max_height),
                              Image.Resampling.LANCZOS)

            # Save as JPEG with compression
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=85, optimize=True)
            buffer.seek(0)

            # Convert to base64
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            # Return with data URL prefix
            return f"data:image/jpeg;base64,{img_base64}"

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing image: {str(e)}")


def base64_to_data_url(base64_string: str) -> str:
    """
    Ensure base64 string has proper data URL format.
    """
    if base64_string and not base64_string.startswith('data:'):
        return f"data:image/jpeg;base64,{base64_string}"
    return base64_string or ""
