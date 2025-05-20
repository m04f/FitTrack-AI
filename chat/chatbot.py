from openai import AsyncOpenAI
import os

from .models import Message
from .tools import call_tool

class ChatBot:
    def __init__(self, uuid):
        self.uuid = uuid
        self.client = client = AsyncOpenAI(
                api_key=os.environ.get('API_KEY'),
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )

    async def send_message(self, msgs: list[Message]):
        chat_msgs = [
            {'role': msg.role, 'content': msg.content}
            for msg in msgs
        ]
        response = await self.client.chat.completions.create(
            model="gemini-2.0-flash",
            messages = chat_msgs,
        )
        msg = response.choices[0].message
        return [Message(session_id=self.uuid, content=msg.content, role=msg.role)]
