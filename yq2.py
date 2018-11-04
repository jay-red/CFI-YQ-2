import pyximport; pyximport.install()
from xj9 import XJ9
import sys
import random
import numpy as np

class YQ2( XJ9 ):
	def GameLoop( self ):
		self.threshold = 4.0
		self.FetchMap()
		boost = False
		targetCell = None
		for target in self.targetCells:
			if ( target.cellType == "gold" or target.cellType == "energy" ):
				if self.Fast( target ):
					targetCell = target
				if self.energy >= 60 and target.cellType == "gold":
					up, right, down, left = self.GetAround( target )
					if not up == None and self.Blast( up.x, up.y, "square" )[ 0 ]:
						pass
					elif not right == None and self.Blast( right.x, right.y, "square" )[ 0 ]:
						pass
					elif not down == None and self.Blast( down.x, down.y, "square" )[ 0 ]:
						pass
					elif not left == None and self.Blast( left.x, left.y, "square" )[ 0 ]:
						pass
					self.Attack( target )
					return
		if targetCell == None or self.SameCell( targetCell, self.lastCell ):
			for target in self.targetCells:
				if self.Fast( target ):
					targetCell = target
					if not self.OwnCell( targetCell ) and not targetCell.owner == 0 and random.randrange( 4 ) == 0:
						break
					elif random.randrange( int( self.targetNum / 2 ) ) == 0:
						break
		if self.energy >= 95.0:
			boost = True
		if self.Fast( targetCell ):
			self.Attack( targetCell, boost = boost )
		if self.gold >= 60.0 and self.baseNum < 3:
			newBase = random.choice( self.myCells )
			if self.Fast( newBase ):
				self.Attack( newBase )
			self.BuildBase( newBase.x, newBase.y )
		if self.baseNum == 1:
			self.Defend( self.bases[ 0 ] )
		self.lastCell = targetCell

player = YQ2()
name = "YQ-2"
if len( sys.argv ) == 2:
	name = sys.argv[ 1 ]
joined = player.Join( name )
if joined:
	player.Start()