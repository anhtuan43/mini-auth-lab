from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# UM-TC-001: Đăng nhập thành công
def test_login_success():
    response = client.post("/login?email=admin@example.com&password=admin123")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "password" not in data # Đảm bảo không lộ pass

# UM-TC-002: Đăng nhập sai mật khẩu
def test_login_wrong_password():
    response = client.post("/login?email=admin@example.com&password=wrongpass")
    assert response.status_code == 401
    assert "access_token" not in response.json()

# UM-TC-007: Truy cập API với Token giả mạo
def test_me_with_fake_token():
    headers = {"Authorization": "Bearer fake_token_12345"}
    response = client.get("/me", headers=headers)
    assert response.status_code == 401
