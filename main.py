from fastapi import FastAPI
from database.database import Base, engine
from routes import user_routes, category_routes, product_routes, transaction_routes


Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(category_routes.router)
app.include_router(product_routes.router)
#app.include_router(transaction_routes.router)