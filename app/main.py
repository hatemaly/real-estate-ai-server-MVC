# app/main.py
# This is the main entry point for the Real Estate AI server application.
# It initializes the FastAPI application, configures routers, sets up database
# connection events, and defines basic API endpoints.

from fastapi import FastAPI
from app.database.session import db_session
from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router
from app.routers.property_router import router as property_router
from app.routers.project_router import router as project_router
from app.routers.developer_router import router as developer_router
from app.routers.location_router import router as location_router
from app.routers.conversation_router import router as conversation_router

# Initialize the FastAPI application with metadata
app = FastAPI(
    title="AI-Powered Real Estate Brokerage API",
    description="API for managing real estate listings with AI features",
    version="1.0.0"
)

# Define event handlers for application lifecycle
@app.on_event("startup")
async def startup_event():
    """
    Event handler that runs when the application starts.
    
    This connects to the MongoDB database to ensure it's available
    when the application begins receiving requests.
    """
    await db_session.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """
    Event handler that runs when the application shuts down.
    
    This properly closes the MongoDB connection to ensure resources
    are released when the application terminates.
    """
    await db_session.disconnect()

# Include all routers with appropriate URL prefixes and tags
# NOTE: There appears to be duplicate inclusion of user_router (lines 30 and 33),
# which should be consolidated into a single inclusion.

# Auth router for authentication endpoints
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# Domain-specific routers for different entities in the system
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(property_router, prefix="/properties", tags=["Properties"])
app.include_router(project_router, prefix="/projects", tags=["Projects"])
app.include_router(developer_router, prefix="/developers", tags=["Developers"])
app.include_router(location_router, prefix="/locations", tags=["Locations"])
app.include_router(conversation_router, prefix="/conversations", tags=["Conversations"])

# Define basic API endpoints
@app.get("/")
async def root():
    """
    Root endpoint that serves as a simple health check.
    
    Returns:
        dict: A simple message indicating the API is running
    """
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    """
    Example endpoint with path parameter.
    
    This demonstrates how to use path parameters in FastAPI routes
    by greeting the user with their provided name.
    
    Args:
        name: The name to include in the greeting
        
    Returns:
        dict: A personalized greeting message
    """
    return {"message": f"Hello {name}"}
