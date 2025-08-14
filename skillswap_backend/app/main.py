from fastapi import FastAPI
from .routes import test_route
from .auth import auth_routes
from .skills import skills_routes

app = FastAPI(title="Skillswap API")

app.include_router(test_route.router)
app.include_router(auth_routes.router)
app.include_router(skills_routes.router)

@app.get("/")
def get_root():
    return {"message":"welcome to our skillswap api"}