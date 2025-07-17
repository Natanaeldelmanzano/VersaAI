import sys
import os

# Add current directory to Python path
sys.path.insert(0, '.')

# Import and run the server
from src.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)