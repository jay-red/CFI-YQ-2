import colorfight as cf
import random

class Player:
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

	def Join( self, name="ExJayNine" ):
		self.game.JoinGame( name )
		self.InitializeGame()

	def Start( self, debug = 0 ):
		if debug == 0:
			while True:
				print "Test"
				self.FetchInfo()
				self.GameLoop()
				self.Refresh()

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
		Player Defined Functions
	"""

	def Cooldown( self ):
		return self.cdTime >= self.currTime

	def Attack( self, cell ):
		while self.Cooldown():
			self.Refresh()
			self.FetchInfo()
		return self.AttackCell( cell.x, cell.y )

	def OwnCell( self, cell ):
		return cell.owner == self.uid

	def GameLoop( self ):
		for x in range( self.game.width ):
			for y in range( self.game.height ):
				c = self.GetCell( x, y )
				if self.OwnCell( c ):
					d = random.choice( [ ( 0, 1 ), ( 0, -1 ), ( 1, 0 ), ( -1, 0 ) ] )
					cc = self.GetCell( x + d[ 0 ], y + d[ 1 ] )
					if cc != None:
						if not self.OwnCell( cc ):
							if cc.takeTime <= 4.0:
								print( self.Attack( cc ) )
								return

player = Player()
player.Join()
player.Start()