from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import clone

app = FastAPI(
    title="Website Cloner API",
    description="API for cloning websites using LLM",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(clone.router, prefix="/api", tags=["clone"])


@app.get("/")
def read_root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
