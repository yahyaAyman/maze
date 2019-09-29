import random
from stack import Stack

class MazeGame:
    '''
    A game where a player moves through a grid to reach some treasure.
    '''

    def __init__(self, width, height, player):
        '''
        (MazeGame, Player) -> None
        Construct a new MazeGame with the given width and height,
        and a player. MazeGame should also place a "gold" at
        a randomly chosen coordinate on the far edge of the grid.
        '''
        
        self.width = width
        self.height = height
        self.player = player
        # place the gold at a random spot on the far edge of the grid
        self.gold_coord = (width-1, random.randint(1, height-1)) 
        
        self.grid = []
        self.make_grid()

        self.s = Stack()
        self.s.push((0,0))
        
    def make_grid(self):#Given
        '''
        (MazeGame) -> None
        Given width, height and positions of player and gold,
        append things to this maze's grid.
        '''
        
        for i in range(self.height):
            self.grid.append([])
            for j in range(self.width):
                self.grid[i].append('(_)') 
        
        self.grid[self.player.y][self.player.x] = '(x)'
        self.grid[self.gold_coord[1]][self.gold_coord[0]] = '(*)'
    
    def play_game(self):#Given
        '''
        (MazeGame) -> None
        Play the game, with each player taking turns making a move, until
        one player reaches the gold. Players each keep track of their wins and losses.
        '''
        
        # print out the starting state of the maze
        print(self)
        print('------------')
        
        while (not (self.player.x, self.player.y) == \
               (self.gold_coord[0], self.gold_coord[1])):
            # if no one has reached the gold yet, play one turn of the game (one player makes one move)
            self.play_one_turn()

        
        print('Yay, you won, {}!'.format(self.player.name))


    def get_new_position(self, d):#given
        '''
        (MazeGame, str) -> tuple of two ints or None        
        Given a direction represented as a string "N", "S", "E", or "W" (for moving North,
        South, East or West respectively), return the new position. If the new position is
        not valid (i.e. falls outside of the grid), return None.
        '''
        
        direction_dict = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
        dx, dy = direction_dict[d]
        new_x = self.player.x + dx
        new_y = self.player.y + dy

        if (0 <= new_x < self.width) and (0 <= new_y < self.height):
            return new_x, new_y
        else:
            return None

    def update_grid(self, new_position):#given
        '''
        (MazeGame, tuple of two ints) -> None
        Move player to the given new position in grid.
        '''
        # update grid to reflect updated coordinates for current_player
        # keep track of the Player's current position before they move
        old_x, old_y = self.player.x, self.player.y 
        self.player.move(new_position)
        self.grid[self.player.y][self.player.x] = self.grid[old_y][old_x]
        self.grid[old_y][old_x] = '(_)'

        self.s.push(new_position)

        
    def play_one_turn(self):#given
        '''
        (MazeGame) -> None
        Play one turn of the game. Turn could involve moving one place,
        attempting to move one place, or undoing the most recent move.
        '''

        # get the direction the Player wants to move
        direction = self.player.get_direction() 

        if (direction == 'U'):
            self.undo_last_move()
        else:
            # this returns None if move is not valid
            new_position = self.get_new_position(direction) 
            
            if new_position: # this is the same as saying "if new_position != None"                
                self.update_grid(new_position)
                print("Player {} moved {}.".format(self.player.name, direction))
            else:
                print("Player {} attempted to move {}. Way is blocked.".format(self.player.name, direction))

        # print current state of game
        print(self)
        print('------------')

    def undo_last_move(self):#not given
        '''
        (MazeGame) -> None
        Update the grid to the state it was in before the previous move was made.
        If no moves were previously made, print out the message "Can't undo".
        '''
        direction_dict = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}        

        if self.s.size() >= 2:
            if self.s.pop() == (0,0):
                pass
            
            else:
                last_move = self.s.pop()
                self.update_grid(last_move)
        
        else:
            pass
        
        # TODO: IMPLEMENT THIS AS DESCRIBED IN INSTRUCTIONS



##        moves_list = self.player.move_tracker
##
##        if '({0},{1})'.format(self.player.x, self.player.y) !=  '(0,0)' \
##           and len(moves_list) > 0:
##            if moves_list[len(moves_list) - 2] == 'U':
##                raise UndoError('A previous move of N, S, E, or W' \
##                                      + ' must be made before using Undo.')
##            elif moves_list[len(moves_list) - 2] == 'N':
##                undone_position = self.get_new_position('S')
##            elif moves_list[len(moves_list) - 2] == 'S':
##                undone_position = self.get_new_position('N')
##            elif moves_list[len(moves_list) - 2] == 'E':
##                undone_position = self.get_new_position('W')
##            elif moves_list[len(moves_list) - 2] == 'W':
##                undone_position = self.get_new_position('E')
##            self.update_grid(undone_position)
##        else:
##            print("Can't undo")
            
#Important Notes: This method has been commented out since the solution
#               requires a Stack.
#Assumed that using U a second time should raise an error
#The issue with using a move_tracker list was the possibility of using U on
#   Turn 1 of Round 2 to undone the Final Turn of Round 1. I worked around this
#   by including, in the first if statement, that the position of the Player
#   should not be at the origin if they wish to use U. If they try to do this,
#   it will print("Can't undo"), as expected in the docstring.

    def __str__(self): #given
        '''
        (MazeGame) -> str
        Return string representation of the game's grid.
        '''
        s = ''
        for row in self.grid:
            s += ''.join(row) + "\n"
        return s.strip()


# TODO: IMPLEMENT PLAYER CLASS AS DESCRIBED IN INSTRUCTIONS
class Player:#This whole class was created from scratch
    """
    Create a Player that can play MazeGame.
    """
    def __init__(self, name, x = 0, y = 0):
        """
        (MazeGame, str, int, int)
        Constructs a new player with a name and a location on the game grid x, y respectively
        """
        self.name = name
        self.x = x
        self.y = y
        #s = Stack()
                
#move_tracker attribute will remain commmented for now


    def get_direction(self) -> str: #Done
        '''Return a string based on the user input. This input will be the
        command that the user wishes to do for their Player self (N, S, E, W,
        or U).'''

        user_command = input("It's your turn! What would you like to do?" \
                        + " (N (North), S (South), E (East), W (West), or" \
                        + " U (Undo last move)): ")

        if user_command not in ['N', 'S', 'E', 'W', 'U']:
            raise IllegalMoveError('Cannot proceed with this move.' \
                                + ' Valid moves include: N, S, E, W, U.')
        else:
            #self.move_tracker.append(user_command)
            return user_command


    def move(self, new_position):
        """
        (MazeGame, tuple) -> None
        Replaces the old x and y coordinates of self with the new coordinates
        from new_position.
        """
        
        self.x, self.y = new_position[0], new_position[1]
        


#Player has the following methods: __init__, move, get_direction
#Player has attributes: name, x, y. Might also have recorded wins/losses
#It seems that get_direction only needs a user input function (N,S,E,W, or U)
#It seems that the move method needs us to change player.x and player.y to
#   to its new coordinates

class IllegalMoveError(Exception): #created
    pass


class UndoError(Exception): #created
    pass


def main():
    """Prompt the user to configure and play the game."""

    width = int(input("Width: "))
    height = int(input("Height: "))

    name = input("What is your name? ")
    p1 = Player(name, 0, 0) #make a player at position (0,0)
    
    play_again = True
    while play_again:
        g = MazeGame(width, height, p1)
        g.play_game()
        # reset player locations at end of round
        p1.move((0,0))
        play_again = input('Again? (y/n) ') == 'y'           


if __name__ == '__main__':
    main()
