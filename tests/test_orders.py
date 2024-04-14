import allure
from conftest import register_user_fixture
from utils.api_client import APIClient


@allure.story('Создание заказов')
class TestCreateOrder:
    @allure.title('Создание заказа с авторизацией и ингредиентами')
    def test_create_order_with_authorization(self, register_user_fixture):
        user_data = {"email": "naumovafox14@ya.ru", "password": "24675Kris", "name": "Kristina"}
        user = register_user_fixture(user_data)
        api = APIClient()
        response = api.auth_user(user_data['email'], user_data['password'])
        response_create = api.create_order(["61c0c5a71d1f82001bdaaa6d"])
        assert response_create.status_code == 200
        assert response_create.json().get('name') == "Флюоресцентный бургер"

    @allure.title('Создание заказа без авторизации')
    def test_create_order_without_authorization(self):
        api = APIClient()
        response_create = api.create_order(["61c0c5a71d1f82001bdaaa6f"])
        assert response_create.status_code == 200
        assert response_create.json().get('name') == "Бессмертный бургер"

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients(self):
        api = APIClient()
        response_create = api.create_order([])
        assert response_create.status_code == 400
        assert response_create.json().get('message') == "Ingredient ids must be provided"

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_with_invalid_ingredients(self):
        api = APIClient()
        response_create = api.create_order(["Hello!123"])
        assert response_create.status_code == 500
