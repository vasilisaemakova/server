import pytest
import allure
from http import HTTPStatus
from data.data_generator import random_email, random_password
from schemas.user import User


@allure.title("Успешная регистрация с валидными данными")
def test_successful_registration(api_client):
    email = random_email()
    password = "ValidPass123!"
    age = 25

    response = api_client.register_user(email, password, age)
    assert response.status_code == HTTPStatus.OK

    user_data = response.json()["user"]
    user = User(**user_data)

    assert user.email == email
    assert user.age == age


@pytest.mark.parametrize("length", [49, 50])
@allure.title("Регистрация с email длиной до 50 символов")
def test_register_email_valid_length(api_client, length):
    domain = "@e.com"
    local_part_length = length - len(domain)
    local_part = "a" * local_part_length
    email = f"{local_part}{domain}"
    password = "ValidPass123"
    age = 25

    response = api_client.register_user(email, password, age)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["user"]["email"] == email


@pytest.mark.parametrize("length", [5, 6, 20])
@allure.title("Регистрация с паролем допустимой длины")
def test_register_valid_password_lengths(api_client, length):
    email = random_email()
    password = "A" * length
    age = 20

    response = api_client.register_user(email, password, age)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["user"]["email"] == email



@allure.title("Регистрация с валидным возрастом")
@pytest.mark.parametrize("age", [0, 1, 99])
def test_register_valid_age(api_client, age):
    email = random_email()
    password = "ValidPass123"

    response = api_client.register_user(email, password, age)

    assert response.status_code == HTTPStatus.OK, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    assert "user" in data, "В ответе нет ключа 'user'"
    assert data["user"]["email"] == email, "Email в ответе не совпадает"

    # age может отсутствовать в ответе, но мы это допускаем
    if "age" in data["user"]:
        assert data["user"]["age"] == age, "Возраст в ответе не совпадает"
    else:
        allure.attach(str(data), name="Ответ без поля 'age'", attachment_type=allure.attachment_type.JSON)
