from xj9 import XJ9
import sys
import random

# Create a new Player that extends the XJ9 moveset
class Player( XJ9 ):
	# Define the GameLoop, containing all the actions
	def GameLoop( self ):
		# Iterate over the horizontal cells
		for x in range( self.game.width ):
			# Iterate over the vertical cells
			for y in range( self.game.height ):
				# Check if the selected cell belongs to the player
				if self.OwnCell( self.GetCell( x, y ) ):
					# Choose an arbitrary value to add/subtract from X or Y
					d = random.choice( [ ( 0, 1 ), ( 0, -1 ), ( 1, 0 ), ( -1, 0 ) ] )
					# Use the arbitrarily chosen values to find a target
					target = self.GetCell( x + d[ 0 ], y + d[ 1 ] )
					# Check if the target is inside the arena
					if not target == None:
						# Check if the target is not owned by the player
						if not self.OwnCell( target ):
							# Check if the target can be attacked quickly
							if target.takeTime <= 4.0:
								# Attack the target and store the results
								data = self.Attack( target )
								# Print the data to the console
								print data
								# Check if the attack was successful
								if data[ 0 ]:
									# Check if the player has enough gold for a base
									if self.gold >= 60 and self.baseNum < 3:
										# Build a base on the newly conquered cell
										self.BuildBase( target.x, target.y )
									# Break from the game loop once a target has been attacked
									return

# Create an instance of the newly defined Player
player = Player()
# Define the name of the player
name = "MyXJ9"
# Check if a command line argument was provided
if len( sys.argv ) == 2:
	# Allow the user to rename the bot through a parameter
	name = sys.argv[ 1 ]
# Join the game and get the data
joined = player.Join( name )
# Check if the player successfully joined the Colorfight game
if joined:
	# Start the GameLoop()
	player.Start()