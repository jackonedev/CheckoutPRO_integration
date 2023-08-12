import phone_arg_validation

import pytest


@pytest.mark.parametrize("phone, expected",
                         zip(
                             phone_arg_validation.inputs,
                             phone_arg_validation.cleaned_inputs))
def test_obtain_phone_digits(phone, expected):
    assert phone_arg_validation.obtain_phone_digits(phone) == expected
