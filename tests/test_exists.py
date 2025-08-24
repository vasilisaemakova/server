import pytest
import allure
from http import HTTPStatus
from data.data_generator import random_email
from schemas.exist import ExistResponse


@allure.title("Проверка на ШОКовость — зарегистрированный пользователь")
def test_exist_registered_user(api_client, new_user):
    response = api_client.check_user_exist(new_user["email"])
    assert response.status_code == HTTPStatus.OK

    data = ExistResponse(**response.json())
    assert data.exist is True


@allure.title("Проверка на ШОКовость — незарегистрированный пользователь")
def test_exist_unregistered_user(api_client, random_email):
    response = api_client.check_user_exist(random_email)
    assert response.status_code == HTTPStatus.OK

    data = ExistResponse(**response.json())
    assert data.exist is False


@allure.title("Проверка на ШОКовость — email без @")
def test_exist_invalid_email_no_at(api_client):
    response = api_client.check_user_exist("invalidemail.com")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Проверка на ШОКовость — email без точки")
def test_exist_invalid_email_no_dot(api_client):
    response = api_client.check_user_exist("user@invalid")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Проверка на ШОКовость — пустой email")
def test_exist_empty_email(api_client):
    response = api_client.check_user_exist("")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Проверка на ШОКовость — SQL-инъекция в поле email")
def test_exist_sql_injection_email(api_client):
    sql_email = "' OR '1'='1"
    response = api_client.check_user_exist(sql_email)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
