from celery import Celery
from fastapi import FastAPI

app = FastAPI()

celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0",
)

# Add this to your Celery config to silence the warning
celery.conf.update(
    broker_connection_retry_on_startup=True,
)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@celery.task
def divide(x, y):
    import time

    time.sleep(5)
    return x / y
