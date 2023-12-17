from fastapi import FastAPI
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from router.product import product_router
from router.auth import auth_router

app = FastAPI()
app.title = "Market Zone"
app.version = "1.0.0"

app.add_middleware(ErrorHandler)
app.include_router(product_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)
