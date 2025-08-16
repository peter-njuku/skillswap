from fastapi import FastAPI
from .auth import auth_routes
from .skills import skills_routes
from .chat import chat_routers
from .notifications import notification_routers
from .matching import matching_routes

app = FastAPI(title="Skillswap API")

app.include_router(auth_routes.router)
app.include_router(skills_routes.router)
app.include_router(chat_routers.router)
app.include_router(notification_routers.router)
app.include_router(matching_routes.router)

@app.get("/")
def get_root():
    return {"message":"welcome to our skillswap api"}