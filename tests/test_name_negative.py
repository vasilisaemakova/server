import pytest
import allure
from http import HTTPStatus


@allure.epic("Редактирование имени")
@allure.feature("Негативные сценарии")
class TestChangeNameNegative:

    @allure.title("Пустое имя")
    def test_empty_name(self, api_client, new_user):
        token = new_user["token"]
        response = api_client.update_user_name(token, "")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        json_data = response.json()
        assert "found" in json_data, f"Ожидалось поле 'found' в ответе: {json_data}"
        assert "name" in json_data["found"], f"Ожидалось поле 'name' в 'found': {json_data}"

    @allure.title("Имя из пробелов")
    def test_name_with_whitespace(self, api_client, new_user):
        token = new_user["token"]
        response = api_client.update_user_name(token, "     ")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert "fields" in response.json() or "message" in response.json()


    @allure.title("SQL-инъекция в имени")
    def test_name_sql_injection(self, api_client, new_user):
        token = new_user["token"]
        response = api_client.update_user_name(token, "' OR 1=1 --")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert "fields" in response.json() or "message" in response.json()

    @allure.title("Управляющие символы в имени (невалидная кодировка)")
    def test_name_with_control_chars(self, api_client, new_user):
        token = new_user["token"]
        response = api_client.update_user_name(token, "\x00\x01")
        assert response.status_code in [HTTPStatus.UNPROCESSABLE_ENTITY, HTTPStatus.INTERNAL_SERVER_ERROR]
        assert "found" in response.json()

    @allure.title("Обновление имени без токена")
    def test_update_name_without_token(self, api_client):
        response = api_client.update_user_name(token="", name="ValidName")
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert "message" in response.json()

    @allure.title("Обновление имени с невалидным токеном")
    def test_update_name_invalid_token(self, api_client):
        response = api_client.update_user_name(token="Bearer faketoken123", name="ValidName")
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert "message" in response.json()

