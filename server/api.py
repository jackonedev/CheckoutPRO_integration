from fastapi import Depends, APIRouter, HTTPException, status, Request
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List
import os
from dotenv import load_dotenv
import mercadopago
from mercadopago.config import RequestOptions
from schema_validation import Checkout, OrderData, FormDataCliente
from preference_validation import Preferencia, Item, BackUrls, PaymentMethods, Payer
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
        return {"error": e}

    try:
        client = body.get("formDataCliente")
        client = FormDataCliente(**client)
    except ValidationError as e:
        print("Validation error:", e)
        return {"error": e}

    item = item.model_dump()
    client = client.model_dump()

    # CHECKPOINT 1
    if not os.path.exists("logs"):
        os.makedirs("logs")
    with open("./logs/01_client_request.json", "w") as f:
        f.write(str(body))

    # client preference
    currency_id = "ARS"

    name_list = client["nombre_apellido"].split(" ")
    if len(name_list) == 2:
        name, surname = name_list
        name, surname = name.title(), surname.title()
    else:
        surname = name_list.pop().title()
        name = " ".join(name_list).title()

    email = client["email"].lower()


    #### VALIDACION DEL TELEFONO
    phone = str(client["telefono"])
    if phone.startswith("0"):
        phone = phone[1:]
    #TODO: sacando los prefijos la longitud debe ser de 10, si comienza con 11, el numero es de longitud 8  




    payer = Payer(
        name=name,
        surname=surname,
        email=email,

    )


    # developer preference
    category_id = "telephones"
    back_urls = BackUrls(
        success="http://localhost:8000/feedback",
        failure="http://localhost:8000/feedback",
        pending="http://localhost:8000/feedback"
    )
    auto_return = "all"
    notification_url = "http://localhost:8000/v1/webhooks"
    # statement_descriptor = "CERTIFICADODEV"
    external_reference = "af.stigliano@gmail.com"

    # seller preference
    item = Item(
        id=item["id"],
        title=item["title"],
        currency_id=currency_id,
        picture_url=item["img_url"],
        description=item["description"],
        category_id=category_id,
        quantity=item["quantity"],
        unit_price=float(item["price"]),
        )
    
    payment_methods = PaymentMethods(
        excluded_payment_methods=[{"id": "visa"}],
        excluded_payment_types=[],
        installments=6
    )

    preference = {
        "items": [item.model_dump()],
        "back_urls": back_urls.model_dump(),
        "auto_return": auto_return,
        "payment_methods": payment_methods.model_dump(),
        "notification_url": notification_url,
        "external_reference": external_reference,



    }


    ## aca va a haber error

    try:
        preference = Preferencia(**preference)
    except ValidationError as e:
        print("Validation error:", e)



    # CHECKPOINT 2
    with open("./logs/02_preference.json", "w") as f:
        f.write(str(preference.model_dump()))

    # response = sdk.preference().create(preference)

    # if response["status"] == 201:
    #     # CHECKPOINT 3
    #     with open("./logs/03_mp_response.json", "w") as f:
    #         f.write(str(response))
    #     return JSONResponse(content={"id": response["response"]["id"]})
    # else:
    #     print(f"\tMercadoPago response error:{response}")
    #     return JSONResponse(content={"error": response["response"]})



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