from unittest import mock

import requests

from project.users import users_router
from project.users.models import User


def test_pytest_setup(client, db_session):
    # test view
    response = client.get(users_router.url_path_for("form_example_get"))
    assert response.status_code == 200

    # test db
    user = User(username="test", email="test@example.com")
    with db_session.begin():
        db_session.add(user)
    assert user.id


def test_view_with_eager_mode(client, db_session, settings, monkeypatch):
    # Get the celery app from the FastAPI app instance
    # The 'client' fixture should give you access to the app
    celery_app = client.app.celery_app

    # Set Celery to eager mode directly on the celery app
    monkeypatch.setattr(celery_app.conf, "task_always_eager", True)
    monkeypatch.setattr(celery_app.conf, "task_eager_propagates", True)
    monkeypatch.setattr(celery_app.conf, "task_store_eager_result", True)

    mock_requests_post = mock.MagicMock()
    monkeypatch.setattr(requests, "post", mock_requests_post)

    monkeypatch.setattr(settings, "CELERY_TASK_ALWAYS_EAGER", True, raising=False)

    user_name = "fdelacruz"
    user_email = f"{user_name}@accordbox.com"
    response = client.post(
        users_router.url_path_for("user_subscribe"),
        json={"email": user_email, "username": user_name},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "send task to Celery successfully",
    }

    mock_requests_post.assert_called_with(
        "https://httpbin.org/delay/5", data={"email": user_email}
    )
