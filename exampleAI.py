from xj9 import XJ9
import sys
import random

class Player( XJ9 ):
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
if len( sys.argv ) == 2:
	joined = player.Join( sys.argv[ 1 ] )
	if joined:
		player.Start()