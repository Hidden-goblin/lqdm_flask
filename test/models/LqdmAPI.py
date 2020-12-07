from models.ApiAbstraction import ApiAbstraction
import requests


class LqdmAPI(ApiAbstraction):
    def __init__(self, url):
        ApiAbstraction.__init__(self, url)
        self.__token = None

    def login(self, email, password, is_recorded: bool = True):
        endpoint = f"{self.url}/v1/api/auth/login"
        payload = {"email": email,
                   "password": password}

        response = requests.post(url=endpoint, json=payload)
        if is_recorded:
            self.history = response

        return response

    def logout(self, email, is_recorded: bool = True):
        endpoint = f"{self.url}/v1/api/auth/logout"
        payload = {"email": email}

        response = requests.post(url=endpoint, json=payload, headers=self.__generate_header())

        if is_recorded:
            self.history = response

        return response

    def sign_up(self, email, password, is_recorded: bool = True):
        endpoint = f"{self.url}/v1/api/auth/signup"
        payload = {"email": email,
                   "password": password}
        response = requests.post(url=endpoint, json=payload)
        if is_recorded:
            self.history = response

        return response

    def delete_user(self, email, is_recorded: bool = True):
        endpoint = f"{self.url}/v1/api/users/{email}"

        response = requests.delete(url=endpoint, headers=self.__generate_header())

        if is_recorded:
            self.history = response

        return response

    def update_user(self, email, account, is_recorded: bool = True):
        endpoint = f"{self.url}/v1/api/users/{email}"

        response = requests.put(url=endpoint, json=account, headers=self.__generate_header())

        if is_recorded:
            self.history = response

        return response

    def users(self, email: str = None, page: int = None, per_page: int = None, is_recorded: bool = True):
        if email is not None:
            endpoint = f"{self.url}/v1/api/users/{email}"

            response = requests.get(url=endpoint, headers= self.__generate_header())

    def __generate_header(self):
        return {"Authorization": f"Bearer {self.__token}"}