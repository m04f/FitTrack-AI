from django.contrib.auth.models import User
from openai import OpenAI
import os

from knowledge.models import Article
from userinfo.models import UserEquipment, UserInfo
from workout.serializers import Exercise

from .models import ChatSession, Message
from .tools import availableTools, call_tool


client = OpenAI(
    api_key=os.environ.get('API_KEY'),
    base_url=os.environ.get('OPENAI_BASE_URL')
)


def sys_prompt():
    if sys_prompt.cache:
        return sys_prompt.cache
    available_exercises = '\n'.join(
        [f'{exercise.name}: {exercise.description}'
        for exercise in Exercise.objects.all()])
    articles_text = '\n'.join(
        [(f'{article.name}:'
         f'```markdown'
         f'{article.content}'
         f'```')
        for article in Article.objects.all()])
    sys_prompt.cache = {
        'role': 'system',
        'content':
            available_exercises +
            articles_text +
            'You are an AI personal trainer.'
            'Your goal is to help users achieve their fitness goals by providing personalized workout and nutrition advice.'
            'You should do one of the following:'
            '- Give nutrition advice according to the user\'s dietary needs.'
            '  The nutrition advice should be send to the user (no tool calls needed)'
            '- Create a new workout based on user information.'
    }
    return sys_prompt.cache

sys_prompt.cache = None

def get_user_info(session_uuid):
    session = ChatSession.objects.get(uuid=session_uuid)
    user = session.user
    user_info = UserInfo.objects.get(user=user)
    equipments = []
    for equipment in UserEquipment.objects.filter(user=user).select_related('equipment'):
        equipments.append(equipment.equipment.name)
    return {
        'role': 'system',
        'content': f'''
    User Information:
    -----------------
    Full Name: {user.first_name} {user.last_name}
    Bio: {user_info.bio}
    Age: {user_info.age}
    Height: {user_info.height} cm
    Weight: {user_info.weight} kg
    Gender: {user_info.gender}
    BMI: {user_info.bmi}
    Fitness Level: {user_info.fitness_level}
    Fitness Goal: {user_info.fitness_goal}
    Equipments: {', '.join(equipments)}
    '''
    }

class ChatBot:
    def __init__(self, uuid, request):
        self.uuid = uuid
        self.client = client
        self.request = request

    def send_message(self, msgs: list[Message]):
            chat_msgs = [
                sys_prompt(),
                get_user_info(self.uuid),
            ]
            for msg in msgs:
                chat_msgs.append({'role': msg.role, 'content': msg.content})
            response = self.client.chat.completions.create(
                model=os.environ.get('LLM_MODEL'),
                messages=chat_msgs,
                tools=availableTools,
            )
            tool_calls = response.choices[0].message.tool_calls
            if tool_calls:
                chat_msgs.append(response.choices[0].message)
                for tool in tool_calls:
                    chat_msgs.append({
                    'role': 'tool',
                    'tool_call_id': tool.id,
                    'content': str(call_tool(tool, self.request))
                    })
                    response = self.client.chat.completions.create(
                        model=os.environ.get('LLM_MODEL'),
                        messages=chat_msgs,
                    )

            msg = response.choices[0].message
            return [Message(session_id=self.uuid, content=msg.content, role=msg.role)]
