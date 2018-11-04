import pyximport; pyximport.install()
import colorfight as cf
import random
from json import dumps, loads
import numpy as np
import time

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
		self.bases = None
		self.goldCellNum = int( 0 )
		self.energyCellNum = int( 0 )
		self.myCells = None
		self.edgeCells = None
		self.cellMap = None
		self.targetCells = None
		self.targetNum = int( 0 )
		self.lastCell = None
		self.threshold = float( 0 )

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
				start = time.time()
				self.FetchInfo()
				duration = time.time() - start
				print duration
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

	def AttackCell( self, x, y, boost = False ):
		return self.game.AttackCell( x, y, boost = boost )

	def Refresh( self ):
		self.game.Refresh()

	def BuildBase( self, x, y ):
		return self.game.BuildBase( x, y )

	def Blast( self, x, y, direction ):
		return self.game.Blast( x, y, direction )

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

	def FetchMap( self ):
		mapStr = ""
		self.myCells = []
		self.edgeCells = []
		self.targetCells = []
		self.bases = []
		for y in range( self.game.height ):
			line = []
			for x in range( self.game.width ):
				cell = self.GetCell( x, y )
				if self.OwnCell( cell ):
					if cell.isBase:
						self.bases.append( cell )
					self.myCells.append( cell )
					if self.EdgeCell( cell ):
						self.edgeCells.append( cell )
						mapStr += "2 "
					else:
						mapStr += "1 "
				else:
					mapStr += "0 "
			mapStr = mapStr[ : -1 ]
			mapStr += "; "
		self.cellMap = np.array( np.mat( mapStr[ : -2 ] ) )

	"""
		Player Defined Utilities
	"""

	def Cooldown( self ):
		return self.cdTime >= self.currTime

	def OwnCell( self, cell ):
		if cell == None:
			return False
		return cell.owner == self.uid

	def GetAround( self, cell ):
		directions = ( ( 0, -1 ), ( 1, 0 ), ( 0, 1 ), ( -1, 0 ) )
		cells = ( self.GetCell( cell.x + directions[ index ][ 0 ], cell.y + directions[ index ][ 1 ] ) for index in range( 4 ) )
		return cells

	def EdgeCell( self, cell ):
		data = False
		up, right, down, left = self.GetAround( cell )
		if not up == None and not self.OwnCell( up ):
			data = True
			self.targetCells.append( up )
			self.targetNum += 1
		if not right == None and not self.OwnCell( right ):
			data = True
			self.targetCells.append( right )
			self.targetNum += 1
		if not down == None and not self.OwnCell( down ):
			data = True
			self.targetCells.append( down )
			self.targetNum += 1
		if not left == None and not self.OwnCell( left ):
			data = True
			self.targetCells.append( left )
			self.targetNum += 1
		return data

	def SameCell( self, c1, c2 ):
		if c1 == None or c2 == None:
			return c1 == None and c2 == None
		return c1.x == c2.x and c1.y == c2.y

	def Fast( self, cell ):
		if cell == None:
			return False
		return not cell.takeTime == -1 and cell.takeTime <= self.threshold

	"""
		Player Defined Actions
	"""

	def Attack( self, cell, boost = False ):
		if cell == None:
			return ( False, 10, "Cell is null" )
		while self.Cooldown():
			self.Refresh()
			self.FetchInfo()
		data = self.AttackCell( cell.x, cell.y, boost = boost )
		if data[ 0 ]:
			while not self.OwnCell( self.GetCell( cell.x, cell.y ) ):
				self.Refresh()
		return data

	def Defend( self, cell ):
		up, right, down, left = self.GetAround( cell )
		triggers = ( up, right, down, left )
		amount = 0
		for trigger in triggers:
			if not self.OwnCell( trigger ):
				amount += 1
		if self.energy >= 30 and amount == 4 and ( cell.isBase and self.baseNum == 1 ):
			self.Blast( cell.x, cell.y, "square" )
		if self.Fast( cell ):
			self.Attack( cell )
		if self.Fast( up ):
			self.Attack( up )
		if self.Fast( right ):
			self.Attack( right )
		if self.Fast( down ):
			self.Attack( down )
		if self.Fast( left ):
			self.Attack( left )

	def GameLoop( self ):
		pass