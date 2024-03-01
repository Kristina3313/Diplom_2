import allure
from conftest import register_user_fixture
from utils.api_client import APIClient


@allure.story('Получение заказов конкретного пользователя')
class TestGetOrders:
    @allure.title('Получение заказов авторизованным пользователем')
    def test_get_orders_with_authorized_user(self, register_user_fixture):
        user_data = {"email": "naumovafox14@ya.ru", "password": "24675Kris", "name": "Kristina"}
        user = register_user_fixture(user_data)
        api = APIClient()
        response_auth = api.auth_user(user_data['email'], user_data['password'])
        authorization_token = response_auth.json().get('accessToken', '')
        get_response = api.get_orders(authorization_token)
        assert get_response.status_code == 200
        assert get_response.json()['success'] is True

    @allure.title('Получение заказов неавторизованным пользователем')
    def test_get_orders_with_unauthorized_user(self):
        api = APIClient()
        get_response = api.get_orders()
        assert get_response.status_code == 401
        assert get_response.json().get('message') == "You should be authorised"
