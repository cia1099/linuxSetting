from fastapi import APIRouter
from httpx import AsyncClient

router = APIRouter()


def get_LAN_address(interface: str) -> str:
    import subprocess

    cmd = "ifconfig %s | grep 'inet ' | awk '{ print $2 }' | cut -d/ -f1" % interface
    try:
        result = subprocess.run(
            cmd, shell=True, check=True, stdout=subprocess.PIPE, text=True
        )
        ip_addr = result.stdout.strip()
        if len(ip_addr.split(".")) != 4:
            raise
        return ip_addr
    except:
        return "-1"


def with_login(func: callable):
    login_body = {
        "LanguageType": 5,
        "loginUsername": "admin",
        "loginPassword": "Ch@nGeM1",
    }

    async def wrapper(*args):
        async with AsyncClient(
            base_url="http://192.168.66.1", follow_redirects=False
        ) as ac:
            await ac.post("/goform/login", data=login_body)
            response = await func(ac, *args)
            await ac.get("/logout.asp")
            return response

    return wrapper


@with_login
async def update_router(async_client: AsyncClient):
    body = {
        "PortForwardingCreateRemove": 0,
        "PortForwardingLocalIp": "192.168.66.103",
        "PortForwardingLocalStartPort": 22,
        "PortForwardingLocalEndPort": 23,
        "PortForwardingExtStartPort": 22,
        "PortForwardingExtEndPort": 23,
        "PortForwardingProtocol": 254,  # 3 UDP,4 TCP, 254 BOTH
        "PortForwardingDesc": "ssh8888",
        "PortForwardingEnabled": 1,
        "PortForwardingApply": 2,
        "PortForwardingTable": 1,  # which row in table
        "OverlapError": 0,
    }
    res = await async_client.post("/goform/RgForwarding", data=body)
    location = res.headers["Location"]


@router.get("/lan")
async def get_LAN(interface: str = ""):
    return {"LAN_address": get_LAN_address(interface)}
