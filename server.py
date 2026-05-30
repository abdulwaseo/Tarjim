"""
server.py
=========
FastAPI backend for the Arabic → English Real-Time Voice Translation web app.
"""
from __future__ import annotations
import asyncio
import logging
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, WebSocket as FastAPIWebSocket
from fastapi.responses import FileResponse, JSONResponse
from starlette.websockets import WebSocketDisconnect
import websockets

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("tarjim")

try:
    from dotenv import load_dotenv
    load_dotenv()
    log.info("Loaded .env file (python-dotenv present).")
except ImportError:
    log.info("python-dotenv not installed — using shell environment only.")

DEEPGRAM_API_KEY: str = os.getenv("DEEPGRAM_API_KEY", "").strip()
if not DEEPGRAM_API_KEY:
    log.error("DEEPGRAM_API_KEY is not set! Export it before starting.")
else:
    masked = DEEPGRAM_API_KEY[:6] + "…" + DEEPGRAM_API_KEY[-4:]
    log.info("DEEPGRAM_API_KEY loaded: %s (length=%d)", masked, len(DEEPGRAM_API_KEY))

BASE_DIR = Path(__file__).parent

app = FastAPI(
    title="Arabic ↔ English Voice Translator",
    version="1.2.0",
)


@app.get("/", response_class=FileResponse, include_in_schema=False)
async def serve_frontend() -> FileResponse:
    html_path = BASE_DIR / "main.html"
    if not html_path.exists():
        raise HTTPException(status_code=404, detail="main.html not found beside server.py")
    return FileResponse(str(html_path))


@app.get("/api/authenticate")
async def authenticate() -> JSONResponse:
    if not DEEPGRAM_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="DEEPGRAM_API_KEY is not set on the server.",
        )
    log.info("Returning API key directly as WS token (Voice Agent auth).")
    return JSONResponse({"token": DEEPGRAM_API_KEY})


@app.get("/health", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok", "api_key_set": bool(DEEPGRAM_API_KEY)})


@app.websocket("/ws/agent")
async def proxy_agent(client_ws: FastAPIWebSocket):
    """Proxy WebSocket connections to Deepgram Voice Agent API.
    This avoids browser CORS/subprotocol issues by routing through the server.
    """
    await client_ws.accept()
    log.info("Client connected to /ws/agent — opening Deepgram proxy connection.")

    if not DEEPGRAM_API_KEY:
        await client_ws.close(code=1008, reason="No API key configured")
        return

    dg_url = "wss://agent.deepgram.com/v1/agent/converse"

    try:
        async with websockets.connect(
            dg_url,
            additional_headers={"Authorization": f"Token {DEEPGRAM_API_KEY}"},
        ) as dg_ws:
            log.info("Deepgram proxy connection established.")

            async def client_to_dg():
                try:
                    while True:
                        msg = await client_ws.receive()
                        if "bytes" in msg and msg["bytes"]:
                            await dg_ws.send(msg["bytes"])
                        elif "text" in msg and msg["text"]:
                            await dg_ws.send(msg["text"])
                except WebSocketDisconnect:
                    log.info("Client disconnected.")
                    await dg_ws.close()
                except Exception as e:
                    log.warning("client_to_dg error: %s", e)

            async def dg_to_client():
                try:
                    async for msg in dg_ws:
                        if isinstance(msg, bytes):
                            await client_ws.send_bytes(msg)
                        else:
                            log.info("Deepgram event: %s", msg[:120])
                            await client_ws.send_text(msg)
                except Exception as e:
                    log.warning("dg_to_client error: %s", e)

            await asyncio.gather(client_to_dg(), dg_to_client())

    except Exception as e:
        log.error("Failed to connect to Deepgram: %s", e)
        await client_ws.close(code=1011, reason=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)