from datetime import datetime
import json
import os
from openai import OpenAI
from .models import Conversation
from apps.courses.models import Course
from apps.teachers.models import Teacher
from apps.schedules.models import Schedule


class MCPService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def execute_action(self, action_data):
        action_type = action_data.get("action")
        data = action_data.get("data", {})

        if action_type == "create_course":
            return Course.objects.create(**data)
        elif action_type == "update_course":
            course_id = data.pop("id")
            return Course.objects.filter(id=course_id).update(**data)
        elif action_type == "delete_course":
            return Course.objects.filter(id=data["id"]).delete()
        elif action_type == "create_teacher":
            return Teacher.objects.create(**data)
        elif action_type == "create_schedule":
            return Schedule.objects.create(**data)
        else:
            raise ValueError(f"Unknown action type: {action_type}")

    def process_prompt(self, conversation_id):
        conversation = Conversation.objects.get(id=conversation_id)
        conversation.status = "processing"
        conversation.save()

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an AI assistant that processes natural language commands for a course dashboard system. 
                     Parse the user's intent and respond with structured actions in JSON format. Example actions:
                     {"action": "create_course", "data": {"name": "Python 101", "description": "Intro to Python"}}
                     {"action": "update_course", "data": {"id": "123", "name": "Updated Course"}}
                     {"action": "create_teacher", "data": {"name": "John Doe", "email": "john@example.com"}}
                     Always respond with valid JSON that includes 'action' and 'data' fields.""",
                    },
                    {"role": "user", "content": conversation.prompt},
                ],
            )

            ai_response = response.choices[0].message.content
            print(f"AI Response: {ai_response}")
            try:
                action_data = json.loads(ai_response)
                result = self.execute_action(action_data)
                conversation.response = f"Success: {str(result)}"
                conversation.status = "completed"
            except json.JSONDecodeError:
                conversation.error = "Invalid JSON response from AI"
                conversation.status = "failed"
            except Exception as e:
                conversation.error = f"Action execution failed: {str(e)}"
                conversation.status = "failed"

        except Exception as e:
            print(f"Error processing conversation: {str(e)}")
            conversation.error = str(e)
            conversation.status = "failed"

        conversation.processed_at = datetime.now()
        conversation.save()
        return conversation
