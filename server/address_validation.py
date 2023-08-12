import re


def obtain_street_number(address):
    return re.sub(r"\D", "", address)


def obtain_address(address):
    address = re.sub(r"\d", "", address)
    return address.rstrip()
