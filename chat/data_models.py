from dataclasses import dataclass


@dataclass
class ChatData:
    MESSAGE = "message"
    FILE = "file"
    LEAVE = "leave"
    ADD = "add"

    room_id: int | None
    user_ids: list[int] | None
    name: str | None
    text: str
    type: str
