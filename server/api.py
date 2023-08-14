from fastapi import Depends, APIRouter, HTTPException, status, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
import os
from dotenv import load_dotenv
import mercadopago
from mercadopago.config import RequestOptions
from pydantic import ValidationError
from schema_validation import Checkout, OrderData, FormDataCliente
from preference_validation import Preferencia, Item, BackUrls, PaymentMethods, Payer, Phone, Address
from phone_arg_validation import obtain_phone_digits, obtain_code_area, obtain_phone_number
from address_validation import obtain_address, obtain_street_number
from deta import Deta
from datetime import datetime
import requests


router = APIRouter(
    prefix="/v1",
    tags=['Integration']
)


load_dotenv()

webhook_url = os.getenv("WEBHOOK_URL")
db_key = os.getenv("DB_ACCESS_KEY")

integrator_id = os.getenv("INTEGRATOR_ID")
access_token = os.getenv("ACCESS_TOKEN")
request_options = RequestOptions(
    integrator_id=integrator_id,
)
sdk = mercadopago.SDK(access_token, request_options=request_options)

deta = Deta(db_key)
db_1 = deta.Base("client_request")
db_2 = deta.Base("preferences_sent")
db_3 = deta.Base("preference_response")
db_4 = deta.Base("backurl_requests")
db_5 = deta.Base("payments_received")


url = 'https://api.mercadopago.com/v1/payments/{}'
headers = {
    'Authorization': f'Bearer {access_token}',
}


###  CREATE PREFERENCE  ###
@router.post("/create_preference")
async def create_preference(request: Checkout):

    timestamp = datetime.now()
    timestamp = timestamp.timestamp()

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
    body["timestamp"] = timestamp
    db_1.put(body)

    # PAYER PREFERENCE
    currency_id = "ARS"

    # Name, Surname, Email / Nombre, Apellido, Email
    name_list = client["nombre_apellido"].split(" ")
    if len(name_list) == 2:
        name, surname = name_list
        name, surname = name.title(), surname.title()
    else:
        surname = name_list.pop().title()
        name = " ".join(name_list).title()

    email = client["email"].lower()

    # Phone / Telefono
    variable = str(client["telefono"])
    phone = obtain_phone_digits(variable)
    code_area = obtain_code_area(phone)
    phone_number = obtain_phone_number(phone)

    phone = Phone(
        area_code=code_area,
        number=phone_number,
    )

    # Address / Direccion
    variable = client["direccion"]
    address = obtain_address(variable)
    street_number = obtain_street_number(variable)
    address = Address(
        zip_code=client["codigo_postal"],
        street_name=address,
        street_number=street_number,
    )

    payer = Payer(
        name=name,
        surname=surname,
        email=email,
        phone=phone.model_dump(),
        address=address.model_dump(),
        identification={"type": "", "number": ""},
    )

    # DEVELOPER PREFERENCE
    category_id = "phones"
    category_description = "Cell Phones & Accessories"
    back_urls = BackUrls(
        success="http://localhost:8000/v1/feedback",
        failure="http://localhost:8000/v1/feedback",
        pending="http://localhost:8000/v1/feedback"
    )
    auto_return = "all"
    notification_url = webhook_url
    statement_descriptor = "CERTIFICADO DEV"
    external_reference = "af.stigliano@gmail.com"

    # SELLER PREFERENCE
    item = Item(
        id=item["id"],
        title=item["description"],
        currency_id=currency_id,
        picture_url=item["img_url"],
        description=category_description,
        category_id=category_id,
        quantity=item["quantity"],
        unit_price=float(item["price"]),
    )

    payment_methods = PaymentMethods(
        excluded_payment_methods=[{"id": "visa"}],
        excluded_payment_types=[],
        installments=6
    )

    ###  VALIDACION PREFERENCE  ###
    preference = {
        "items": [item.model_dump()],
        "payer": payer.model_dump(),
        "back_urls": back_urls.model_dump(),
        "auto_return": auto_return,
        "payment_methods": payment_methods.model_dump(),
        "notification_url": notification_url,
        "statement_descriptor": statement_descriptor,
        "external_reference": external_reference,
    }

    try:
        preference = Preferencia(**preference)
    except ValidationError as e:
        print("Validation error:", e)
        return {"Validación fallida": e}

    ###  CREACION PREFERENCIA  ###
    json_preference = jsonable_encoder(preference)
    response = sdk.preference().create(json_preference)

    # CHECKPOINT 2
    db_2.put({"timestamp": timestamp, "preference": json_preference})
    db_3.put({"timestamp": timestamp, "response": response})

    if response["status"] == 201:
        return JSONResponse(content={"id": response["response"]["id"]})
    else:
        print(f"\tMercadoPago response error:{response}")
        return JSONResponse(content={"error": response["response"]})


# BACK_URLS
@router.get('/feedback')
async def feedback(request: Request, collection_id: str, collection_status: str, payment_id: str, status: str, external_reference: str, payment_type: str, merchant_order_id: str, preference_id: str, site_id: str, processing_mode: str, merchant_account_id: str):
    timestamp = datetime.now()
    timestamp = timestamp.timestamp()

    content = {
        "Collection": collection_id,
        "CollectionStatus": collection_status,
        "Payment": payment_id,
        "Status": status,
        "ExternalReference": external_reference,
        "Type": payment_type,
        "MerchantOrder": merchant_order_id,
        "Preference": preference_id,
        "Site": site_id,
        "ProcessingMode": processing_mode,
        "MerchantAccount": merchant_account_id
    }

    body = {
        "timestamp": timestamp,
        "content": content
    }

    db_4.put(body)

    response = requests.get(url.format(content["Payment"]), headers=headers)

    if response.status_code == 200:
        data = response.json()
        db_5.put({"id": content["Payment"],
                 "payment": data, "timestamp": timestamp})

    return JSONResponse(content=content)  # HTMLResponse(...)?
