import logging
import math
import threading
import time
from pathlib import Path

import psutil
import speedtest
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")


# Store previous counters
logger = logging.getLogger(__name__)
old = psutil.net_io_counters()

# Live speed state
live_speed = {
    "download": 0,
    "upload": 0
}

# Ookla test state
max_speed = {
    "download": None,
    "upload": None,
    "ping": None,
    "running": False,
    "error": None,
}

def monitor_network():
    global old

    while True:
        time.sleep(1)

        new = psutil.net_io_counters()

        upload = (new.bytes_sent - old.bytes_sent) * 8 / 1_000_000
        download = (new.bytes_recv - old.bytes_recv) * 8 / 1_000_000

        live_speed["upload"] = round(upload, 2)
        live_speed["download"] = round(download, 2)

        old = new


@app.on_event("startup")
def startup():
    thread = threading.Thread(
        target=monitor_network,
        daemon=True
    )
    thread.start()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.get("/live")
async def get_live_speed():
    return live_speed


@app.post("/speedtest")
async def run_speed_test():

    if max_speed["running"]:
        return {"message": "Speed test already running"}

    max_speed.update({
        "download": None,
        "upload": None,
        "ping": None,
        "running": True,
        "error": None,
    })

    def worker():
        try:
            st = speedtest.Speedtest(timeout=10, secure=True)
            st.get_closest_servers(limit=3)
            st.get_best_server()

            ping = (
                round(st.results.ping, 2)
                if (
                    st.results.ping is not None
                    and math.isfinite(st.results.ping)
                    and st.results.ping < 10_000
                )
                else None
            )

            download = st.download() / 1_000_000
            if (
                not math.isfinite(download)
                or download <= 0
                or st.results.bytes_received == 0
            ):
                raise RuntimeError("Ookla download test received no data")

            upload = st.upload() / 1_000_000
            if (
                not math.isfinite(upload)
                or upload <= 0
                or st.results.bytes_sent == 0
            ):
                raise RuntimeError("Ookla upload test sent no data")

            max_speed.update(
                download=round(download, 2),
                upload=round(upload, 2),
                ping=ping,
                error=None,
            )

        except Exception as e:
            logger.exception("Ookla speed test failed")
            max_speed.update(
                download=None,
                upload=None,
                ping=None,
                error=str(e) or "Ookla servers could not be reached. Check network or firewall access.",
            )
        finally:
            max_speed["running"] = False

    threading.Thread(
        target=worker,
        daemon=True
    ).start()

    return {"message": "started"}


@app.get("/speedtest-result")
async def get_test_result():
    return max_speed