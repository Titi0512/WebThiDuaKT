from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

from app.core.config import settings
from app.core.database import engine, Base
from app.api import auth, users, don_vi, danh_hieu, hinh_thuc, ho_so, thong_ke, export

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Hệ thống quản lý khen thưởng tại trường Sĩ quan Chính trị"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include API routers
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(don_vi.router, prefix="/api")
app.include_router(danh_hieu.router, prefix="/api")
app.include_router(hinh_thuc.router, prefix="/api")
app.include_router(ho_so.router, prefix="/api")
app.include_router(thong_ke.router, prefix="/api")
app.include_router(export.router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page."""
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard page."""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/ho-so", response_class=HTMLResponse)
async def ho_so_page(request: Request):
    """Hồ sơ list page."""
    return templates.TemplateResponse("ho_so_list.html", {"request": request})


@app.get("/don-vi", response_class=HTMLResponse)
async def don_vi_page(request: Request):
    """Đơn vị management page."""
    return templates.TemplateResponse("don_vi.html", {"request": request})


@app.get("/don-vi-chi-tiet", response_class=HTMLResponse)
async def don_vi_detail_page(request: Request):
    """Đơn vị detail page with sidebar menu."""
    return templates.TemplateResponse("don_vi_detail.html", {"request": request})


@app.get("/danh-muc", response_class=HTMLResponse)
async def danh_muc_page(request: Request):
    """Danh mục management page."""
    return templates.TemplateResponse("danh_muc.html", {"request": request})


@app.get("/thong-ke", response_class=HTMLResponse)
async def thong_ke_page(request: Request):
    """Thống kê page."""
    return templates.TemplateResponse("thong_ke.html", {"request": request})


@app.get("/users", response_class=HTMLResponse)
async def users_page(request: Request):
    """User management page (ADMIN only)."""
    return templates.TemplateResponse("users.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "app": settings.APP_NAME, "version": settings.APP_VERSION}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
