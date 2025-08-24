import pytest
import allure
from http import HTTPStatus
from data.data_generator import random_email, random_password


@allure.title("Регистрация без email")
def test_register_without_email(api_client):
    response = api_client.register_user(email=None, password="Valid123!", age=25)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Регистрация без пароля")
def test_register_without_password(api_client):
    response = api_client.register_user(email=random_email(), password=None, age=25)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Регистрация без возраста")
def test_register_without_age(api_client):
    response = api_client.register_user(email=random_email(), password="Valid123!", age=None)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Регистрация с email без @")
def test_register_invalid_email_no_at(api_client):
    response = api_client.register_user(email="invalidemail.ru", password="Valid123!", age=30)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Регистрация с email без точки")
def test_register_invalid_email_no_dot(api_client):
    response = api_client.register_user(email="invalid@email", password="Valid123!", age=30)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Регистрация с email длиной 51 символ")
def test_register_email_too_long(api_client):
    local_part = "a" * (51 - len("@mail.ru"))
    email = f"{local_part}@mail.ru"
    response = api_client.register_user(email=email, password="Valid123!", age=20)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Регистрация с email длиной 1 символ")
def test_register_email_too_short(api_client):
    response = api_client.register_user(email="a", password="Valid123!", age=25)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Регистрация с паролем короче 5 символов")
def test_register_short_password(api_client):
    response = api_client.register_user(email=random_email(), password="1234", age=20)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Регистрация с паролем длиннее 20 символов")
def test_register_long_password(api_client):
    response = api_client.register_user(email=random_email(), password="a" * 21, age=20)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("age", [-1, 100])
@allure.title("Регистрация с невалидным возрастом (меньше 0 или больше 99)")
def test_register_invalid_age_range(api_client, age):
    response = api_client.register_user(email=random_email(), password="Valid123!", age=age)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Регистрация с возрастом, содержащим буквы")
def test_register_age_with_letters(api_client):
    response = api_client.session.post(
        f"{api_client.base_url}/auth/register",
        json={"email": random_email(), "password": "Valid123!", "age": "abc"}
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Регистрация с возрастом в формате float (10.5)")
def test_register_age_with_float(api_client):
    response = api_client.session.post(
        f"{api_client.base_url}/auth/register",
        json={"email": random_email(), "password": "Valid123!", "age": 10.5}
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Регистрация уже существующего пользователя")
def test_register_existing_user(api_client, new_user):
    response = api_client.register_user(
        new_user["email"], new_user["password"], new_user["age"]
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
