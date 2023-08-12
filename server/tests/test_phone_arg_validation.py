import phone_arg_validation
import pytest


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

code_area_expected = [
    "11",
    None,
    "261",
    "351",
    "266",
    "343",
    "11",
    None,
    None,
    "343",
    "343",
    None
]
phone_number_expected = [
    "4444-0000",
    ValueError,
    "123-4567",
    "333-4444",
    "999-0000",
    "123-8888",
    "8888-4444",
    ValueError,
    ValueError,
    "999-0000",
    "699-0000",
    ValueError
]


@pytest.mark.parametrize("phone, expected",
                         zip(
                             inputs,
                             cleaned_inputs))
def test_obtain_phone_digits(phone, expected):
    assert phone_arg_validation.obtain_phone_digits(phone) == expected

@pytest.mark.parametrize("phone, expected",
                         zip(
                             cleaned_inputs,
                             code_area_expected))
def test_obtain_code_area(phone, expected):
    assert phone_arg_validation.obtain_code_area(phone) == expected

@pytest.mark.parametrize("phone, expected",
                         zip(
                             cleaned_inputs,
                             phone_number_expected))
def test_obtain_phone_number(phone, expected):
    if expected == ValueError:
        with pytest.raises(ValueError):
            phone_arg_validation.obtain_phone_number(phone)
    else:
        result = phone_arg_validation.obtain_phone_number(phone)
        assert result == expected