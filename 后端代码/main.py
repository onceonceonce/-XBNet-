from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI,APIRouter
from starlette.middleware.cors import CORSMiddleware

from DataRoutes.download_data import download_router
from DataRoutes.query_route import query_router
from DataRoutes.upload_data import upload_router
from db_connector.db_connector1 import database

from loguru import logger

# #模块总前缀
# base_router = APIRouter(prefix="/api/v1/ThirdPartyPlatformInteractionModule")
# #将提供第三方数据的路由作为子路由添加到总路由
# base_router.include_router(third_service_dealer.third_party_route)

async def on_startup():
    logger.info("app开始启动...")
    async def init_database():
        logger.info("连接到数据库..")
        try:
            await database.third_create_tables()
        except Exception as e:
            logger.error(f"创建数据库表时发生未知错误: ")
            logger.exception(e)
            exit(-1)
        logger.success("连接到数据库成功...")

    logger.info("正在启动..")
    await init_database()


async def on_shutdown():
    logger.info("app关闭...")
    pass

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    定义生命周期，在app运行之前做一些事，之后做一些事
    """
    await on_startup()
    yield
    await on_shutdown()


app = FastAPI(lifespan=lifespan,arbitrary_types_allowed=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # 配置允许域名
# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:9528",
# ]
# # 配置允许域名列表、允许方法、请求头、cookie等
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(query_router)
app.include_router(upload_router)
app.include_router(download_router)

if __name__ == "__main__":
    uvicorn.run("main:app",port=8000,reload=True)




