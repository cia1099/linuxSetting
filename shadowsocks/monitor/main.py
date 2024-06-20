import asyncio
from fastapi import FastAPI, HTTPException
from routers.services import router as service_router
from routers.services import get_LAN_address, update_router, parse_goform


app = FastAPI()
app.include_router(service_router)

if __name__ == "__main__":
    # asyncio.run(update_router())

    import json, requests

    res = requests.get("http://192.168.66.1/RgForwarding.asp")
    jobj = parse_goform(res.text)
    print(json.dumps(jobj, indent=4))
    print(get_LAN_address("en0"))
