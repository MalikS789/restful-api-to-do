import pytest
from flask import json

from app import create_app, db
from app.models import User


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()


@pytest.fixture(scope='module')
def new_user():
    user = User(username='testuser', password='testpass')
    return user


@pytest.fixture(scope='module')
def auth_token(test_client, new_user):
    # Register the user
    test_client.post('/register', json={
        'username': new_user.username,
        'password': 'testpass'
    })

    # Login to get a JWT token
    response = test_client.post('/login', json={
        'username': new_user.username,
        'password': 'testpass'
    })

    token = json.loads(response.data)['access_token']
    return f'Bearer {token}'


def test_create_task_success(test_client, auth_token):
    response = test_client.post('/tasks', json={
        'title': 'Test Task',
        'description': 'A test task description',
        'completed': False
    }, headers={
        'Authorization': auth_token
    })
    assert response.status_code == 201
    assert b'Test Task' in response.data


def test_get_all_tasks_success(test_client, auth_token):
    response = test_client.get('/tasks', headers={
        'Authorization': auth_token
    })
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)


def test_get_task_by_id_success(test_client, auth_token):
    create_response = test_client.post('/tasks', json={
        'title': 'Another Task',
        'description': 'Another task description',
        'completed': False
    }, headers={
        'Authorization': auth_token
    })
    task_id = json.loads(create_response.data)['id']

    response = test_client.get(f'/tasks/{task_id}', headers={
        'Authorization': auth_token
    })
    assert response.status_code == 200
    assert b'Another Task' in response.data


def test_get_task_invalid_id(test_client, auth_token):
    response = test_client.get('/tasks/9999', headers={
        'Authorization': auth_token
    })
    assert response.status_code == 404
    assert b'Task not found' in response.data


def test_update_task_success(test_client, auth_token):
    create_response = test_client.post('/tasks', json={
        'title': 'Update Task',
        'description': 'Update task description',
        'completed': False
    }, headers={
        'Authorization': auth_token
    })
    task_id = json.loads(create_response.data)['id']

    update_response = test_client.put(f'/tasks/{task_id}', json={
        'title': 'Updated Task',
        'description': 'Updated task description',
        'completed': True
    }, headers={
        'Authorization': auth_token
    })
    assert update_response.status_code == 200
    assert b'Updated Task' in update_response.data


def test_update_task_fail(test_client, auth_token):
    create_response = test_client.post('/tasks', json={
        'title': 'Task',
        'description': 'Task description',
        'completed': False
    }, headers={
        'Authorization': auth_token
    })
    task_id = json.loads(create_response.data)['id']

    update_response = test_client.put(f'/tasks/{task_id}', json={
        'title': '',
        'description': 'This update should fail',
        'completed': True
    }, headers={
        'Authorization': auth_token
    })
    assert update_response.status_code == 400


def test_delete_task_success(test_client, auth_token):
    create_response = test_client.post('/tasks', json={
        'title': 'Task to Delete',
        'description': 'Task description',
        'completed': False
    }, headers={
        'Authorization': auth_token
    })
    task_id = json.loads(create_response.data)['id']

    delete_response = test_client.delete(f'/tasks/{task_id}', headers={
        'Authorization': auth_token
    })
    assert delete_response.status_code == 200
    assert b'Task deleted' in delete_response.data


def test_delete_task_invalid_id(test_client, auth_token):
    response = test_client.delete('/tasks/9999', headers={
        'Authorization': auth_token
    })
    assert response.status_code == 404
    assert b'Task not found' in response.data


def test_login_success(test_client):
    test_client.post('/register', json={
        'username': 'testuser',
        'password': 'testpass'
    })

    response = test_client.post('/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })

    assert response.status_code == 200
    assert b'token' in response.data


def test_login_invalid_credentials(test_client):
    response = test_client.post('/login', json={
        'username': 'wronguser',
        'password': 'wrongpass'
    })
    assert response.status_code == 401
    assert b'Invalid credentials' in response.data


def test_create_task_missing_information(test_client, auth_token):
    response = test_client.post('/tasks', headers={
        'Authorization': auth_token
    }, json={
        'title': '',
        'description': 'Missing title',
        'completed': False
    })
    assert response.status_code == 400


def test_get_tasks_success(test_client, auth_token):
    response = test_client.get('/tasks', headers={
        'Authorization': auth_token
    })
    assert response.status_code == 200
    assert len(json.loads(response.data)) >= 1


def test_get_task_by_invalid_id(test_client, auth_token):
    response = test_client.get('/tasks/999', headers={
        'Authorization': auth_token
    })
    assert response.status_code == 404
    assert b'Task not found' in response.data


def test_update_task_invalid_id(test_client, auth_token):
    response = test_client.put('/tasks/999', headers={
        'Authorization': auth_token
    }, json={
        'title': 'Updated Task',
        'completed': True
    })
    assert response.status_code == 404
    assert b'Task not found' in response.data
