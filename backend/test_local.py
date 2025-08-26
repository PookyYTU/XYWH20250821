import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run application
if __name__ == "__main__":
    print("Starting XYWH backend service (local test)...")
    
    try:
        # Test configuration loading
        from app.config import settings
        print(f"Config loaded successfully - Database: {settings.db_host}:{settings.db_port}/{settings.db_name}")
        
        # Test database connection
        from app.database import test_connection
        if test_connection():
            print("Database connection successful")
        else:
            print("Database connection failed")
            sys.exit(1)
        
        # Start server
        import uvicorn
        from main import app
        
        print("Starting development server...")
        print("Local address: http://127.0.0.1:8000")
        print("API docs: http://127.0.0.1:8000/docs")
        print("Health check: http://127.0.0.1:8000/api/health")
        print("=" * 50)
        
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except Exception as e:
        print(f"Startup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)