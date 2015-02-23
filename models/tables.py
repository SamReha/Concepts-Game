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
TYPES = ['size', 'fullness', 'color', 'distance', 'longer', 'number', 'quantity']
db.define_table('problems',
                Field('problemType'),
                Field('problemMessage', requires=IS_NOT_EMPTY()),     # The text prompt at the head of each problem, eg "Please choose the larger object"
                Field('complexity', requires=IS_INT_IN_RANGE(0, 20)), # Number of objects to compare
               )
db.problems.problemType.requires = IS_IN_SET(TYPES)

# Each problem image represents a single image associated with a particular problem.
# Each problemImage is tagged as either being a correct or incorrect answer.
# IT IS IMPORTANT THAT EVERY IMAGE SET CONTAIN AT LEAST 1 CORRECT ANSWER, EVEN THOUGH THE SCHEMA DOES NOT ENFORCE THIS.
# An image set is constructed by querying problemImages for a particular problem ID.
db.define_table('problemImages',
                Field('problemID'),
                Field('image', 'upload'),
                Field('correctAnswer', 'boolean'),
               )

# Use this method to guarantee the currently logged-in user is the caretaker of the player in question. If not, redirects user to index.
def verifiyCaretaker(caretakerID, playerID):
    pID = long(playerID)
    player = db(db.player.id==pID).select().first()
    if long(player.caretakerID) != caretakerID:
        redirect(URL('default', 'index'))
        session.flash=T("You cannot view players that you don't manage!")
