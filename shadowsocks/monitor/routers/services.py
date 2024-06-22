from bs4 import BeautifulSoup
from typing import AsyncGenerator
from httpx import AsyncClient
import subprocess


switch_url = "http://192.168.66.1"


def get_LAN_address(interface: str) -> str:
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


def get_pc_name() -> str:
    cmd = "hostname"
    result = subprocess.run(
        cmd, shell=True, check=False, stdout=subprocess.PIPE, text=True
    )
    pc_name = result.stdout.strip()
    return pc_name


def with_login(func: callable):
    login_body = {
        "LanguageType": 5,
        "loginUsername": "admin",
        "loginPassword": "Ch@nGeM1",
    }

    async def wrapper(*args):
        async with AsyncClient(base_url=switch_url, follow_redirects=False) as ac:
            await ac.post("/goform/login", data=login_body)
            response = await func(ac, *args)
            await ac.get("/logout.asp")
            return response

    return wrapper


async def parse_goform(html: str) -> AsyncGenerator[dict, any]:
    body_soup = BeautifulSoup(html, "lxml")
    table_div = body_soup.find("div", class_="table_data table_data12")
    soup = BeautifulSoup(str(table_div), "lxml")
    protocol = {"UDP": 3, "TCP": 4, "BOTH": 254}
    # 提取表格内容
    rows = soup.find_all("tr")[2:]  # 跳过前两行表头
    # data = []
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
            # data.append(entry)
            yield entry
    # return data


@with_login
async def update_router(async_client: AsyncClient, ip_addr: str):
    if ip_addr == "-1":
        return

    my_name = get_pc_name()
    res = await async_client.get("/RgForwarding.asp")
    async for data in parse_goform(res.text):
        data["PortForwardingLocalIp"] = ip_addr
        # Description can only accept less 14 length of string
        data["PortForwardingDesc"] = my_name if len(my_name) <= 14 else my_name[:14]
        await async_client.post("/goform/RgForwarding", data=data)
    # location = res.headers["Location"]


@with_login
async def get_switch_ip(async_client: AsyncClient) -> str:
    my_name = get_pc_name()
    res = await async_client.get("/RgForwarding.asp")
    ip_set = set()
    async for data in parse_goform(res.text):
        ip_set.add(data["PortForwardingLocalIp"])
    if len(ip_set) > 0:
        return list(ip_set)[0]
    else:
        return ""
