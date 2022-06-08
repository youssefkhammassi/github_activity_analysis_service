import uvicorn as uvicorn
from fastapi import FastAPI, APIRouter

from config.base import gaas_config
from config.injection import Container
from source import apis


def create_application():
    # Create the FastAPI application
    application = FastAPI(title='GitHub Activity analysis service',
                          version='0.0.1',
                          contact={'email': 'yousseff.khammassi@gmail.com'},
                          )
    # Injecting
    container = Container()
    application.container = container
    # Routers
    global_router = APIRouter()  # Router used to add a global prefix
    global_router.include_router(apis.github_activity_router, tags=["github activity routes"])
    application.include_router(global_router, prefix="/api")
    return application


app = create_application()


def run():
    return uvicorn.run("app:app", host=gaas_config.HOST, port=gaas_config.PORT)


if __name__ == "__main__":
    run()
