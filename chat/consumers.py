from channels.generic.websocket import WebsocketConsumer

import json

from .models import Message, ChatSession
from .chatbot import ChatBot


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.bot = None
        self.messages = []
        self.uuid = None

    def connect(self):
        self.uuid = self.scope['url_route']['kwargs']['session']
        self.accept()

        # Check if there are existing messages in the database
        for msg in Message.objects.filter(session_id=self.uuid):
            self.messages.append(msg)

        self.bot = ChatBot(self.uuid)

    def disconnect(self, code):
        pass

    def send_message(self, message: Message):
        self.send(text_data=json.dumps({'message': message.content, 'role': message.role, 'timestamp': str(message.timestamp)}))

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            if text_data_json['message']:
                message = text_data_json['message']
                db_message = Message.objects.create(session_id=self.uuid, role='user', content=message)
                self.messages.append(db_message)
                self.send_message(db_message)

                # Call the chat model
                response = self.bot.send_message(self.messages)
                Message.objects.bulk_create(response)
                self.send_message(response[-1])
