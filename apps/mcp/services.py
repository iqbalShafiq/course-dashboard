from datetime import datetime
import json
import os
from django.db import connection
from openai import OpenAI
from .models import Conversation, Analysis
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
        elif action_type == "request_info":
            return {"status": "awaiting_input", "question": data["question"]}
        else:
            raise ValueError(f"Unknown action type: {action_type}")

    def execute_query(self, query):
        """Execute a raw SQL query safely and return results"""
        with connection.cursor() as cursor:
            cursor.execute(query)
            if cursor.description:  # If the query returns rows
                columns = [col[0] for col in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            return []

    def get_table_schema(self):
        """Get schema information for relevant tables"""
        tables = {
            "courses": Course._meta.get_fields(),
            "teachers": Teacher._meta.get_fields(),
            "schedules": Schedule._meta.get_fields(),
        }

        schema = {}
        for table, fields in tables.items():
            schema[table] = [
                {
                    "name": field.name,
                    "type": field.get_internal_type(),
                    "null": field.null if hasattr(field, "null") else True,
                }
                for field in fields
            ]
        return schema

    def get_db_context(self):
        """Get comprehensive database context including schema and sample data"""
        context = {}

        # Get table schemas with actual column types
        schema_query = """
            SELECT table_name, column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name IN ('courses_course', 'teachers_teacher', 'schedules_schedule')
        """
        context["schema"] = self.execute_query(schema_query)

        # Get table statistics
        stats_query = """
            SELECT 
                schemaname, 
                relname as table_name, 
                n_live_tup as row_count
            FROM pg_stat_user_tables
            WHERE schemaname = 'public'
            AND relname IN ('courses_course', 'teachers_teacher', 'schedules_schedule')
        """
        context["statistics"] = self.execute_query(stats_query)

        return context

    def get_analysis_data(self, query_type):
        """Get relevant data based on query type"""
        if "enrollment" in query_type.lower():
            return self.execute_query("""
                SELECT c.name as course_name, COUNT(s.id) as enrollment_count 
                FROM courses_course c
                LEFT JOIN schedules_schedule s ON c.id = s.course_id
                GROUP BY c.name
            """)
        elif "teacher" in query_type.lower():
            return self.execute_query("""
                SELECT t.name as teacher_name, COUNT(s.id) as class_count 
                FROM teachers_teacher t
                LEFT JOIN schedules_schedule s ON t.id = s.teacher_id
                GROUP BY t.name
            """)
        elif "schedule" in query_type.lower():
            return self.execute_query("""
                SELECT day_of_week, COUNT(*) as class_count 
                FROM schedules_schedule 
                GROUP BY day_of_week
            """)
        elif "capacity" in query_type.lower():
            return self.execute_query("""
                SELECT name as course_name, capacity, description
                FROM courses_course 
                WHERE capacity >= 5 AND is_active = true
                ORDER BY capacity DESC
            """)
        return []

    def process_prompt(self, conversation_id):
        conversation = Conversation.objects.get(id=conversation_id)
        conversation.status = "processing"
        conversation.save()

        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are an AI assistant that processes natural language commands for a course dashboard system. 
                    If you need more information to process a request, respond with a JSON like:
                    {"action": "request_info", "data": {"question": "What specific information do you need?"}}
                    
                    For other actions, respond with JSON like:
                    {"action": "create_course", "data": {"name": "Python 101", "description": "Intro to Python"}}
                    {"action": "update_course", "data": {"id": "123", "name": "Updated Course"}}
                    {"action": "create_teacher", "data": {"name": "John Doe", "email": "john@example.com"}}""",
                }
            ]

            if conversation.parent:
                messages.append({"role": "user", "content": conversation.parent.prompt})
                messages.append(
                    {"role": "assistant", "content": conversation.parent.response}
                )

            messages.append({"role": "user", "content": conversation.prompt})

            if conversation.context:
                for ctx in conversation.context:
                    messages.append(
                        {"role": "user", "content": f"Additional context: {ctx}"}
                    )

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
            )

            ai_response = response.choices[0].message.content

            try:
                action_data = json.loads(ai_response)
                result = self.execute_action(action_data)

                if (
                    isinstance(result, dict)
                    and result.get("status") == "awaiting_input"
                ):
                    conversation.request_information(result["question"])
                else:
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

    def process_analysis(self, analysis_id):
        """Process an analysis request with database integration"""
        analysis = Analysis.objects.get(id=analysis_id)

        try:
            # Get database context
            db_context = self.get_db_context()

            # Get initial data based on query type
            data = self.get_analysis_data(analysis.query)

            messages = [
                {
                    "role": "system",
                    "content": f"""You are a PostgreSQL data analysis expert with access to a course management database.

Available database context:
Schema: {json.dumps(db_context["schema"], indent=2)}
Statistics: {json.dumps(db_context["statistics"], indent=2)}

You can write custom SQL queries to analyze the data. The main tables are:
- courses_course: Stores course information including name, capacity, description
- teachers_teacher: Contains teacher details
- schedules_schedule: Links courses with teachers and contains scheduling info

Format your response as a JSON object:
{{
    "sql": "your custom SQL query here",
    "data": [numerical_values for visualization],
    "labels": [label_values for visualization],
    "summary": "Text summary of findings",
    "metadata": {{
        "total": sum_of_values,
        "average": average_value,
        "additional_metrics": {{}}
    }}
}}""",
                },
                {
                    "role": "user",
                    "content": f"""Analysis Query: {analysis.query}
Visualization Type: {analysis.visualization_type}
Initial Data Sample: {json.dumps(data, indent=2)}""",
                },
            ]

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
            )

            # Extract the message content from the response
            ai_response = response.choices[0].message.content.strip()

            try:
                result = json.loads(ai_response)

                # If AI provided a custom SQL query, execute it
                if "sql" in result:
                    try:
                        custom_data = self.execute_query(result["sql"])
                        result["raw_data"] = custom_data
                    except Exception as sql_error:
                        print(f"Error executing custom SQL: {str(sql_error)}")
                        result["raw_data"] = data
                else:
                    result["raw_data"] = data

            except json.JSONDecodeError:
                result = {
                    "data": [],
                    "labels": [],
                    "summary": "Failed to parse analysis results",
                    "metadata": {"error": "Invalid JSON response"},
                    "raw_data": data,
                }

            analysis.result = result
            analysis.save()
            return result

        except Exception as e:
            error_result = {
                "data": [],
                "labels": [],
                "summary": f"Error processing analysis: {str(e)}",
                "metadata": {"error": str(e)},
                "raw_data": [],
            }
            analysis.result = error_result
            analysis.save()
            return error_result
