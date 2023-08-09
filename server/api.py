from fastapi import Depends, APIRouter, HTTPException, status, Request
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List
import os
from dotenv import load_dotenv
import mercadopago
from mercadopago.config import RequestOptions
from schema_validation import Checkout, OrderData, FormDataCliente
from preference_validation import Preference
from pydantic import ValidationError

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
        item = OrderData(**item)
    except ValidationError as e:
        print("Validation error:", e)
        return JSONResponse(content={"error": e})

    try:
        client = body.get("formDataCliente")
        client = FormDataCliente(**client)
    except ValidationError as e:
        print("Validation error:", e)
        return JSONResponse(content={"error": e})        

    item = item.model_dump()
    client = client.model_dump()

    # CHECKPOINT 1
    if not os.path.exists("logs"):
        os.makedirs("logs")
    with open("./logs/01_client_request.json", "w") as f:
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


    ## aca va a haber error

    try:
        preference = Preference(**preference)
    except ValidationError as e:
        print("Validation error:", e)



    # CHECKPOINT 2
    with open("./logs/02_preference.json", "w") as f:
        f.write(str(preference.model_dump()))

    response = sdk.preference().create(preference)

    if response["status"] == 201:
        # CHECKPOINT 3
        with open("./logs/03_mp_response.json", "w") as f:
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