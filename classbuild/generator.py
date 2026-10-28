import os
import json
from dotenv import load_dotenv
from groq import Groq
from classbuild.models.course import CourseOutline
from classbuild.models.lesson import LessonContent
from classbuild.models.quiz import Quiz

load_dotenv()

def generate_course_outline(topic: str, difficulty: str, lesson_count: int) -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
    
    client = Groq(api_key=api_key)
    schema = CourseOutline.model_json_schema()
    
    prompt = f"""
    Create a course outline about '{topic}' at a '{difficulty}' level with exactly {lesson_count} lessons.
    You must respond ONLY with a valid JSON object matching this schema, with no extra text or markdown code blocks:
    {json.dumps(schema, indent=2)}
    """
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert educational course creator. Always output strictly valid JSON."},
            {"role": "user", "content": prompt}
        ],
        model=model_name,
        temperature=0.7
    )
    
    content = response.choices[0].message.content.strip()
    if content.startswith("```json"):
        content = content[7:-3].strip()
    elif content.startswith("```"):
        content = content[3:-3].strip()
        
    return json.loads(content)

def generate_lesson_content(course_title: str, difficulty: str, lesson_number: int, lesson_title: str) -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
    
    client = Groq(api_key=api_key)
    schema = LessonContent.model_json_schema()
    
    prompt = f"""
    Write the full content for Lesson {lesson_number}: '{lesson_title}' 
    for a '{difficulty}' level course about '{course_title}'.
    You must respond ONLY with a valid JSON object matching this schema, with no extra text or markdown code blocks:
    {json.dumps(schema, indent=2)}
    """
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert educational course creator. Always output strictly valid JSON."},
            {"role": "user", "content": prompt}
        ],
        model=model_name,
        temperature=0.7
    )
    
    content = response.choices[0].message.content.strip()
    if content.startswith("```json"):
        content = content[7:-3].strip()
    elif content.startswith("```"):
        content = content[3:-3].strip()
        
    return json.loads(content)

def generate_quiz(course_title: str, difficulty: str, lesson_number: int, lesson_title: str, lesson_content: str) -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
    
    client = Groq(api_key=api_key)
    schema = Quiz.model_json_schema()
    
    prompt = f"""
    Create a 5-question multiple-choice quiz for Lesson {lesson_number}: '{lesson_title}' 
    of the '{difficulty}' course '{course_title}'.
    Base the questions ONLY on this lesson content:
    {lesson_content}
    
    You must respond ONLY with a valid JSON object matching this schema, with no extra text or markdown code blocks:
    {json.dumps(schema, indent=2)}
    """
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert educational course creator. Always output strictly valid JSON."},
            {"role": "user", "content": prompt}
        ],
        model=model_name,
        temperature=0.7
    )
    
    content = response.choices[0].message.content.strip()
    if content.startswith("```json"):
        content = content[7:-3].strip()
    elif content.startswith("```"):
        content = content[3:-3].strip()
        
    return json.loads(content)