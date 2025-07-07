import pytest
from faker import Faker
from client.api_client import APIClient
from data.data_generator import random_email as gen_email, random_password as gen_password, random_age

fake = Faker()

@pytest.fixture(scope="session")
def api_client():
    return APIClient()

@pytest.fixture
def new_user(api_client):
    email = gen_email()
    password = gen_password()
    age = random_age()

    reg_response = api_client.register_user(email, password, age)
    assert reg_response.status_code == 200
    
    login_response = api_client.login_user(email, password)
    assert login_response.status_code == 200
    token = login_response.json()["token"]

    yield {
        "email": email,
        "password": password,
        "age": age,
        "token": token
    }

@pytest.fixture
def random_email():
    return gen_email()

@pytest.fixture
def random_password():
    return gen_password()