import requests
import toolz
import networkx as nx
from collections import deque
from secret import client_secret

API_URL = 'https://api.spotify.com/v1'
AUTH_URL = 'https://accounts.spotify.com/api/token'
CLIENT_ID = 'e7a111ec03b94df2924cdcabe28b4bf5'

KANYE_WEST = '5K4W6rqBFWDnAN6FQUkS6x'
KEVIN_ABSTRACT = '07EcmJpfAday8xGkslfanE'
JAY_Z = '37i9dQZF1DZ06evO1XGbvi'

def authorization_header():
	response = requests.post(
		AUTH_URL,
		data={
			'grant_type': 'client_credentials',
			'client_id': CLIENT_ID,
			'client_secret': client_secret
		}
	).json()

	access_token = response['access_token']
	return {'Authorization': 'Bearer ' + access_token}

def get(url, params={}):
	return requests.get(
    url,
    headers=authorization_header(),
    params=params
  ).json()

def get_artist(id):
	url = API_URL + '/artists/' + id
	return get(url)

def get_album(id):
	url = API_URL + '/albums/' + id
	return get(url)

def get_artists_albums(id):
	url = API_URL + '/artists/' + id + '/albums'
	response = get(url)
	if 'items' in response:
		return response['items']
	else:
		return []

def search(query, type):
  url = API_URL + '/search'
  params = {
    "q": query,
    "type": type
  }
  response = get(url, params)
  return response

def query(query, type, limit=10):
  search_response = search(query, type)
  items = search_response[type + 's']['items']
  # TODO: make this a func
  extractFields = lambda item: {
    "name": item['name'],
    "id": item['id']
  }
  return list(map(extractFields, items))[:limit]

id = lambda item: item['id']

# G = nx.Graph()

# artist1 = KANYE_WEST
# artist2 = KEVIN_ABSTRACT

# queue = deque([artist1])

# visited = []

# while len(queue) > 0:
# 	artist_id = queue.popleft()
# 	artists_albums = get_artists_albums(artist_id)
# 	album_ids = map(id, artists_albums)

# 	visited.append(artist_id)

# 	artist = get_artist(artist_id)
# 	if 'name' in artist:
# 		print artist['name']

# 	# TODO: create weighted edges based on number of features
# 	for album in map(get_album, album_ids):
# 		if 'tracks' not in album:
# 			continue
# 		for track in album['tracks']['items']:
# 			for artist in track['artists']:
# 				featuring_artist_id = artist['id']
# 				if featuring_artist_id not in visited and featuring_artist_id not in queue:
# 					G.add_edge(artist_id, artist['id'])
# 					queue.append(featuring_artist_id)