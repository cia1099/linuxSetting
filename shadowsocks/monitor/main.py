import asyncio, argparse
import time, os
from datetime import datetime
from multiprocessing import Process
from fastapi import FastAPI, HTTPException
from routers.records import check_ip
from routers.services import get_LAN_address
from routers.services import router as service_router


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

    p = Process(
        target=os.system,
        args=("nohup uvicorn main:app --host 0.0.0.0 --port 50050 > /dev/null &",),
    )
    p.daemon = True
    p.run()
    while True:
        # now = datetime.now().strftime("%H:%M:%S")
        # print(f"what time is this? {now}")
        asyncio.run(check_ip(interface))
        time.sleep(args.time)

else:
    app = FastAPI()
    app.include_router(service_router)
