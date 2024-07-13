from typing import Optional
from core.models import User, Tweet
from dataclasses import dataclass

@dataclass
class AddCommentDTO:
    author : Optional['User'] 
    content: str
