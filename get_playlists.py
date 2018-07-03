"""
file: get_playlists.py
description: gets users' followed playlists
author: Zygimantass
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import config
import spotipy
import spotipy.util

token = spotipy.util.prompt_for_user_token(config.SPOTIFY_USERNAME, config.SPOTIFY_SCOPE, config.SPOTIFY_CLIENT_ID, config.SPOTIFY_CLIENT_SECRET, config.SPOTIFY_REDIRECT_URI)
sp = spotipy.Spotify(auth=token)

playlists = sp.user_playlists(config.SPOTIFY_USERNAME)

print "Your followed playlists: \n"

for playlist in playlists['items']:
    playlistOwner = None
    if playlist['owner']['display_name']:
        playlistOwner = playlist['owner']['display_name']
    else:
        playlistOwner = playlist['owner']['id'] if playlist['owner']['id'] != config.SPOTIFY_USERNAME else 'you'

    playlistName = playlist['name']
    formattedName = 'Playlist "{0}" by {1}'.format(playlistName, playlistOwner)
    print formattedName.encode("utf-8")