import allure
import pytest
from utils.api_client import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
@allure.step('Регистрируем пользователя')
def register_user_fixture(request):
    user = {}

    def register_user(data):
        nonlocal user
        response = APIClient().create_new_user(
            endpoint='register',
            email=data['email'],
            password=data['password'],
            name=data['name']
        )
        user.update({
            "response": response,
            "accessToken": response.json().get('accessToken', '')
        })
        return user

    yield register_user
    request.addfinalizer(lambda: APIClient().delete_user(authorization=user.get("accessToken")))
