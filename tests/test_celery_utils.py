from project.celery_utils import custom_celery_task
from project.database import db_context
from project.users.models import User


# tasks


@custom_celery_task()
def successful_task(user_id):
    with db_context() as session:
        user = session.get(User, user_id)
        user.username = "test"
        session.commit()


# tests


def test_custom_celery_task(db_session, settings, user, monkeypatch):
    monkeypatch.setattr(settings, "CELERY_TASK_ALWAYS_EAGER", True, raising=False)

    successful_task.delay(user.id)

    assert db_session.get(User, user.id).username == "test"
