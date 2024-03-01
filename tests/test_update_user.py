import allure
import pytest
from utils.api_client import APIClient
from conftest import register_user_fixture


@allure.story('Изменение данных пользователя')
class TestUpdateUser:
    @allure.title('Изменение данных пользователя без авторизации')
    @pytest.mark.parametrize("field_to_update, new_value", [("name", "Kristina123"),
                                                            ("email", "new_email@example.com"),("password", "passwo")])
    def test_update_user_without_authorization(self, field_to_update, new_value):
        api = APIClient()
        updated_user_data = {field_to_update: new_value}
        response_update = api.update_user_data(updated_user_data)
        assert response_update.status_code == 401
        assert response_update.json()['message'] == "You should be authorised"

    @allure.title('Изменение данных пользователя с авторизацией')
    @pytest.mark.parametrize("updated_name, updated_password", [("TestName", "NewPassword"),
                                                               ("AnotherName", "AnotherPassword")])
    def test_update_user_with_authorization(self, register_user_fixture, updated_name, updated_password):
        user_data = {"email": "naumovafox21@ya.ru", "password": "24675Kris", "name": "Kristina"}
        user = register_user_fixture(user_data)
        api = APIClient()
        response_auth = api.auth_user(user_data['email'], user_data['password'])
        authorization_token = response_auth.json().get('accessToken', '')
        updated_user_data = {"name": updated_name, "password": updated_password}
        response_update = api.update_user_data(updated_user_data, authorization=authorization_token)
        assert response_update.status_code == 200
        assert response_update.json()['success'] is True

    @allure.title('Изменение данных на уже используемую почту пользователя с авторизацией')
    def test_update_user_with_authorization_with_mail_used(self, register_user_fixture,):
        user_data = {"email": "naumovafox21@ya.ru", "password": "24675Kris", "name": "Kristina"}
        user = register_user_fixture(user_data)
        api = APIClient()
        response_auth = api.auth_user(user_data['email'], user_data['password'])
        authorization_token = response_auth.json().get('accessToken', '')
        updated_user_data = {"email": "crystalkris13@yandex.ru"}
        response_update = api.update_user_data(updated_user_data, authorization=authorization_token)
        assert response_update.status_code == 403
        assert response_update.json()['message'] == "User with such email already exists"
