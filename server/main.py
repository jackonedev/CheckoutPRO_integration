from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import mercadopago
from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI()

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


# PATH OPERATION FUNCTIONS
@app.post("/create_preference")
async def create_preference(request: Request):
    body = await request.json()

    # # creating SDK instance
    # access_token = request.headers["Authorization"].split(" ")[1]
    access_token = os.getenv("ACCESS_TOKEN")
    sdk = mercadopago.SDK(access_token)

    preference = {
        "items": [
            {
                "title": body["description"],
                "unit_price": float(body["price"]),
                "quantity": int(body["quantity"]),
            }
        ],
        "back_urls": {
            "success": "http://localhost:8000/feedback",
            "failure": "http://localhost:8000/feedback",
            "pending": "http://localhost:8000/feedback"
        },
        "auto_return": "approved",
    }
    response = sdk.preference().create(preference)
    if response["status"] == 201:
        return JSONResponse(content={"id": response["response"]["id"]})
    else:
        print(f"\tMercadoPago response error:{response}")
        return JSONResponse(content={"error": response["response"]})


@app.get('/feedback')
async def feedback(request: Request, collection_id: str, collection_status: str, payment_id: str, status: str, external_reference: str, payment_type: str, merchant_order_id: str, preference_id: str, site_id: str, processing_mode: str, merchant_account_id: str):
    # print(f"request: {request}") -> <starlette.requests.Request object at 0x000002057C96AA90>
    return JSONResponse(content={
        "Payment": payment_id,
        "Status": status,
        "MerchantOrder": merchant_order_id
    })
