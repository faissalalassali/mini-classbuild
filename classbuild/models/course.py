from pydantic import BaseModel, Field
from typing import List

class Lesson(BaseModel):
    title: str = Field(description="The title of the lesson")
    objective: str = Field(description="The main objective of this lesson")

class CourseOutline(BaseModel):
    course_title: str = Field(description="The main title of the course")
    difficulty_level: str = Field(description="The difficulty level of the course")
    lessons: List[Lesson] = Field(description="List of lessons in this course")