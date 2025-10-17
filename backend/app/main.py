from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.db.mongodb import Database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await Database.connect_to_database()
    yield
    # Shutdown
    await Database.close_database_connection()

app = FastAPI(
    title="RFP Contract Management System",
    description="API for managing RFP contracts",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "API is running"}

# Import and include routers
from app.api.endpoints import users, rfps, documents, notifications

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(rfps.router, prefix="/api/rfps", tags=["rfps"])
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred", "detail": str(exc)},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
