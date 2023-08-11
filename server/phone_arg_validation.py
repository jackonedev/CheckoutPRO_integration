import re


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

expected = [
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

    # first clean up
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

    # first length validation
    if len(phone) == 10:
        print("return: Valid number of phone digits")

    if phone[:2] == "11" and phone[2:4] == "15":  # case 11 15 12345678
        phone = phone[:2] + phone[4:]
        if len(phone) == 10:
            print("return: Valid number of phone digits")

    if phone[:-7].endswith("15"):  # caso 351 15 1234567
        phone = phone[:3] + phone[5:]
        if len(phone) == 10:
            print("return: Valid number of phone digits")

    if phone[:-6].endswith("15"):  # caso 3543 15 123456
        phone = phone[:4] + phone[6:]
        if len(phone) == 10:
            print("return: Valid number of phone digits")

    return phone
