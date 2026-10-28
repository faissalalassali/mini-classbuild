from pydantic import BaseModel, Field
from typing import List

class Question(BaseModel):
    question: str = Field(description="The multiple-choice question")
    options: List[str] = Field(description="Exactly 4 distinct options", min_length=4, max_length=4)
    correct_answer: int = Field(description="The index of the correct answer (0, 1, 2, or 3)", ge=0, le=3)
    explanation: str = Field(description="Explanation of why the answer is correct")

class Quiz(BaseModel):
    lesson_number: int = Field(description="The number of the lesson this quiz belongs to")
    lesson_title: str = Field(description="The title of the lesson")
    questions: List[Question] = Field(description="Exactly 5 questions", min_length=5, max_length=5)