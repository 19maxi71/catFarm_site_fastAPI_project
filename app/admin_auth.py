from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from .auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, verify_token

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/admin/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Serve the login page."""
    return templates.TemplateResponse("admin_login.html", {"request": request})


@router.post("/admin/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    """Handle login form submission."""
    user = authenticate_user(username, password)
    if not user:
        return templates.TemplateResponse(
            "admin_login.html",
            {"request": request, "error": "Invalid username or password"}
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )

    # Set token in session (simple approach - in production use proper session management)
    response = RedirectResponse(url="/admin", status_code=302)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return response


@router.post("/admin/logout")
async def logout():
    """Handle logout."""
    response = RedirectResponse(url="/admin/login", status_code=302)
    response.delete_cookie(key="access_token")
    return response


@router.get("/admin/protected")
async def protected_route(current_user: dict = Depends(verify_token)):
    """Example protected route."""
    return {"message": f"Hello {current_user.username}!"}
