import asyncio
from fastapi import FastAPI, HTTPException
from routers.services import router as service_router
from routers.services import get_LAN_address, update_router


app = FastAPI()
app.include_router(service_router)

if __name__ == "__main__":
    asyncio.run(update_router())
    print(get_LAN_address("en0"))
