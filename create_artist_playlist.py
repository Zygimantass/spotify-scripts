"""
file: create_artist_playlist.py
description: gets users' followed playlists, then filters songs by artist, and curates a playlist
author: Zygimantass
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import config
import spotipy
import spotipy.util
import sys

def filterByArtist(spTracks, artist):
    tracks = []
    for track in spTracks['items']:
        track = track['track']
        artists = [spArtist['name'] for spArtist in track['artists']]
        if artist in artists:
            if not track in tracks:
                tracks.append(track)
    return tracks

artist = raw_input("Please enter your artists' exact name: ")
curatedPlaylistName = raw_input("Please enter curated playlists' name: ")
publicPlaylist = False if raw_input("Do you want the curated playlist to be public (y/n, default: y): ").lower() \
                   == 'n' else True
onlyOwnPlaylists = False if raw_input("Do you want to filter songs only from your playlists (y/n, default y): ").lower() \
                   == 'n' else True

token = spotipy.util.prompt_for_user_token(config.SPOTIFY_USERNAME, config.SPOTIFY_SCOPE, config.SPOTIFY_CLIENT_ID,
                                           config.SPOTIFY_CLIENT_SECRET, config.SPOTIFY_REDIRECT_URI)
sp = spotipy.Spotify(auth=token)

playlists = sp.user_playlists(config.SPOTIFY_USERNAME)
artist_tracks = []

for playlist in playlists['items']:
    playlistOwner = playlist['owner']['id']
    if onlyOwnPlaylists:
        if playlistOwner != config.SPOTIFY_USERNAME:
            continue

    spPlaylist = sp.user_playlist(playlistOwner, playlist['id'], fields="tracks,next")
    tracks = []
    spTracks = spPlaylist['tracks']
    tracks += filterByArtist(spTracks, artist)
    while spTracks['next']:
        spTracks = sp.next(spTracks)
        tracks += filterByArtist(spTracks, artist)
    artist_tracks += tracks

unique_artist_tracks = []

for track in artist_tracks:
    if track not in unique_artist_tracks and track["id"]:
        unique_artist_tracks.append(track)

curated_playlist_id = sp.user_playlist_create(config.SPOTIFY_USERNAME, curatedPlaylistName, publicPlaylist)['id']

sp.user_playlist_add_tracks(config.SPOTIFY_USERNAME, curated_playlist_id, [track['id'] for track in unique_artist_tracks])

print "Added tracks: " + ", ".join([track["name"] for track in unique_artist_tracks])