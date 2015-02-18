# -*- coding: utf-8 -*-
from datetime import datetime

db.define_table('player',
                Field('name'),
                Field('videoLinks'), # Video Links are represented as a JSON string list of complete youtube URLs.
                Field('lastTimePlayed', 'datetime'),
                Field('gamesPlayed'), # The number of games played
                Field('percentCorrect'),
                Field('totalTimePlayed'),
               )

db.define_table('problem',
                Field('problemType'), # "size", "fullness", "color", etc.
                Field('complexity'), # "2", "3", etc. Number of objects to compare
                Field('images'), # The set of images used in the problem
               )
