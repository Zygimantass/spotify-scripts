"""
file: get_spotify_token.py
description: gets users' Spotify access token
author: Zygimantass
"""

import config
import spotipy.util
import re

token = spotipy.util.prompt_for_user_token(config.SPOTIFY_USERNAME, config.SPOTIFY_SCOPE, config.SPOTIFY_CLIENT_ID, config.SPOTIFY_CLIENT_SECRET, config.SPOTIFY_REDIRECT_URI)

print "Your token is: " + token