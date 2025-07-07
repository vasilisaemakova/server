import pytest
import allure
from http import HTTPStatus
from data.data_generator import random_email, random_password, random_age
from schemas.user import User
from data import data_generator as gen

@allure.title("Успешный логин после регистрации")
def test_successful_login(api_client):
    email = random_email()
    password = random_password()
    age = random_age()

    register_response = api_client.register_user(email=email, password=password, age=age)
    assert register_response.status_code == HTTPStatus.OK


    login_response = api_client.login_user(email=email, password=password)
    assert login_response.status_code == HTTPStatus.OK

    data = login_response.json()


    assert "token" in data
    assert "user" in data

    user = data["user"]
    assert isinstance(user["id"], int)
    assert user["email"] == email
    assert user["name"] == "Neko" 
    assert user["age"] == age
    