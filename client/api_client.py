import requests
from config.settings import BASE_URL

class APIClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def register_user(self, email, password, age):
        url = f"{self.base_url}/auth/register"
        data = {"email": email, "password": password, "age": age}
        return self.session.post(url, json=data)

    def login_user(self, email, password):
        url = f"{self.base_url}/auth/login"
        data = {"email": email, "password": password}
        return self.session.post(url, json=data)

    def check_user_exist(self, email):
        url = f"{self.base_url}/exist"
        data = {"email": email}
        return self.session.post(url, json=data)

    def update_user_name(self, token, name):
        url = f"{self.base_url}/user/name"
        headers = {"Authorization": f"Bearer {token}"}
        data = {"name": name}
        return self.session.patch(url, json=data, headers=headers)

    def get_user_data(self, token):
        url = f"{self.base_url}/user/me"
        headers = {"Authorization": f"Bearer {token}"}
        return self.session.get(url, headers=headers)
