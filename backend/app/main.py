from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.staticfiles import StaticFiles
from app.core.database.postgresql import create_tables
from app.core.security.create_admin_user import create_admin_user
from app.core.seed.seed_data import seed_all_data
from app.utils.exception import http_exception_handler
from contextlib import asynccontextmanager
from app.controllers import auth_controller,user_controller,category_controller,product_controller,size_controller
from pathlib import Path


@asynccontextmanager
async def lifespan(app: FastAPI):
    upload_dir = Path("uploads/products")
    upload_dir.mkdir(parents=True, exist_ok=True)
    await create_tables()
    await create_admin_user()
    await seed_all_data()
    yield


app = FastAPI(
    title="Simple Storage Api",
    description="Simple Storage Api",
    version="0.1.0",
    lifespan=lifespan
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_exception_handler(HTTPException, http_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_controller.router, prefix="/api/v1")
app.include_router(user_controller.router, prefix="/api/v1")
app.include_router(category_controller.router, prefix="/api/v1")
app.include_router(product_controller.router, prefix="/api/v1")
app.include_router(size_controller.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"Hello": "World"}