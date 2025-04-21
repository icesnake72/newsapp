import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

class AudioConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("WebSocket 연결됨")

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            print("음성 데이터 수신:", len(bytes_data), "bytes")
            # 여기서 Whisper나 다른 모델로 처리 가능
            # 결과를 클라이언트로 전송하려면 아래처럼:
            # await self.send(text_data="STT 결과")

    async def disconnect(self, close_code):
        print("WebSocket 연결 해제됨")
