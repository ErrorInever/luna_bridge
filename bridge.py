import asyncio
import websockets
import requests
import json

LUNA_WS = "ws://127.0.0.1:9001/api/ws/text/origin"
INGEST_URL = "http://127.0.0.1:8000/ingest"


async def run():
    while True:   # 🔥 RETRY LOOP (вот он)
        try:
            print("🔌 connecting to Luna...")

            async with websockets.connect(LUNA_WS) as ws:
                print("✅ connected to Luna")

                while True:
                    msg = await ws.recv()

                    try:
                        data = json.loads(msg)
                        text = data.get("text", msg)
                    except:
                        text = msg

                    try:
                        requests.post(INGEST_URL, json={
                            "text": text,
                            "source": "luna"
                        })
                    except:
                        pass

                    print("ORIGIN:", text)

        except Exception as e:
            print("❌ Luna not ready, retrying...", e)
            await asyncio.sleep(2)