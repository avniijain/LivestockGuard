from app.main import app
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    import uvicorn

    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", 8000))

    uvicorn.run("main:app", host=host, port=port, reload=True)