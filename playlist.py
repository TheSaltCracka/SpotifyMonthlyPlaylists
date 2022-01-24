from typing import Optional, List
from spotipy import Spotify

from song import Song


class Playlist:
    """Stores relevant data and methods for a playlist retrieved from spotify's API.

    :param sp: Spotipy client object.
    :param playlist: Dictionary containing playlist data from Spotipy.
    """
    songs: Optional[List[Song]]
    id: str
    name: str
    sp: Spotify

    def __init__(self, sp: Spotify, playlist: dict) -> None:
        self.sp = sp
        self.name = playlist['name']
        self.id = playlist['id']
        self.songs = None

    def add_song(self, song: Song):
        """Adds a song to the playlist."""

        if not self.songs:
            if not self.__fetch_songs():
                print('error when loading songs in playlist')
                return
        if not self.__song_in(song):
            print(song.name, 'added to', self.name)
            self.sp.playlist_add_items(self.id, [song.id])
        else:
            print(song.name, 'already in', self.name)

    def __song_in(self, song: Song) -> bool:
        """Checks if a song is already in the playlist.

        :param song: The song to check for.
        :return: True for song in playlist, False otherwise.
        """

        return any(x.id == song.id for x in self.songs)

    def __fetch_songs(self) -> bool:
        """Retrieves and stores the playlist's songs using spotify's api.

        :return: True for success, False otherwise.
        """

        try:
            results = self.sp.playlist_items(playlist_id=self.id, additional_types=('track',))
        except Exception as e:
            print(repr(e))
            return False
        if 'items' not in results:
            return False
        self.songs = [Song(x) for x in results['items']]
        return True
