from fastapi import Depends, APIRouter, HTTPException, status, Request
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List
import os
from dotenv import load_dotenv
import mercadopago
from mercadopago.config import RequestOptions
from schema_validation import Checkout, OrderData, FormDataCliente


router = APIRouter(
    prefix="/v1",
    tags=['Integration']
)


load_dotenv()

integrator_id = os.getenv("INTEGRATOR_ID")
access_token = os.getenv("ACCESS_TOKEN")
request_options = RequestOptions(
    integrator_id=integrator_id,
)
sdk = mercadopago.SDK(access_token, request_options=request_options)


# CRETE PREFERENCE
@router.post("/create_preference")
async def create_preference(request: Checkout):

    body = request.model_dump()

    try:
        item = body.get("orderData")
        item = OrderData(**item).model_dump()
    except:
        return JSONResponse(content={"error": "orderData is required"})

    try:
        client = body.get("formDataCliente")
        client = FormDataCliente(**client).model_dump()
    except:
        return JSONResponse(content={"error": "formDataCliente is required"})

    with open("request.json", "w") as f:
        f.write(str(body))

    preference = {
        "items": [
            {
                "title": item["description"],
                "unit_price": float(item["price"]),
                "quantity": int(item["quantity"]),
            }
        ],
        "back_urls": {
            "success": "http://localhost:8000/feedback",
            "failure": "http://localhost:8000/feedback",
            "pending": "http://localhost:8000/feedback"
        },
        "auto_return": "all",
    }

    response = sdk.preference().create(preference)
    if response["status"] == 201:
        with open("response.json", "w") as f:
            f.write(str(response))
        return JSONResponse(content={"id": response["response"]["id"]})
    else:
        print(f"\tMercadoPago response error:{response}")
        return JSONResponse(content={"error": response["response"]})



# BACK_URLS
@router.get('/feedback')
async def feedback(request: Request, collection_id: str, collection_status: str, payment_id: str, status: str, external_reference: str, payment_type: str, merchant_order_id: str, preference_id: str, site_id: str, processing_mode: str, merchant_account_id: str):
    # print(f"request: {request}") -> <starlette.requests.Request object at 0x000002057C96AA90>
    return JSONResponse(content={
        "Payment": payment_id,
        "Status": status,
        "MerchantOrder": merchant_order_id
    })


# WEBHOOKS - AUTO-GENERATED
@router.post('/webhooks')
async def webhooks(request: Request):
    data = await request.json()
    with open("webhooks.json", "w") as f:
        f.write(str(data))
    payment_id = data["data"]["id"]
    payment = sdk.payment().get(payment_id)
    if payment["status"] == 200:
        with open("payment.json", "w") as f:
            f.write(str(payment))
        return JSONResponse(content={"Payment": payment})
    else:
        print(f"\tMercadoPago response error:{payment}")
        return JSONResponse(content={"error": payment["response"]})