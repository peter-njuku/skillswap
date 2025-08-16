from fastapi import FastAPI
from .auth import auth_routes
from .skills import skills_routes
from .chat import chat_routers

app = FastAPI(title="Skillswap API")

app.include_router(auth_routes.router)
app.include_router(skills_routes.router)
app.include_router(chat_routers.router)

@app.get("/")
def get_root():
    return {"message":"welcome to our skillswap api"}