from abc import ABC, abstractmethod
from typing import List, Dict


class Message(ABC):
    @abstractmethod
    def to_json(self):
        raise NotImplementedError


class ScalerMessage(Message):
    """Request"""

    """name of the project"""
    projectName: str
    """upload scalers"""
    scalers: List[str]
    """current trailId"""
    trialName: str

    def __init__(self, projectName: str, scalers: List[str], trialName: str) -> None:
        self.projectName = projectName
        self.scalers = scalers
        self.trialName = trialName

    def to_json(self):
        return self.__dict__
