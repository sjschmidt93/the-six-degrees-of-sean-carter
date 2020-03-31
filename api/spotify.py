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

flatten = lambda l: [item for sublist in l for item in sublist]

def flat_map(function, iterable):
	return flatten(map(function, iterable))

def unique_list(l):
	return list(set(l))

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

def artist(artist_id):
	url = f'{API_URL}/artists/{artist_id}'
	return get(url)

def album(album_id):
	url = f'{API_URL}/albums/{album_id}'
	return get(url)

def albums_tracks(album_id):
	url = f'{API_URL}/albums/{album_id}/tracks'
	return get(url)

def artists_albums(artist_id):
	url = f'{API_URL}/artists/{artist_id}/albums'
	return get(url)

def track(track_id):
	url = f'{API_URL}/tracks/{track_id}'
	return get(url)

# returns array of all ids for artists 1 degree 
# of separation from artist corresponding to artist_id
def related_artists_ids(artist_id):
	albums_response = artists_albums(artist_id)
	album_ids = extract_field(albums_response)
	track_responses = map(albums_tracks, album_ids)
	tracks = flat_map(lambda track_response: track_response['items'], track_responses)
	artist_objs = flat_map(lambda track: track['artists'], tracks)
	artist_ids = list(map(lambda artist: artist['id'], artist_objs))
	return filter(lambda id: id != artist_id, artist_ids)
	

def search(query, type):
  url = API_URL + '/search'
  params = {
    'q': query,
    'type': type
  }
  response = get(url, params)
  return response

# TODO: make extract_fields which takes field as an array
def extract_field(response, field='id'):
	items = response['items']
	return list(map(lambda item: item[field], items))

###

def search_query(query, type, limit=10):
  search_response = search(query, type)
  items = search_response[type + 's']['items']
  # TODO: make this a func
  extractFields = lambda item: {
    'name': item['name'],
    'id': item['id']
  }
  return list(map(extractFields, items))[:limit]

print(related_artists_ids(KANYE_WEST))

	# G = nx.Graph()

	# queue = deque([(id, 0)])
	# visited = []

	# while len(queue) > 0:
	# 	(artist_id, dist) = queue.popleft()
	# 	artist_albums = artists_albums(artist_id)
	# 	album_ids = map(lambda item: item['id'], artist_albums)

	# 	visited.append(artist_id)

	# 	artist = artists(artist_id)
	# 	if 'name' in artist:
	# 		print(artist['name'])

	# 	# TODO: create weighted edges based on number of features
	# 	for album in map(albums, album_ids):
	# 		if 'tracks' not in album:
	# 			continue
	# 		for track in album['tracks']['items']:
	# 			for artist in track['artists']:
	# 				featuring_artist_id = artist['id']
	# 				if featuring_artist_id not in visited and featuring_artist_id not in queue and dist < degrees:
	# 					G.add_edge(artist_id, artist['id'])
	# 					queue.append((featuring_artist_id, dist + 1))

#related_artists(KANYE_WEST, 1)
#print(albums_tracks('7fJJK56U9fHixgO0HQkhtI'))