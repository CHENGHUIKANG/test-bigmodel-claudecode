from database import engine, Base
from models.user import User
from models.session import UserSession

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("数据库表创建成功！")

if __name__ == "__main__":
    create_tables()