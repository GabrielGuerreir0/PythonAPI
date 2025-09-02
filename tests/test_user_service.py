import pytest
from fastapi import HTTPException
from app.services import user_service
from app.schemas.user_schema import UserCreate
from unittest.mock import patch
import base64

# Mock da função de hash de senha para simplificar os testes
@patch("app.core.security.get_password_hash", side_effect=lambda password: password + "hashed")
def test_register_user_service_success(mock_get_password_hash, db_session):
    username = "testuser"
    email = "test@example.com"
    full_name = "Test User"
    password = "securepassword"
    profile_image_data = base64.b64encode(b"fake_image_data")

    response = user_service.register_user_service(
        username, email, full_name, password, profile_image_data, db_session
    )

    assert response["message"] == "Usuário criado com sucesso!"
    assert "user_id" in response
    assert isinstance(response["user_id"], int)

    created_user = user_service.get_user_by_id_service(response["user_id"], db_session)
    assert created_user["username"] == username
    assert created_user["email"] == email

def test_get_user_by_id_service_found(db_session):

    user_data = {
        "username": "existing_user",
        "email": "existing@example.com",
        "full_name": "Existing User",
        "hashed_password": "securepasswordhashed",
        "profile_image": b"fake_image_data"
    }
    user = user_service.user_model.User(**user_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    found_user = user_service.get_user_by_id_service(user.id, db_session)

    assert found_user["id"] == user.id
    assert found_user["username"] == "existing_user"
    assert found_user["email"] == "existing@example.com"
