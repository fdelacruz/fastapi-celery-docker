from project.users.models import User
from project.users import users_router


def test_pytest_setup(client, db_session):
    # test view
    response = client.get(users_router.url_path_for("form_example_get"))
    assert response.status_code == 200

    # test db
    user = User(username="test", email="test@example.com")
    with db_session.begin():
        db_session.add(user)
    assert user.id
