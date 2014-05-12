#coding: utf-8

# Copyright (C) 2013, 2014 Johan Reitan
#
# This file is part of QtChordii.
#
# QtChordii is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# QtChordii is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with QtChordii.  If not, see <http://www.gnu.org/licenses/>.

import json


class Songbook:
    def __init__(self, name=None):
        self.name = name
        self.songs = []

    def add_song(self, filename):
        self.songs.append(filename)

    def clear(self):
        self.songs.clear()

    def save(self, filename):
        json.dump(self.__dict__, open(filename, 'w'), indent=4)

    def load(self, filename):
        self.__dict__ = json.load(open(filename, 'r'))
