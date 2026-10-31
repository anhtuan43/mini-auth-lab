from sqlmodel import create_engine
# Tạo file database.db ngay trong thư mục hiện tại
sqlite_url = "sqlite:///./database.db"
engine = create_engine(sqlite_url, echo=True)
