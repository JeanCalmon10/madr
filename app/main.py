from fastapi import FastAPI

from app.routers import auth, user, romancist, book, health

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MADR API")

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost', 
        'http://localhost:5173', 
        'http://127.0.0.1:5173'
    ],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)	
app.include_router(auth.router)
app.include_router(health.router)
app.include_router(romancist.router)
app.include_router(book.router)

@app.get('/')
def home():
    """Root endpoint."""
    return {"message": "welcome to My Digital Collection of Novels"}



    