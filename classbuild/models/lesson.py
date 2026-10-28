from pydantic import BaseModel, Field
from typing import List

class LessonSection(BaseModel):
    heading: str = Field(description="The heading of the section")
    explanation: str = Field(description="The detailed explanation of the concept")
    example: str = Field(description="A practical example or code snippet")

class Exercise(BaseModel):
    question: str = Field(description="The exercise task or question")
    hint: str = Field(description="A helpful hint for solving the exercise")

class LessonContent(BaseModel):
    lesson_number: int = Field(description="The number of the lesson")
    title: str = Field(description="The title of the lesson")
    introduction: str = Field(description="A brief introduction to the lesson")
    sections: List[LessonSection] = Field(description="2 to 4 teaching sections", min_length=2, max_length=4)
    summary: str = Field(description="A brief summary of what was learned")
    exercises: List[Exercise] = Field(description="Exactly 2 practical exercises", min_length=2, max_length=2)