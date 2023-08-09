from typing import List, Dict, Optional
from pydantic import BaseModel, HttpUrl
from datetime import datetime, timedelta


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
    area_code: str  # 0351 | 351  Considerar eliminar 0 al comienzo
    number: str  # admite un '-'


class Identification(BaseModel):
    type: str = "DNI"
    number: str  # considerar la eliminación de puntos


class Address(BaseModel):
    street_name: str
    street_number: int
    zip_code: str


class Payer(BaseModel):
    name: str
    surname: str
    email: str
    phone: Phone
    identification: Identification
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


class Preferencia(BaseModel):
    items: List[Item]
    payer: Payer
    back_urls: BackUrls
    auto_return: str = "all"
    payment_methods: PaymentMethods
    notification_url: HttpUrl
    statement_descriptor: Optional[str] # Nombre del emisor de la factura
    external_reference: str
    expires: bool = True
    expiration_date_from: datetime = datetime.now()
    expiration_date_to: datetime = datetime.now() + timedelta(days=15)
