from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api import users
from database import engine
from models.user import User
from models.session import UserSession
import uvicorn

# 创建数据库表
User.metadata.create_all(bind=engine)
UserSession.metadata.create_all(bind=engine)

app = FastAPI(
    title="用户管理系统",
    description="用户注册、登录、登出和信息管理API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "欢迎使用用户管理系统API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(main, host="0.0.0.0", port=8000)