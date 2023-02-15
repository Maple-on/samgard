from fastapi import FastAPI
from database.database import Base, engine
from routes import user_routes, category_routes, product_routes, transaction_routes
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(engine)

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router)
app.include_router(category_routes.router)
app.include_router(product_routes.router)
# app.include_router(transaction_routes.router)
