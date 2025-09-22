from fastapi import FastAPI

from app.routers import auth, user, romancist, book, health

app = FastAPI(title="MADR API")

app.include_router(user.router)	
app.include_router(auth.router)
app.include_router(health.router)

@app.get('/')
def home():
    """Root endpoint."""
    return {"message": "welcome to My Digital Collection of Novels"}



    