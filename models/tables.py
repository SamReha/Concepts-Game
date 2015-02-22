# -*- coding: utf-8 -*-
from datetime import datetime

# The player tables collects all the information relating to a particular player, including stats.
# To find videos associated with a particular player, query the "videos" table with the player's ID.
# caretakeID is the unique account ID of the caretake associated with a particular player.
db.define_table('player',
                Field('caretakerID'),
                Field('name'),
                Field('lastTimePlayed', 'datetime'),
                Field('gamesPlayed'), # The number of games played
                Field('percentCorrect'),
                Field('totalTimePlayed'),
               )

# Each entry in the videos table is a youtube link and a reference to the player that owns the video.
db.define_table('videos',
                Field('playerID'),
                Field('link'),
               )

# Each entry in the problem table is a collection of information describing a particular problem.
db.define_table('problem',
                Field('problemType'), # "size", "fullness", "color", etc.
                Field('complexity'), # "2", "3", etc. Number of objects to compare
                Field('images'), # The set of images used in the problem. Placeholder.
               )

# Use this method to guarantee the currently logged-in user is the caretaker of the player in question. If not, redirects user to index.
def verifiyCaretaker(caretakerID, playerID):
    pID = long(playerID)
    player = db(db.player.id==pID).select().first()
    if long(player.caretakerID) != caretakerID:
        redirect(URL('default', 'index'))
        session.flash=T("You cannot view players that you don't manage!")
