from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import api



app = FastAPI()

#  STATIC FILES
# app.mount("/static", StaticFiles(directory="./frontend/static"), name="static")
# app.mount("/img", StaticFiles(directory="./frontend/static/img"), name="img")


# CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}
#     # Devolver el archivo HTML principal de React
#     return FileResponse("./frontend/index.html")