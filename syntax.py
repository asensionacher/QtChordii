# Copyright 2013 Johan Reitan
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

from PyQt4.QtCore import QRegExp
from PyQt4.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter


def font_format(color, style=''):
    """
    Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages
STYLES = {
    'keyword': font_format('olive'),
    'argument': font_format('darkcyan'),
    'curlyBrace': font_format('orange'),
    'chord': font_format('firebrick')
}


class ChordProHighlighter(QSyntaxHighlighter):
    """
    Syntax highlighter for the ChordPro language.
    """
    # ChordPro keywords
    keywords = [
        'new_song', 'ns', 'start_of_chorus', 'soc', 'end_of_chorus', 'eoc', 'start_of_tab', 'sot', 'end_of_tab', 'eot',
        'define', 'no_grid', 'ng', 'grid', 'g', 'new_page', 'np', 'new_physical_page', 'npp', 'column_break', 'colb'
    ]
    argumentKeywords = [
        'title', 't', 'subtitle', 'st', 'comment', 'c', 'comment_italic', 'ci', 'comment_box', 'cb', 'textfont',
        'textsize', 'chordfont', 'chordsize', 'titles', 'columns', 'col', 'pagetype'
    ]
    keywords.extend(argumentKeywords)

    # Braces
    curlyBraces = [
        '\{', '\}',
    ]
    squareBraces = [
        '\[', '\]',
    ]

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        rules = []

        # Rules
        # TODO: make a nice rule for chord definition
        # TODO: make rules for keywords that take special arguments (like numbers)
        rules += [(r'\{%s\:(.)*\}' % w, 0, STYLES['argument']) for w in ChordProHighlighter.argumentKeywords]
        rules += [(r'\{%s\:?' % w, 0, STYLES['keyword']) for w in ChordProHighlighter.keywords]
        rules += [(r'%s' % b, 0, STYLES['curlyBrace']) for b in ChordProHighlighter.curlyBraces]
        rules += [(r'\[[^\]]*\]', 0, STYLES['chord'])]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """
        Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, fmt in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings

    #        in_multiline = self.match_multiline(text, *self.tri_single)
    #        if not in_multiline:
    #            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        # TODO: adapt this for ChordPro blocks (chorus etc.)
        """
        Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = text.length() - start + add
                # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False