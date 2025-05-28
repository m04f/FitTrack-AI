from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall
import json

from rest_framework.reverse import reverse

from workout.models import Workout, Exercise, WorkoutExercise
from django.db.models import Q

async def create_workout(name: str, description: str, exercises: list[dict]) -> dict:
    """
    Create a workout with the given details.

    Args:
        name (str): The name of the workout.
        description (str): A description of the workout.
        exercises (list): A list of exercises with details (exercise_id, order, reps, duration, etc.).

    Returns:
        dict: A dictionary containing the created workout details or an error message.
    """
    try:
        workout = await Workout.objects.acreate(
            name=name,
            description=description,
        )
        workout_exercises = [
            WorkoutExercise(
                workout=workout,
                exercise_id=exercise['exercise_id'],
                order=exercise['order'],
                reps=exercise.get('reps'),
                duration=exercise.get('duration'),
                weight=exercise.get('weight'),
                sets=exercise.get('sets', 1),
                rest=exercise.get('rest', 120),
                notes=exercise.get('notes', '')
            )
            for exercise in exercises
        ]
        await WorkoutExercise.objects.abulk_create(workout_exercises)
        return {"status": "success", "message": f'Workout added at {reverse("workout-details",kwargs={'pk': workout.uuid})}'}
    except Exception as e:
        return {"status": "error", "message": str(e)}

async def call_tool(tool: ChatCompletionMessageToolCall) -> dict:
    """
    Helper function to call a tool with the provided arguments.

    Args:
        tool (dict): The tool definition containing function metadata.
        available_tools (dict): A dictionary of available tools with their function names as keys.
        **kwargs: Arguments to pass to the tool's function.

    Returns:
        dict: The result of the tool's function execution.
    """
    if tool.function.name == 'create_workout':
        args = json.loads(tool.function.arguments)
        return await create_workout(args['name'], args['description'], args['exercises'])


create_workout_tool = {
    'type': 'function',
    'function': {
        'name': 'create_workout',
        'description': 'Create a workout with specified exercises',
        'parameters': {
            'type': 'object',
            'required': ['name', 'description', 'exercises'],
            'properties': {
                'name': {'type': 'string', 'description': 'The name of the workout'},
                'description': {'type': 'string', 'description': 'A description of the workout'},
                'exercises': {
                    'type': 'array',
                    'description': 'A list of exercise names with details',
                    'items': {
                        'type': 'object',
                        'required': ['exercise_id', 'order'],
                        'properties': {
                            'exercise_id': {'type': 'integer', 'description': 'The ID of the exercise'},
                            'order': {'type': 'integer', 'description': 'The order of the exercise in the workout'},
                            'reps': {'type': 'integer', 'description': 'The number of repetitions', 'nullable': True},
                            'duration': {'type': 'integer', 'description': 'The duration in seconds', 'nullable': True},
                            'weight': {'type': 'integer', 'description': 'The weight in kilograms', 'nullable': True},
                            'sets': {'type': 'integer', 'description': 'The number of sets', 'default': 1},
                            'rest': {'type': 'integer', 'description': 'The rest time in seconds', 'default': 120},
                            'notes': {'type': 'string', 'description': 'Additional notes', 'nullable': True},
                        }
                    }
                }
            }
        }
    }
}

availableTools = [
    create_workout_tool
]
