import asyncio, argparse
import time, os
from datetime import datetime
from multiprocessing import Process
from fastapi import FastAPI, HTTPException, Response
from routers.records import check_ip
from routers.records import router as record_router
from routers.services import get_LAN_address


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="monitor switch LAN ip distribution in this machine"
    )
    parser.add_argument(
        "-i",
        "--interface",
        type=str,
        default=" ",
        help="your LAN connected ip. It must connect to 192.168.66.x. You can use 'nmcli d' to see which device.",
    )
    parser.add_argument(
        "-t",
        "--time",
        default=60,
        type=int,
        help="How long do check ip address in second",
    )
    args = parser.parse_args()

    interface = args.interface
    if get_LAN_address(interface) == "-1":
        print(
            f"\x1b[4mCan't find valid \x1b[36mip address\x1b[0m\x1b[4m in interface: \x1b[1m\x1b[31m{interface}\x1b[0m"
        )
        assert get_LAN_address(interface) != "-1"
    assert isinstance(args.time, int)

    p = Process(
        target=os.system,
        args=("nohup uvicorn main:app --host 0.0.0.0 --port 50050 > /dev/null &",),
    )
    p.daemon = True
    p.run()
    i = 0
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        print(f"what \x1b[92mtime\x1b[0m is this? \x1b[92m{now}\x1b[0m")
        asyncio.run(check_ip(interface, i % 10 > 0))
        time.sleep(args.time)
        i += 1
        if i // 10 > 0:
            i = 0

else:
    app = FastAPI()
    app.include_router(record_router)


@app.get("/manifest.json")
async def get_json():
    with open(f"manifest.json", "r") as f:
        return Response(f.read(), media_type="application/json")


@app.get("/assets/{image_name}.png")
async def assets_png(image_name: str):
    try:
        with open(f"assets/{image_name}.png", "rb") as f:
            return Response(f.read(), media_type="image/png")
    except:
        raise HTTPException(404, detail=image_name)


"""
TODO: fastAPI URL can't parse "/xx/xx" in a str, 
you have to separate individually '/' in manual


@app.get("/{script_name}.js")
async def get_script(script_name: str):
    with open(f"{script_name}.js", "r") as f:
        return Response(f.read(), media_type="application/javascript")


@app.get("/{style_name}.css")
async def get_style(style_name: str):
    with open(f"{style_name}.css", "r") as f:
        return Response(f.read(), media_type="text/css")

"""
