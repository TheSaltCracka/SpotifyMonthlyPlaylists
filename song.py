from datetime import datetime


class Song:
    """Stores relevant data for a song retrieved from spotify's API.

    :param song: Dictionary containing playlist data from spotify's API.
    """
    added_at: datetime
    id: str
    name: str

    def __init__(self, song: dict) -> None:
        self.added_at = datetime.strptime(song['added_at'], "%Y-%m-%dT%H:%M:%SZ")
        self.id = song['track']['id']
        self.name = song['track']['name']
