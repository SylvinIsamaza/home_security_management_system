from fastapi import FastAPI
from .routers.user import router as user_router
from .routers.device import router as device_router
from .routers.alerts import router as alert_router

app = FastAPI()
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(device_router, prefix="/devices", tags=["devices"])
app.include_router(alert_router, prefix="/alerts", tags=["alerts"])
