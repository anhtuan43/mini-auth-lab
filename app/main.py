from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import datetime

app = FastAPI()
# SECRET_KEY = "my_super_secret_key"
SECRET_KEY = "main_secret_key_123"
security = HTTPBearer()

# API Đăng nhập
@app.post("/login")
def login(email: str, password: str):
    if email == "admin@example.com" and password == "admin123":
        # Tạo token hết hạn sau 30 phút
        payload = {
            "sub": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return {"access_token": token}
    
    raise HTTPException(status_code=401, detail="Sai email hoặc mật khẩu")

# API Lấy thông tin (Yêu cầu Token)
@app.get("/me")
def get_me(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        return {"message": "Thành công", "user": payload["sub"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token đã hết hạn")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token không hợp lệ")
