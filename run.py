import multiprocessing
import uvicorn
import requests
import time
import asyncio
import bridge


def run_server():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)


def wait_server():
    for _ in range(20):
        try:
            requests.get("http://127.0.0.1:8000/docs")
            print("✅ server ready")
            return
        except:
            time.sleep(0.5)


def run_bridge():
    asyncio.run(bridge.run())


if __name__ == "__main__":
    server = multiprocessing.Process(target=run_server)
    server.start()

    wait_server()   # 🔥 ВОТ ТУТ

    bridge_proc = multiprocessing.Process(target=run_bridge)
    bridge_proc.start()

    server.join()
    bridge_proc.join()