import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import core components
from .core.config import settings
from .core.logging_config import get_logger
from .core.error_handling import register_exception_handlers

# Initialize main application logger
logger = get_logger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    description="Secure document validation application for Credit Unions",
    version="1.0.0",
    debug=settings.DEBUG,
)

# Mount static files directory
static_dir = os.path.join(os.path.dirname(__file__), 'static')
if os.path.exists(static_dir) and os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    logger.info(f"Using static directory at {static_dir}")
else:
    logger.warning(f"Static directory not found at {static_dir}. Create it if you need to serve static files.")

# Configure Jinja2 templates
templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
if os.path.exists(templates_dir) and os.path.isdir(templates_dir):
    templates = Jinja2Templates(directory=templates_dir)
    logger.info(f"Using templates directory at {templates_dir}")
else:
    templates = None
    logger.warning(f"Templates directory not found at {templates_dir}. Create it if you need to use Jinja2 templates.")

# Import and include routers
from .api import routes as api_routes
from .frontend import routes as frontend_routes

# Include routers
app.include_router(api_routes.router, prefix="/api", tags=["api"])
app.include_router(frontend_routes.router, tags=["frontend"])

# Register custom exception handlers
register_exception_handlers(app)

# Add root endpoint (optional)
@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to the Secure Document Validation Application!"}

# Startup and Shutdown Events
@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION} ({settings.APP_ENV})")
    # Add any startup tasks here (database connections, etc.)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.APP_NAME}")
    # Add any cleanup tasks here