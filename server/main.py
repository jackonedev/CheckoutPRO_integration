from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import api



app = FastAPI()

#  STATIC FILES
app.mount("/assets", StaticFiles(directory="./frontend/assets"), name="assets")
app.mount("/img", StaticFiles(directory="./frontend/img"), name="img")


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api.router)

@app.get("/")
async def read_root():
##  Devolver el archivo HTML principal de React
    return FileResponse("./frontend/index.html")