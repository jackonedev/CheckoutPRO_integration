from enum import Enum
import re
from typing import Union




class CodeArea(Enum):
    CABA = "11"
    PROV_CORDOBA_I = "351"
    PROV_CORDOBA_II = "3543"
    PROV_CORRIENTES = "379"
    PROV_FORMOSA = "370"
    PROV_BUENOS_AIRES = "221"
    PROV_LA_RIOJA = "380"
    PROV_MENDOZA = "261"
    PROV_NEUQUEN = "299"
    PROV_ENTRE_RIOS = "343"
    PROV_MISIONES = "376"
    PROV_CHUBUT = "2804"
    PROV_CHACO = "362"
    PROV_SANTA_CRUZ = "2966"
    PROV_SALTA = "387"
    PROV_CATAMARCA = "383"
    PROV_SAN_JUAN = "264"
    PROV_SAN_LUIS = "266"
    PROV_TUCUMAN = "381"
    PROV_JUJUY = "388"
    PROV_SANTA_FE = "342"
    PROV_LA_PAMPA = "2954"
    PROV_SANTIAGO_DEL_ESTERO = "385"
    PROV_RIO_NEGRO = "2920"
    PROV_TIERRA_DEL_FUEGO = "2901"




def obtain_phone_digits(phone):
    """This function removes all non-digits from the phone number
    And returns the phone number with only 10 digits
    """

    # Remove all non-digits
    phone = re.sub(r"\D", "", phone)

    if phone[:4] == "0054":
        phone = phone[4:]

    if phone[:3] == "054":
        phone = phone[3:]

    if phone[:2] == "54":
        phone = phone[2:]

    if phone[:1] == "9":
        phone = phone[1:]

    if phone[:1] == "0":
        phone = phone[1:]

    if phone[:2] == "11" and phone[2:4] == "15":  # case 11 15 12345678
        phone = phone[:2] + phone[4:]

    if phone[:-7].endswith("15"):  # caso 351 15 1234567
        phone = phone[:3] + phone[5:]

    if phone[:-6].endswith("15"):  # caso 3543 15 123456
        phone = phone[:4] + phone[6:]

    if len(phone) == 10:
        return phone


def obtain_code_area(phone: str) -> Union[str, None]:
    """Verify if phone starts with any code area from Argentina """

    if any(phone.startswith(code.value) for code in CodeArea):
        code_area = next(
            code.value for code in CodeArea if phone.startswith(code.value))
        return code_area


def obtain_phone_number(phone: str) -> Union[str, None]:
    """Verify if phone starts with any code area from Argentina """
    code_area = obtain_code_area(phone)
    if code_area:
        number = phone[len(code_area):]
        if len(code_area) + len(number) != 10:
            raise ValueError("El número de teléfono no tiene 10 dígitos")
        number = number[:-4] + "-" + number[-4:]
        return number
    else:
        raise ValueError(
            "El número de teléfono no comienza con un código de área válido")

