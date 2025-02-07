from fastapi import FastAPI
from app.database.session import db_session
from app.routers import auth_router
from app.routers.conversation_router import router as conversation_router
from app.routers.user_router import router as user_router
from app.routers.property_router import router as property_router
from app.routers.project_router import router as project_router
from app.routers.developer_router import router as developer_router
from app.routers.location_router import router as location_router

app = FastAPI(
    title="AI-Powered Real Estate Brokerage API",
    description="API for managing real estate listings with AI features",
    version="1.0.0"
)

# Include event handlers
@app.on_event("startup")
async def startup_event():
    await db_session.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await db_session.disconnect()



app.include_router(auth_router.router)
# Include routers
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(property_router, prefix="/properties", tags=["Properties"])
app.include_router(project_router, prefix="/projects", tags=["Projects"])
app.include_router(developer_router, prefix="/developers", tags=["Developers"])
app.include_router(location_router, prefix="/locations", tags=["Locations"])

app.include_router(conversation_router, prefix="/conversations", tags=["Conversations"])

# Add endpoints
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
