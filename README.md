# SpotifyMonthlyPlaylists
Automatically add newly saved songs to a monthly playlist using Spotify's API.


## Usage

To get started, first create an app on https://developers.spotify.com/. Be sure to set a Redirect URI in app's settings.

Install spotipy using pip.

```bash
pip install spotipy
```

or using
```bash
pip install -r requirements.txt
```

### Basic Example

```python
from monthlyplaylists import MonthlyPlaylists

spotify = MonthlyPlaylists(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    redirect_uri='http://localhost:8888/callback'
)
spotify.update_monthly_playlists()
```

Calling update_monthly_playlists() checks for liked songs after a certain date and adds them to a playlist corresponding to the date the song was liked.

By default, only songs liked after the first of the month are added, and playlists are named using the current month's abbreviation and last 2 
digits of the current year (ex: Jan 22).

After a newly liked song is found and added to a playlist the program will only add songs which are liked after. This allows for songs to be removed from a monthly playlist without the program constantly adding them back.

### Another Example

```python
from monthlyplaylists import MonthlyPlaylists
from datetime import datetime, timedelta

one_yr_ago = datetime.now() - timedelta(days=365)
spotify = MonthlyPlaylists(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    redirect_uri='http://localhost:8888/callback',
    date=one_yr_ago,
    name_format="%B '%y"
)
spotify.update_monthly_playlists()
```

This example will add every liked song from the last year into a monthly playlist using a different naming format (ex: January '22).