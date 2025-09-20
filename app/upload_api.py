from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import json

from .photo_utils import save_uploaded_photo, get_image_info

router = APIRouter()


@router.post("/upload/photo")
async def upload_photo(
    file: UploadFile = File(...),
    cat_name: Optional[str] = Form(None),
    article_image: Optional[str] = Form(None)
):
    """
    Upload and process a photo (cat or article).
    Returns the file paths for storage in database.
    """
    try:
        # Determine the naming prefix based on type
        name_prefix = f"article_{cat_name}" if article_image == "true" else cat_name

        # Process and save the photo
        full_path, thumb_path = await save_uploaded_photo(file, name_prefix, article_image == "true")

        # Get image info
        image_info = get_image_info(full_path)

        return JSONResponse(content={
            "success": True,
            "message": "Photo uploaded successfully",
            "data": {
                "full_image": full_path,
                "thumbnail": thumb_path,
                "original_filename": file.filename,
                "image_info": image_info
            }
        })

    except HTTPException as e:
        return JSONResponse(
            content={"success": False, "message": e.detail},
            status_code=e.status_code
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"Upload failed: {str(e)}"},
            status_code=500
        )


@router.post("/upload/multiple")
async def upload_multiple_photos(files: list[UploadFile] = File(...)):
    """
    Upload multiple photos at once.
    """
    results = []
    errors = []

    for i, file in enumerate(files):
        try:
            full_path, thumb_path = await save_uploaded_photo(file)
            results.append({
                "index": i,
                "filename": file.filename,
                "full_image": full_path,
                "thumbnail": thumb_path
            })
        except Exception as e:
            errors.append({
                "index": i,
                "filename": file.filename,
                "error": str(e)
            })

    return JSONResponse(content={
        "success": len(results) > 0,
        "message": f"Uploaded {len(results)} photos, {len(errors)} failed",
        "data": {
            "successful": results,
            "failed": errors
        }
    })


@router.delete("/upload/cleanup")
async def cleanup_temp_files():
    """
    Clean up temporary files (for maintenance).
    """
    try:
        from .photo_utils import cleanup_old_temp_files
        cleanup_old_temp_files()
        return JSONResponse(content={
            "success": True,
            "message": "Temporary files cleaned up"
        })
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)},
            status_code=500
        )
