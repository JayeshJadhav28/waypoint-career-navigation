from pydantic import BaseModel, Field
from typing import List


class CareerRecommendation(BaseModel):
    career: str
    suitability_score: int = Field(ge=0, le=100)
    reason: str


class LearningResource(BaseModel):
    resource: str
    type: str


class RoadmapStep(BaseModel):
    step: str
    time_required: str


class CareerAdvice(BaseModel):
    recommended_careers: List[CareerRecommendation]
    skills_to_learn: List[str]
    recommended_certifications: List[str]
    learning_resources: List[LearningResource]
    roadmap: List[RoadmapStep]
    estimated_transition_time: str