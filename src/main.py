import uvicorn

from src.config import app_settings

if __name__ == '__main__':
    uvicorn.run(
        app='src.app:app',
        host=app_settings.BACK_HOST,
        port=int(app_settings.BACK_PORT),
    )
