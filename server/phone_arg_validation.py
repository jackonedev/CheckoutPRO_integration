from enum import Enum
import re
from typing import Union


code_area_wiki = {"CABA": "11",
                  "Provincia de Córdoba I": "351",
                  "Provincia de Córdoba II": "3543",
                  "Provincia de Corrientes": "379",
                  "Provincia de Formosa": "370",
                  "Provincia de Buenos Aires": "221",
                  "Provincia de La Rioja": "380",
                  "Provincia de Mendoza": "261",
                  "Provincia del Neuquén": "299",
                  "Provincia de Entre Ríos": "343",
                  "Provincia de Misiones": "376",
                  "Provincia del Chubut": "2804",
                  "Provincia del Chaco": "362",
                  "Provincia de Santa Cruz": "2966",
                  "Provincia de Salta": "387",
                  "Provincia de Catamarca": "383",
                  "Provincia de San Juan": "264",
                  "Provincia de San Luis": "266",
                  "Provincia de Tucumán": "381",
                  "Provincia de Jujuy": "388",
                  "Provincia de Santa Fe": "342",
                  "Provincia de La Pampa": "2954",
                  "Provincia de Santiago del Estero": "385",
                  "Provincia de Río Negro": "2920",
                  "Provincia de Tierra del Fuego, Antártida e Islas del Atlántico Sur": "2901"}


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


inputs = [
    "+54 11 4444-0000 ",
    "+54 341 1118888 ",
    "(+549261)1234567 ",
    "(0351)333-4444 ",
    "266 - 999 - 0000 ",
    "343-1238888 ",
    "+5491188884444 ",
    "543412228888 ",
    "(54)233-15-111-2222 ",
    "(+54-343)9990000 ",
    "+54 (3436) 99-0000 ",
    "(0)8003337333 ",
]

cleaned_inputs = [
    "1144440000",
    "3411118888",
    "2611234567",
    "3513334444",
    "2669990000",
    "3431238888",
    "1188884444",
    "3412228888",
    "2331112222",
    "3439990000",
    "3436990000",
    "8003337333",
]


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
        print("La variable comienza con uno de los valores de CodeArea")
        code_area = next(code.value for code in CodeArea if phone.startswith(code.value))
        print(code_area)
        return code_area
    else:
        print("La variable no comienza con ninguno de los valores de CodeArea")
        



def obtain_phone_number(phone: str) -> Union[str, None]:
    """Verify if phone starts with any code area from Argentina """
    code_area = obtain_code_area(phone)
    if code_area:
        number = phone[len(code_area):]
        if len(code_area) + len(number) != 10:
            raise ValueError("El número de teléfono no tiene 10 dígitos")       
        number = number[:-4] + "-" + number[-4:]
        return number
        

