import time

import pytest

import config
from registration_page_object import RegistrationPageObject

LOCATOR_WAIT_TIMEOUT = 3000  # ms, таймаут ожидания появления локатора на странице
USERNAME_VALIDATE_MESSAGE_STANDARD = " Допустимые символы (от 6 до 32): a-z, 0-9, _. Имя должно начинаться с буквы "
USERNAME_VALIDATE_MESSAGE_BUSY = " Имя пользователя уже занято "
USERNAME_VALIDATE_MESSAGE_SYMBOLS = " Введены недопустимые символы: "
VALIDATE_MESSAGE_EMPTY = " Поле не заполнено "

EMAIL_VALIDATE_STANDARD = " Формат e-mail: username@test.ru "

PASS_CLICK_VALIDATE_TO_SHORT = " Пароль должен содержать минимум 8 символов "
PASS_CLICK_VALIDATE_STANDARD = " Пароль должен содержать от 8 до 64 символов, включая заглавные буквы и цифры "
PASS_KEYPRESS_VALIDATE_TO_SHORT = " Сложность пароля: слишком короткий "
PASS_KEYPRESS_VALIDATE_TO_EASY = " Сложность пароля: низкая "
PASS_KEYPRESS_VALIDATE_MIDDLE = " Сложность пароля: средняя "
PASS_KEYPRESS_VALIDATE_ABOVE_AVERAGE = " Сложность пароля: выше среднего "
PASS_KEYPRESS_VALIDATE_HIGH = " Сложность пароля: высокая "

REFERRAL_CODE_VALIDATE = " Неверный формат ссылки "


@pytest.mark.parametrize("username, validate_string", [
    ("", VALIDATE_MESSAGE_EMPTY),  # проверка на пустое поле
    ("1aaaaaa", USERNAME_VALIDATE_MESSAGE_STANDARD),  # Проверка на начало с буквы
    ("a" * 5, USERNAME_VALIDATE_MESSAGE_STANDARD),  # проверка на количество символов минимум
    ("a" * 33, USERNAME_VALIDATE_MESSAGE_STANDARD),  # проверка на количество символов максимум
    ("a" * 6, USERNAME_VALIDATE_MESSAGE_BUSY),  # имя занято
], ids=["empty value", "not letter first", "over min chars length", "over max chars length", "name is already used"])
def test_username_validate_click(browser, username, validate_string):
    page = RegistrationPageObject(browser, config.URL)
    page.username.set(username)
    page.username.click()
    page.next_button_click()
    if username != "":
        assert page.username.get_text_on_page(validate_string), f"Не дождались элемент с текстом {validate_string}"
    validate_text = page.username.validate_text()
    assert validate_text == validate_string, f"Для имени пользователя {username} ожидаемый текст ошщибки валидации {validate_string}, получен - {validate_text}"


@pytest.mark.parametrize("username, validate_string", [
    ('!@#$%^&*()_-+=', USERNAME_VALIDATE_MESSAGE_SYMBOLS + '!@#$%^&amp;*()-+= '),  # Проверка на спецсимволы, "_" не должно быть в списке - разрешен
    ('пользователь', USERNAME_VALIDATE_MESSAGE_SYMBOLS + 'пользвате '),  # ппроверка на кирилицу и повторяющиеся символы
], ids=["special characters", "cyrillic & repeated characters"])
def test_username_validate_no_click(browser, username, validate_string):
    page = RegistrationPageObject(browser, config.URL)
    page.username.set(username)
    validate_text = page.username.validate_text()
    assert validate_text == validate_string, f"Для имени пользователя {username} ожидаемый текст ошщибки валидации {validate_string}, получен - {validate_text}"


