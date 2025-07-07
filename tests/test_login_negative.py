import pytest
import allure
from http import HTTPStatus
from data import data_generator as gen


@allure.title("Получение текущего пользователя без токена — ожидаем 401")
def test_get_user_no_token(api_client):
    response = api_client.get_user_data(token="")

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@allure.title("Логин с пустым email")
def test_login_empty_email(api_client):
    response = api_client.login_user(email="", password=gen.random_password())
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Логин с пустым паролем")
def test_login_empty_password(api_client):
    response = api_client.login_user(email=gen.random_email(), password="")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Логин с пустыми email и паролем")
def test_login_empty_fields(api_client):
    response = api_client.login_user(email="", password="")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Логин с email, не зарегистрированным в системе")
def test_login_nonexistent_email(api_client):
    response = api_client.login_user(email="notregistered@example.com", password="Valid123")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Логин с неправильным паролем")
def test_login_wrong_password(api_client, new_user):
    response = api_client.login_user(email=new_user["email"], password="WrongPassword123")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Логин с email с пробелами по краям")
def test_login_email_with_spaces(api_client, new_user):
    email_with_spaces = f"   {new_user['email']}   "
    response = api_client.login_user(email=email_with_spaces, password=new_user["password"])
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Логин с SQL-инъекцией в email")
def test_login_sql_injection_email(api_client):
    sql_payload = "' OR '1'='1"
    response = api_client.login_user(email=sql_payload, password="Valid123")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@allure.title("Логин с SQL-инъекцией в пароле")
def test_login_sql_injection_password(api_client):
    response = api_client.login_user(email="valid@example.com", password="' OR '1'='1")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY