from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from environ import environ

SPOTIFY_CLIENT_ID = environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = environ['SPOTIFY_CLIENT_SECRET']
REDIRECT_URI = 'http://example.com'

date = input('Enter date in following formate (YYYY-MM-DD) ex:(2004-04-23):')
os.system('cls' if os.name == 'nt' else 'clear')

response = requests.get(f'https://www.billboard.com/charts/hot-100/{date}/')
soup = BeautifulSoup(response.text, 'html.parser')

song_names_h3 = soup.select('li h3')
songs = [song.text.strip() for song in song_names_h3][:100]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

songs_uri = []
year = date.split('-')[0]
print("Finding songs please wait XD")

for song in songs:
    result = sp.search(q=f"track: {song} year: {year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uri.append(uri)
    except IndexError:
        print(f'We were unable to find ({song})...skipped!')

os.system('cls' if os.name == 'nt' else 'clear')
print(f'Total song found {len(songs_uri)}')

new_playlist = sp.user_playlist_create(
    user='kjs0jalvbdwlezui4u52jue2c',
    name=f'{date} Billboard',
    public=False,
)

sp.playlist_add_items(playlist_id=new_playlist['id'], items=songs_uri)
print(f'{len(songs_uri)} Songs has been added successfully!')
