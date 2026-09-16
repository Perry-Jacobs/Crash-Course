from dataclasses import dataclass


@dataclass
class Poll:
    id: int
    question: str


@dataclass
class Option:
    id: int
    poll_id: int
    text: str
    vote_count: int
