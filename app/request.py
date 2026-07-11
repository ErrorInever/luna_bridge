import requests

requests.post(
    "http://127.0.0.1:8000/ingest",
    json={"text": "地味な作業が好きな私としては収穫の手伝いは面倒なことでも何でもないのだ。思い出したように何度も感謝の言葉を掛けられる方が心苦しい。"
                  "", "source": "luna"}
)