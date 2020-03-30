from flask import Flask
from flask_cors import CORS
import spotify

application = Flask(__name__)
# TODO: is this secure?
CORS(application)

@application.route('/search/<query>/')
def search(query):
  return { "artists": spotify.query(query, "artist") }

application.run(debug=True)