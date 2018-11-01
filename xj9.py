import colorfight as cf
import random
from json import dumps, loads

class XJ9:
	"""
		Initialization for the Player and its Variables
	"""

	def __init__( self ):
		self.game = cf.Game()
		self.uid = int( 0 )
		self.width = int( 0 )
		self.height = int( 0 )
		self.currTime = float( 0 )
		self.cdTime = float( 0 )
		self.gold = float( 0 )
		self.energy = float( 0 )
		self.cellNum = int( 0 )
		self.baseNum = int( 0 )
		self.goldCellNum = int( 0 )
		self.energyCellNum = int( 0 )

	def InitializeGame( self ):
		self.uid = self.game.uid
		self.width = self.game.width
		self.height = self.game.height

	def Join( self, name = "" ):
		if name == "":
			print "usage: Join( name )"
		data = self.game.JoinGame( name, token = True )
		self.InitializeGame()
		return data

	def Start( self, debug = 0 ):
		if debug == 0:
			while True:
				self.FetchInfo()
				self.GameLoop()
				self.Refresh()
		else:
			newArr = []
			for y in range( self.height ):
				line = []
				for x in range( self.width ):
					line.append( self.GetCell( x, y ).takeTime )
				newArr.append( line )
			print dumps( newArr )

	"""
		Recreation of Built-in Functions for future Cython Implementation
	"""

	def GetCell( self, x, y ):
		return self.game.GetCell( x, y )

	def AttackCell( self, x, y ):
		return self.game.AttackCell( x, y )

	def Refresh( self ):
		self.game.Refresh()

	"""
		Functions for Gathering Relevant Information
	"""
	def FetchInfo( self ):
		self.currTime = self.game.currTime
		self.cdTime = self.game.cdTime
		self.gold = self.game.gold
		self.energy = self.game.energy
		self.cellNum = self.game.cellNum
		self.baseNum = self.game.baseNum
		self.goldCellNum = self.game.goldCellNum
		self.energyCellNum = self.game.energyCellNum

	"""
		Player Defined Utilities
	"""

	def Cooldown( self ):
		return self.cdTime >= self.currTime

	def OwnCell( self, cell ):
		return cell.owner == self.uid

	"""
		Player Defined Actions
	"""

	def Attack( self, cell ):
		while self.Cooldown():
			self.Refresh()
			self.FetchInfo()
		data = self.AttackCell( cell.x, cell.y )
		if data[ 0 ]:
			while not self.OwnCell( self.GetCell( cell.x, cell.y ) ):
				self.Refresh()
		return data

	def GameLoop( self ):
		pass