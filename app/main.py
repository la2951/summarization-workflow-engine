from fastapi import FastAPI

# Create the FastAPI application instance
app = FastAPI(title="Simple Workflow Engine", version="0.1.0")


@app.get("/")
def read_root():
    """
    Basic health check endpoint.
    This will help us confirm that the server is running.
    """
    return {"message": "Workflow engine API is up!"}