@pytest.mark.parametrize("email, validate_string", [
    ('', VALIDATE_MESSAGE_EMPTY),  # Проверка на пустое значение
    ('test', EMAIL_VALIDATE_STANDARD),  # Проверка без @
    ('a' * 1000, EMAIL_VALIDATE_STANDARD),  # Проверка валидации на большое число символов
    ('test@123.123', EMAIL_VALIDATE_STANDARD),  # Проверка с не корректным корневым доменом
], ids=["empty value", "no @ in e-mail", "long line 1000 symbols", "invalid root domain"])
def test_email_validate(browser, email, validate_string):
    page = RegistrationPageObject(browser, config.URL)
    page.email.set(email)
    page.next_button_click()
    assert page.email.get_text_on_page(validate_string), f"Не дождались элемент с текстом {validate_string}"
    validate_text = page.email.validate_text()
    assert validate_text == validate_string, f"Для почты {email} ожидаемый текст ошщибки валидации {validate_string}, получен - {validate_text}"


@pytest.mark.parametrize("password, validate_string", [
    ('', VALIDATE_MESSAGE_EMPTY),  # Проверка на пустое значение
    ('1' * 7, PASS_CLICK_VALIDATE_TO_SHORT),  # Проверка короткого пароля
    ('a' * 65, PASS_CLICK_VALIDATE_STANDARD),  # Проверка длинного пароля
    ('A1234567', PASS_CLICK_VALIDATE_STANDARD),  # Проверка без строчной буквы
    ('a1234567', PASS_CLICK_VALIDATE_STANDARD),  # Проверка без заглавной буквы
    ('a' * 8, PASS_CLICK_VALIDATE_STANDARD),  # Проверка без цифр

], ids=["empty value", "too short password", "too long password",
        "without a lowercase letter", "without a uppercase letter",
        "without numbers"])
def test_password_click_validate(browser, password, validate_string):
    page = RegistrationPageObject(browser, config.URL)
    page.password.set(password)
    page.next_button_click()
    assert page.password.get_text_on_page(validate_string), f"Не дождались элемент с текстом {validate_string}"
    validate_text = page.password.validate_text()
    assert validate_text == validate_string, f"Для пароля {password} ожидаемый текст ошщибки валидации {validate_string}, получен - {validate_text}"


@pytest.mark.parametrize("password, validate_string", [
    ('1' * 7, PASS_KEYPRESS_VALIDATE_TO_SHORT),  # Проверка короткого пароля
    ('A1234567', PASS_KEYPRESS_VALIDATE_TO_EASY),  # Проверка низкой сложности пароля
    ('1234567890Aa', PASS_KEYPRESS_VALIDATE_MIDDLE),  # Проверка средней сложности пароля
    ('1234567890Aa!', PASS_KEYPRESS_VALIDATE_ABOVE_AVERAGE),  # Проверка выше средней сложности пароля
    ('1234567890Aa!23', PASS_KEYPRESS_VALIDATE_HIGH),  # Проверка высокой сложности пароля
], ids=["too short password", "low password complexity", "middle password complexity",
        "higher middle password complexity", "high password complexity"])
def test_password_keypress_validate(browser, password, validate_string):
    page = RegistrationPageObject(browser, config.URL)
    page.password.set(password)
    assert page.password.get_text_on_page(validate_string), f"Не дождались элемент с текстом {validate_string}"
    validate_text = page.password.get_validate_keypress_text()
    assert validate_text == validate_string, f"Для пароля {password} ожидаемый текст ошщибки валидации {validate_string}, получен - {validate_text}"


@pytest.mark.parametrize("referral_code, validate_string", [
    ('1', REFERRAL_CODE_VALIDATE),  # Проверка короткого кода
    ('!";', REFERRAL_CODE_VALIDATE),  # Проверка спецсимволов
], ids=["too short code", "special characters"])
def test_referral_code_validate(browser, referral_code, validate_string):
    page = RegistrationPageObject(browser, config.URL)
    page.referral_code.set(referral_code)
    validate_text = page.referral_code.validate_text()
    assert validate_text == validate_string, f"Для реферального кода {referral_code} ожидаемый текст ошщибки валидации {validate_string}, получен - {validate_text}"
    page.referral_code.set("")  # очищаем поле, чтобы не блокировалась кнопка "Далее"


def test_agreement_checkbox(browser):  # проверка выделениея красным чекбокса соглащения , если он не отмечен
    page = RegistrationPageObject(browser, config.URL)
    page.next_button_click()
    result = page.get_agreement_checkbox_error_state()
    assert result
