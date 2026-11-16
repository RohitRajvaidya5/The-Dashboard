import time
import psutil
import uvicorn


def run_server() -> None:
    uvicorn.run("internetspeedproject.app:app", host="127.0.0.1", port=8000, reload=True)


def run_monitor() -> None:
    old = psutil.net_io_counters()

    while True:
        time.sleep(1)
        new = psutil.net_io_counters()

        sent = (new.bytes_sent - old.bytes_sent) * 8 / 1_000_000
        recv = (new.bytes_recv - old.bytes_recv) * 8 / 1_000_000

        print(
            f"\r↑ {sent:.2f} Mbps | ↓ {recv:.2f} Mbps",
            end="",
            flush=True,
        )

        old = new


if __name__ == "__main__":
    run_monitor()
