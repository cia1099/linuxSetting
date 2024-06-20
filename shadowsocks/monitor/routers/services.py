import asyncio
from bs4 import BeautifulSoup
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


def parse_goform(html: str) -> list[dict]:
    body_soup = BeautifulSoup(html, "lxml")
    table_div = body_soup.find("div", class_="table_data table_data12")
    soup = BeautifulSoup(str(table_div), "lxml")
    # 提取表头
    # header = [th.get_text() for th in soup.find_all("th") if th.get_text()]
    protocol = {"UDP": 3, "TCP": 4, "BOTH": 254}
    # 提取表格内容
    rows = soup.find_all("tr")[2:]  # 跳过前两行表头
    data = []
    for i, row in enumerate(rows):
        cells = row.find_all("td")
        if len(cells) > 0:  # 跳过空行
            entry = {
                "PortForwardingCreateRemove": 0,
                "PortForwardingLocalIp": cells[0].get_text(),
                "PortForwardingLocalStartPort": int(cells[1].get_text()),
                "PortForwardingLocalEndPort": int(cells[2].get_text()),
                "PortForwardingExtStartPort": int(cells[3].get_text()),
                "PortForwardingExtEndPort": int(cells[4].get_text()),
                "PortForwardingProtocol": protocol[cells[5].get_text()],
                "PortForwardingDesc": cells[6].get_text(),
                "PortForwardingEnabled": 1,  # cells[7].get_text(),
                "PortForwardingApply": 2,
                "PortForwardingTable": i,  # which row in table
                "OverlapError": 0,
            }
            data.append(entry)
    return data


@with_login
async def update_router(async_client: AsyncClient, interface: str):
    ip_addr = get_LAN_address(interface)
    if ip_addr == "-1":
        return
    res = await async_client.get("/RgForwarding.asp")
    data = parse_goform(res.text)
    for d in data:
        d["PortForwardingLocalIp"] = ip_addr
    #     _ = await async_client.post("/goform/RgForwarding", data=d)
    await asyncio.gather(
        *(async_client.post("/goform/RgForwarding", data=d) for d in data)
    )
    # location = res.headers["Location"]


@router.get("/lan")
async def get_LAN(interface: str = ""):
    return {"LAN_address": get_LAN_address(interface)}