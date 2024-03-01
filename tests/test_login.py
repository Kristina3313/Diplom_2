import allure
from conftest import register_user_fixture
from utils.api_client import APIClient


@allure.story('Авторизация пользователя')
class TestLoginUser:
    @allure.title('Логин под существующим пользователем')
    def test_authorization_existing_user(self, register_user_fixture):
        user_data = {"email": "naumovafox14@ya.ru", "password": "24675Kris", "name": "Kristina"}
        user = register_user_fixture(user_data)
        api = APIClient()
        response = api.auth_user(user_data['email'], user_data['password'])
        assert response.status_code == 200
        assert user['response'].json().get('success') is True

    @allure.title('Логин с неверным логином и паролем')
    def test_authorization_with_invalid_login_and_password(self):
        user_data = {"email": "naumovafox16@ya.ru", "password": "24675Kris"}
        api = APIClient()
        response = api.auth_user(user_data['email'], user_data['password'])
        assert response.status_code == 401
        assert response.json()['message'] == "email or password are incorrect"
