import pytest
import allure


@allure.title("Изменение имени пользователя")
def test_change_user_name(api_client, new_user):
    token = new_user["token"]
    new_name = "MyNewCoolName"

    update_response = api_client.update_user_name(token, new_name)
    assert update_response.status_code == 200

    user_info = api_client.get_user_data(token).json()
    assert user_info["user"]["name"] == new_name