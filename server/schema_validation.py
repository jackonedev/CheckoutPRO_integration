from pydantic import BaseModel, ConfigDict, EmailStr, conint, constr, HttpUrl
from typing import Optional
from datetime import datetime


class Checkout(BaseModel):
    orderData: dict
    formDataCliente: dict

class OrderData(BaseModel):
    id: str
    quantity: int
    price: str
    amount: int
    description: str
    img_url: HttpUrl
    name: str

class FormDataCliente(BaseModel):
    nombre_apellido: str
    email: EmailStr
    telefono: str
    direccion: str
    codigo_postal: int