from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]


def test_get_existed_user():
    """Получение существующего пользователя"""
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]


def test_get_unexisted_user():
    """Получение несуществующего пользователя"""
    response = client.get("/api/v1/user", params={'email': 'unexisted@mail.com'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_create_user_with_valid_email():
    """Создание пользователя с уникальной почтой"""
    new_user = {
        'name': 'Sidor Sidorov',
        'email': 's.s.sidorov@mail.com'
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert isinstance(response.json(), int)


def test_create_user_with_invalid_email():
    """Создание пользователя с почтой, которую использует другой пользователь"""
    existing_user = {
        'name': 'Another Ivan',
        'email': users[0]['email']
    }
    response = client.post("/api/v1/user", json=existing_user)
    assert response.status_code == 409
    assert response.json() == {'detail': 'User with this email already exists'}


def test_delete_user():
    """Удаление пользователя"""
    email_to_delete = users[1]['email']
    response = client.delete("/api/v1/user", params={'email': email_to_delete})
    assert response.status_code == 204
    # Проверка, что пользователь действительно удален (опционально)
    response_get = client.get("/api/v1/user", params={'email': email_to_delete})
    assert response_get.status_code == 404
    assert response_get.json() == {'detail': 'User not found'}
