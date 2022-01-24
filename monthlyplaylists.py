from datetime import datetime
from typing import Optional, List
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from playlist import Playlist
from song import Song


class MonthlyPlaylists:
    """Fetches and checks playlists against newly saved songs then adds new songs to a monthly playlist.

    :param client_id: Client ID for Spotify API.
    :param client_secret: Client Secret for Spotify API.
    :param redirect_uri: Any valid URI matching the redirect URI in Spotify Developer application (optional).
    :param date: Date to detect newly saved songs after (optional).
    :param name_format: Strftime format string to name monthly playlists (optional).
    :param headless: Allows authenticating Spotify on a headless machine (optional).
    """
    user_id: str
    saved_songs: Optional[List[Song]]
    playlists: Optional[List[Playlist]]
    last_checked: datetime
    name_format: str

    def __init__(self, client_id: str, client_secret: str,
                 redirect_uri: str = 'http://localhost:8888/callback',
                 date: datetime = None, name_format: str = '%b %y', headless: bool = False) -> None:
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope="user-library-read playlist-modify-private playlist-modify-public playlist-read-private",
                open_browser=headless
            )
        )
        self.user_id = self.sp.current_user()['id']
        self.saved_songs = None
        self.playlists = None
        self.last_checked = datetime.today().replace(day=1) if date is None else date
        self.name_format = name_format

    def update_monthly_playlists(self):
        """Performs every step for maintaining monthly playlists."""

        if not self.__fetch_saved_songs():
            print('error when loading saved songs')
            return
        new_songs = self.__fetch_new_saved_songs()
        if not new_songs:
            print('No new songs')
            return
        if not self.__fetch_playlists():
            print('error when loading playlists')
            return
        if not self.__add_songs_to_playlist(new_songs):
            print('error during playlist creation/detection')
            return
        self.last_checked = new_songs[0].added_at

    def __fetch_saved_songs(self) -> bool:
        """Fetches and stores currently saved songs using spotify's api.
        :return: True for success, False otherwise.
        """

        self.saved_songs = None
        try:
            results = self.sp.current_user_saved_tracks(limit=50)
        except Exception as e:
            print(repr(e))
            return False
        if 'items' not in results:
            return False
        tracks = results['items']
        self.saved_songs = [Song(x) for x in tracks]
        return True

    def __fetch_playlists(self) -> bool:
        """Fetches and stores current playlists using spotify's api.
        :return: True for success, False otherwise.
        """

        self.playlists = None
        try:
            results = self.sp.current_user_playlists()
        except Exception as e:
            print(repr(e))
            return False
        if 'items' not in results:
            return False
        playlists = results['items']
        self.playlists = [Playlist(self.sp, x) for x in playlists]
        return True

    def __fetch_new_saved_songs(self):
        """Returns list of songs that were added after the last_date checked."""

        return [song for song in self.saved_songs if song.added_at > self.last_checked]

    def __add_songs_to_playlist(self, songs: List[Song]) -> bool:
        """Adds songs to playlist that is named from the current month and year (Jan 22).

        :param songs: List of songs to add.
        :return: True for success, False otherwise.
        """

        name = songs[0].added_at.strftime(self.name_format)
        existing_playlist = self.__find_playlist(name)
        if existing_playlist is None:
            return False
        for song in songs:
            # Change playlists if a song is liked from a different month than the previous song
            curr_name = song.added_at.strftime(self.name_format)
            if existing_playlist.name != curr_name:
                existing_playlist = self.__find_playlist(curr_name)
            if existing_playlist is None:
                return False
            existing_playlist.add_song(song)
        return True

    def __find_playlist(self, name: str) -> Optional[Playlist]:
        """Returns a playlist matching the given name or creates one.

        :param name: The title of the playlist to search for or create.
        :return: Playlist if successful, None otherwise.
        """

        playlist = next((x for x in self.playlists if x.name == name), None)
        # If playlist does not exist attempt to create it
        if playlist is None:
            try:
                data = self.sp.user_playlist_create(user=self.user_id, name=name)
            except Exception as e:
                print(repr(e))
                return None
            if data.get('type') != 'playlist':
                return None
            playlist = Playlist(sp=self.sp, playlist=data)
            print(playlist.name, 'was created')
        return playlist
