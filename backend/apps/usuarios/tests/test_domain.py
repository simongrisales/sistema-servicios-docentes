from ..domain.entities import Role, User


def test_usuario_entidad_conserva_username():
    user = User(
        user_id=1,
        username="testuser",
        email="test@example.com",
        password="",
        role=Role(1, "Admin", "Administrador"),
    )

    assert user.username == "testuser"
