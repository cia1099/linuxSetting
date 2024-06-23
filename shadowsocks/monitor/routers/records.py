import asyncio, json, os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Generator

from models.record import Record

from routers.services import get_LAN_address, get_switch_ip, update_router, parse_goform
from fastapi import APIRouter, Request, HTTPException, status
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


def log_changed(info: dict):
    record_path = Path("ip_records.log")
    is_exit = record_path.exists() and record_path.stat().st_size < 1024 * 1024
    mode = "a" if is_exit else "w"
    with open(str(record_path), mode) as ofile:
        ofile.write("%s\n" % json.dumps(info))


def load_record_ip() -> str:
    record_path = Path("ip_records.log")
    if not (record_path.exists() and record_path.is_file()):
        return ""
    # 读取文件的最后一行
    with open(str(record_path), "rb") as file:
        file.seek(0, 2)  # 移动文件指针到文件末尾
        file_size = file.tell()  # 获取文件大小
        buffer = bytearray()
        for i in range(file_size - 1, -1, -1):
            file.seek(i)
            byte = file.read(1)
            if byte == b"\n" and buffer:
                break
            buffer.extend(byte)
        last_line = (
            buffer[::-1].decode("utf-8").strip()
        )  # 获取最后一行并去除前后空白字符
    return json.loads(last_line)["new"]


async def check_ip(interface: str, read_local: bool = True):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as executor:
        load_ip_task = loop.run_in_executor(executor, load_record_ip)
        get_lan_task = loop.run_in_executor(executor, get_LAN_address, interface)

    done = await asyncio.gather(
        load_ip_task if read_local else get_switch_ip(), get_lan_task
    )
    cached_ip, ip_addr = done

    detail = "log" if read_local else "switch"
    print(f"cached_ip is {cached_ip} ({detail})")
    print(f"current ip is {ip_addr}")
    if ip_addr == cached_ip or ip_addr == "-1":
        return
    info = {
        "asctime": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        "new": ip_addr,
        "old": cached_ip,
        "detail": detail,
    }
    with ThreadPoolExecutor() as executor:
        sync_task = loop.run_in_executor(executor, log_changed, info)
    # --- concurrent sync and async functions
    await asyncio.gather(sync_task, update_router(ip_addr))
    # log_changed(info) # debug


def read_file_reverse(filename: str) -> Generator[str, None, str]:
    with open(filename, "rb") as f:
        f.seek(0, os.SEEK_END)  # 移动到文件末尾
        position = f.tell()  # 获取文件末尾位置
        line = bytearray()  # 用于存储当前行的内容

        while position >= 0:
            f.seek(position)  # 移动到当前位置
            char = f.read(1)  # 读取一个字符

            if char == b"\n":  # 检查是否是换行符
                if line:
                    yield line.decode()[::-1]  # 打印当前行
                    line = bytearray()  # 重置行缓冲区
            else:
                line.extend(char)  # 将字符添加到当前行的缓冲区

            position -= 1  # 向前移动位置

        if line:  # 打印文件的第一行
            return line.decode()[::-1]


@router.get("/lan")
async def get_LAN(req: Request, interface: str = ""):
    ip_addr = get_LAN_address(interface)
    if ip_addr == "-1":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The interface doesn't exist",
        )
    return templates.TemplateResponse(
        "records.html",
        {
            "request": req,
            "ip_addr": ip_addr,
            "records": [
                Record.from_dict(json.loads(r))
                for r in read_file_reverse("ip_records.log")
            ],
        },
    )


if __name__ == "__main__":
    with open("ip_records.log", "r") as f:
        objs = [json.loads(line.strip()) for line in f.readlines()]
    for obj in objs:
        obj["detail"] = "123"
    encode_objs = [json.dumps(obj) for obj in objs]
    with open("ip_records.log", "w") as f:
        f.write("\n".join(encode_objs))
