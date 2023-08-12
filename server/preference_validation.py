from typing import List, Dict, Optional
from pydantic import BaseModel, HttpUrl
from datetime import datetime, timedelta

ahora = datetime.now()
expiracion_pagos_efectivo = ahora + timedelta(days=5)
expiracion_preferencia = ahora + timedelta(days=15)

class Item(BaseModel):
    id: str = "item-ID-1234"
    title: str
    currency_id: str = "ARS"
    picture_url: HttpUrl
    description: str
    category_id: str
    quantity: int
    unit_price: float


class Phone(BaseModel):
    area_code: str
    number: str


class Identification(BaseModel):
    type: str = "DNI"
    number: str


class Address(BaseModel):
    street_name: str
    street_number: int
    zip_code: str


class Payer(BaseModel):
    name: str
    surname: str
    email: str
    phone: Phone
    identification: Optional[Identification]
    address: Address


class BackUrls(BaseModel):
    success: HttpUrl
    failure: HttpUrl
    pending: HttpUrl


class PaymentMethod(BaseModel):
    id: str


class PaymentType(BaseModel):
    id: str


class PaymentMethods(BaseModel):
    excluded_payment_methods: List[PaymentMethod]
    excluded_payment_types: List[PaymentType]
    installments: int = 12


class Shipment(BaseModel):
    cost: int
    mode: str = "not_specified"


class Preferencia(BaseModel):
    items: List[Item]
    payer: Payer
    back_urls: BackUrls
    auto_return: str = "all"
    payment_methods: PaymentMethods
    notification_url: HttpUrl
    statement_descriptor: Optional[str] = "abc"  # Nombre del emisor de la factura
    external_reference: str
    date_of_expiration: str = str(expiracion_pagos_efectivo)
    expires: bool = True
    expiration_date_from: str = str(ahora)
    expiration_date_to: str = str(expiracion_preferencia)
    # shipment_cost: Optional[Shipment]
