import time
from monthlyplaylists import MonthlyPlaylists

# https://medium.com/@maxtingle/getting-started-with-spotifys-api-spotipy-197c3dc6353b
# You must add a matching redirect URI to your application at My Dashboard
spotify = MonthlyPlaylists(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    redirect_uri='http://localhost:8888/callback'
)

# The class updates its date threshold to whichever song it added last.
# Therefore, calling update_monthly_playlists() multiple times will make minimal api calls
while True:
    spotify.update_monthly_playlists()
    time.sleep(30)
