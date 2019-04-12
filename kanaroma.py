# -*- coding: utf-8 -*-

import re
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QGridLayout, QWidget
from PyQt5.QtCore import Qt


class kanaTORomaji(QMainWindow):
	katakanaSet = u"ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶ"
	hiraganaSet = u"ああいいううええおおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖ"
	#               ぁあぃいぅうぇえぉお
	
	katakanaSet = [ord(char) for char in katakanaSet]
	hiraganaSet = [ord(char) for char in hiraganaSet]
	
	kataTOhiraTable = dict(zip(katakanaSet, hiraganaSet))

	
	hiraGeneral = u"あいうえおかがきぎくぐけげこごさざしじすずせぜそぞただちぢつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもやゆよらりるれろわをん"
	hiraGeneral = [ord(char) for char in hiraGeneral]
	romajiTable = [u"a", u"i", u"u", u"e", u"o", u"ka", u"ga", u"ki", u"gi", u"ku", u"gu", u"ke", u"ge", u"ko", u"go",
	               u"sa", u"za", u"shi", u"ji", u"su", u"zu", u"se", u"ze", u"so", u"zo", u"ta", u"da", u"chi", u"dji",
	               u"tsu", u"dzu", u"te", u"de", u"to", u"do", u"na", u"ni", u"nu", u"ne", u"no", u"ha", u"ba", u"pa",
	               u"hi", u"bi", u"pi", u"fu", u"bu", u"pu", u"he", u"be", u"pe", u"ho", u"bo", u"po", u"ma", u"mi",
	               u"mu", u"me", u"mo", u"ya", u"yu", u"yo", u"ra", u"ri", u"ru", u"re", u"ro", u"wa", u"wo", u"n"]
	hiraTORomajiTable = dict(zip(hiraGeneral, romajiTable))
	
	def kanaTORomaji(self, kanaBox, romajiBox):
		"""

		:param kanaBox: the box on the left, which takes kana input
		:param romajiBox: gives romaji translation
		:return: none
		"""
		newText = str(kanaBox.toPlainText().translate(self.kataTOhiraTable))
		newText = str(newText.translate(self.hiraTORomajiTable))
		newText = re.sub(r'(?<=j)iゃ', "a", newText)
		newText = re.sub(r'(?<=j)iゅ', "u", newText)
		newText = re.sub(r'(?<=j)iょ', "o", newText)
		newText = re.sub(r'(?<=sh|ch)iゃ', "a", newText)
		newText = re.sub(r'(?<=sh|ch)iゅ', "u", newText)
		newText = re.sub(r'(?<=sh|ch)iょ', "o", newText)
		newText = re.sub(r'iゃ', "ya", newText)
		newText = re.sub(r'iゅ', "yu", newText)
		newText = re.sub(r'iょ', "yo", newText)
		newText = self.handleSmallTsu(newText)
		newText = self.handleBar(newText)
		
		romajiBox.setText(newText)
	
	def __init__(self):
		super().__init__()
		
		self.initUI()
	
	# noinspection PyUnresolvedReferences
	def initUI(self):
		"""initilizes user interface"""
		
		# the text box on the left
		kanaBox = QTextEdit()
		
		kanaBox.setFontPointSize(17)
		
		
		# the text box on the rigth
		romajiBox = QTextEdit()
		romajiBox.setFontItalic(True)
		romajiBox.setReadOnly(True)
		romajiBox.setFontItalic(True)
		romajiBox.setTextColor(Qt.gray)
		romajiBox.setFontPointSize(17)
		
		# connect input from left to translater function which also going to set output
		# to the box on the left
		kanaBox.textChanged.connect(lambda: self.kanaTORomaji(kanaBox, romajiBox))
		
		grid = QGridLayout()
		grid.setSpacing(20)
		
		
		grid.addWidget(kanaBox,1,1)
		
		grid.addWidget(romajiBox,1,2)
		
		wid = QWidget(self)
		self.setCentralWidget(wid)

		wid.setLayout(grid)

		
		# Set window background color
		self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.gray)
		self.setPalette(p)
		
		# set main window attributes
		self.statusBar()
		self.setGeometry(100, 100, 1080, 500)
		self.setWindowTitle('kanaTOromaji GUI')
		self.setStatusTip("enter kana to left, romaji will appear on the right")
		self.show()
	
	def handleSmallTsu(self, text: str):
		"""
			input: str
			output: str, all small tsu's replaced
			handles small tsu, replaces it with the next character
		"""
		listText = list(text)
		i = 0
		while i < len(listText) - 1:
			if (listText[i] == u"っ"):
				listText[i] = listText[i + 1]
			i += 1
		return "".join(listText)
	
	def handleBar(self, text: str):
		"""
		:param text: text that potetially contains 'ー'
		:return:  text, 'ー' replaced with it's preceeding syllable
		"""
		listText = list(text)
		i = 1
		while i < len(listText):
			if (listText[i] == u"ー"):
				listText[i] = listText[i - 1]
			i += 1
		return "".join(listText)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = kanaTORomaji()
	sys.exit(app.exec_())
