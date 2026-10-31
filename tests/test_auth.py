from fastapi.testclient import TestClient
from app.main import app
from app.database import engine
from app.models import User
from sqlmodel import Session, select

client = TestClient(app)

# Hàm phụ trợ để đảm bảo DB có user admin trước khi test
def setup_db():
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == "admin@example.com")).first()
        if not user:
            session.add(User(email="admin@example.com", password="admin123"))
            session.commit()

# UM-TC-001: Đăng nhập thành công (Code đúng)
def test_login_success():
    setup_db()
    response = client.post("/login?email=admin@example.com&password=admin123")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "password" not in data

# UM-TC-002: Đăng nhập sai mật khẩu (Code đúng)
def test_login_wrong_password():
    setup_db()
    response = client.post("/login?email=admin@example.com&password=wrongpass")
    assert response.status_code == 401

# UM-TC-007: Truy cập API với Token giả mạo (Code đúng)
def test_me_with_fake_token():
    headers = {"Authorization": "Bearer fake_token_12345"}
    response = client.get("/me", headers=headers)
    assert response.status_code == 401

# TEST CỐ TÌNH GÂY LỖI (Để xem CI báo đỏ)
def test_intentional_fail():
    # Code backend trả về 401 (vì user này không có trong DB), 
    # nhưng chúng ta cố tình assert nó phải là 200 để test bị Fail.
    response = client.post("/login?email=khong_ton_tai@example.com&password=123")
    assert response.status_code == 200 