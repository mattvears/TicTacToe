#!/usr/bin/env python2.5
""" TicTacToe server """
import re
import sys
import soul

sys.path.append('/home/confusio/py_libs/')
import web

from ttt2 import ttt, Game
from board import GameBoard


# REST routing & general web.py setup
urls = ("/(.+)/", "PlayTurn")
app = web.application(urls, locals())
session = web.session.Session(app, web.session.DiskStore('gamedata'))
app_loc = 'http://beta.confusiontechnology.com/TicTacToe/'

class PlayTurn:
	""" Given a valid board, PlayTurn returns a board with the next AI turn taken, and a ttt.Game.Status """
	def GET(self, path=None):
		re1 = '([0-2]{9,9})'
		rg = re.compile(re1,re.IGNORECASE|re.DOTALL)
		
		if path is not None and rg.search(path):
			board = [int(pos) for pos in path]	
			
			gamestate = ttt.CheckBoard(board)
			if gamestate is Game.KeepPlaying:
				board = ttt.GetNextAIMove(board)
				gamestate = ttt.CheckBoard(board)

				if gamestate > 0:
					gb = ttt.ListToGameBoard(board)
					gb = GameBoard.MarkEndPath(gb)
					board = ttt.GameBoardToList(gb)
						
			
			# diy jsonp....
			qs = web.input()
			bstr = ''.join(["%s" % i for i in board])
			return str(qs.callback) + "({'r':'" + str(gamestate) + "','b':'" + bstr + "'})"


if __name__ == "__main__":
	    app.run()

