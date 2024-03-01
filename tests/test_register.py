import allure
from conftest import register_user_fixture


@allure.story('Регистрация пользователя')
class TestRegisterUser:
    @allure.title('Создание уникального пользователя')
    def test_example(self, register_user_fixture):
        user_data = {"email": "naumovafox14@ya.ru", "password": "24675Kris", "name": "Kristina"}
        user = register_user_fixture(user_data)
        assert user['response'].status_code == 200
        assert user['response'].json().get('success') is True

    @allure.title('Создание пользователя, который уже зарегистрирован')
    def test_create_duplicate_user(self, register_user_fixture):
        user_data = {"email": "naumovafox3445@ya.ru", "password": "24675Kris", "name": "Kristina"}
        response_1 = register_user_fixture(user_data)
        response_2 = register_user_fixture(user_data)
        assert response_2['response'].status_code == 403
        assert response_2['response'].json()['message'] == "User already exists"

    @allure.title('Создание пользователя без заполнения одного из обязательных полей')
    def test_create_user_missing_one_field(self, register_user_fixture):
        user_data = {"email": "naumovafox123@ya.ru", "password": "24675Kris", "name": ""}
        response = register_user_fixture(user_data)
        assert response['response'].status_code == 403
        assert response['response'].json()['message'] == "Email, password and name are required fields"
