#!/usr/bin/python
# oggname adds vorbis comments to ogg vorbis files
# dependencies:
#   - vorbiscomment
import os
import glob
from sys import exit
from subprocess import call

class Album(object):
	def __init__(self, albumname):
		self.name = albumname

	def __str__(self):
		return self.name

	def get_tracks(self):
		"""Gets the track comments from the user"""
		self.tracks = []

		for filename in sorted(glob.glob("*.ogg")):
			print()
			this_track= Track(filename)
			print(this_track)

			this_track.number = input("What is the track number of this track?\n> ")
			this_track.title  = input("What is the name of this track?\n> ")
			if self.is_multiartist:
				this_track.artist = input("Who is the artist for this track?\n> ")
			else:
				this_track.artist = self.artist

			self.tracks.append(this_track)

	def get_artist(self):
		"""Determines if the album is multiartist.
		If not then it get the album artist
		"""
		self.is_multiartist = \
			input("Is this a multi-artist album? [y/N] ").lower() == "y"
		if not self.is_multiartist:
			self.artist = input("What is the artist's name?\n> ")

class Track(object):
	def __init__(self, filename):
		self.filename = filename

	def __str__(self):
		return self.filename


def confirm_comments(album):
	"""Asks the user to confirm if what the vorbis comments are correct"""
	print("-"*80)
	print("Please confirm that the following is correct.")
	print()
	print("Album:", album.name)
	if not album.is_multiartist:
		print("Artist:", album.artist)

	for track in album.tracks:
		print()
		print("filename:", track.filename)
		print("number:  ", track.number)
		print("title:   ", track.title)
		if album.is_multiartist:
			print("artist   ", track.artist)

	sure = input("Are you sure you want to write these comments? [y/N] ")
	return sure.lower() == "y"

def write_vorbis_comments(album):
	"""Writes vorbis comments to the ogg files"""
	print("Writing comments...")

	for track in album.tracks:
		comment_filename = "%s.comment" % track
		comment_file = open(comment_filename, "w")
		comment_file.write("TRACKNUMBER=%s\n" % track.number)
		comment_file.write("TITLE=%s\n"       % track.title)
		comment_file.write("ARTIST=%s\n"      % track.artist)
		comment_file.write("ALBUM=%s\n"       % album)
		comment_file.close()

		# use vorbiscomment to name the tracks
		call(["vorbiscomment", "-w", "-c", comment_filename, track.filename, "%s.named" % track])
		os.remove(comment_filename)

	print("Done!")


# get the album information
album = Album(input("What is the name of this album?\n> "))
album.get_artist()
album.get_tracks()

if confirm_comments(album):
	write_vorbis_comments(album)
else:
	exit(0)
