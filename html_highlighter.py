from PyQt5.QtCore import Qt, QRegularExpression
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QSyntaxHighlighter, QFont

class HtmlHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)

        tagFormat = QTextCharFormat()
        tagFormat.setForeground(Qt.darkBlue)
        tagFormat.setFontWeight(QFont.Bold)

        self.highlightingRules = [
            (QRegularExpression(r'&[a-zA-Z0-9]+;'), tagFormat),  # HTML entities
            (QRegularExpression(r'<\s*\b[a-zA-Z0-9_]+\b>'), tagFormat),  # Opening tags
            (QRegularExpression(r'</\s*\b[a-zA-Z0-9_]+\b\s*>'), tagFormat),  # Closing tags
        ]

        attributeFormat = QTextCharFormat()
        attributeFormat.setForeground(Qt.darkCyan)
        self.highlightingRules.append((QRegularExpression(r'\b[a-zA-Z0-9_]+\s*='), attributeFormat))

        valueFormat = QTextCharFormat()
        valueFormat.setForeground(Qt.darkGreen)
        self.highlightingRules.append((QRegularExpression(r'".*?"'), valueFormat))
        self.highlightingRules.append((QRegularExpression(r"'.*?'"), valueFormat))

        commentFormat = QTextCharFormat()
        commentFormat.setForeground(Qt.gray)
        self.highlightingRules.append((QRegularExpression(r'<!--.*?-->'), commentFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegularExpression(pattern)
            match = expression.match(text)
            while match.hasMatch():
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, format)
                match = expression.match(text, start + length)
