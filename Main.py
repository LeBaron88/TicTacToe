# Tic Tac Toe Game developed in Python
# Le Baron 2019
# ------------------------------------


# ------ Import section --------------

import turtle
import random

# ------- end of import --------------

# ---- Initialize Variables ----------

game_data = [  # 2D list to hold game position values on the board, used also during drawing
    [0,0,0],
    [0,0,0],
    [0,0,0]
]
game_play = True # Set the game as ready with a True value, false meaning game over
player_turn = False # True waits for the player and False waits for the computer

# ------ End of Initialization -------

# ------ Functons section ------------

# Screen Set-up
def setup_screen():
    GameWindow = turtle.Screen()
    GameWindow.bgcolor("black") # Black background for the game
    GameWindow.title("Tic Tac Toe") # Game title

# Draw the game lines
def draw_lines():
    # Draw my game borders
    border_pen = turtle.Turtle()
    border_pen.speed(0)
    border_pen.color("white") # white lines on the black background
    border_pen.pensize(3) # width of the lines
    x, y, z = -150, 50, 300  # x and y positions of the pen on the 600x600 screen, z length of the line to be drawn
    # draw horizontal lines as per default position of the turtle head (from left to right)
    for i in range(2):
        border_pen.penup()  # Refrain the pen from writing
        border_pen.setposition(x, y)  # go to position of x and y to start drawing the line
        border_pen.pendown()  # Get the pen ready to write
        border_pen.fd(z)  # start drawing a line for z distance
        y *= -1 # Allow the second line to be drawn on the opposite position on the y axis

    # draw vertical lines
    border_pen.rt(90)  # change head direction 90 degree down
    x, y = -50, 150  # set new position of the pen on the screen
    for i in range(2):
        border_pen.penup()  # Refrain the pen from writing
        border_pen.setposition(x, y)  # go to position of x and y to start drawing the line
        border_pen.pendown()  # Get the pen ready to write
        border_pen.fd(z)  # start drawing a line for z distance
        x *= -1 # Allow the second line to be drawn on the opposite position on the x axis
    border_pen.hideturtle()

# Draw Game markers that used to show the positions the players used, taking the game data list and positions to be used to draw on the board
def draw_marker(data, a, b):
    # Place markers on the game, X for player and O for the Computer
    global game_play # global variable to be accessed in this function to check if the game is still on or over
    marker = turtle.Turtle() # create a marker turtle to write on the game board
    marker.speed(0)
    marker.color("white")
    marker.penup()
    x, y =  -105, 90 # first box position on the game board, centering the text on each box
    if data[a][b] == 1: # marker for the player
        marker_string = "X"
    elif data[a][b] == -1: # marker for the computer
        marker_string = "O"
    marker.setposition(x + (b * 100), y + (a * -100))
    marker.write(marker_string, False, align="left", font=("Arial", 20, "normal"))
    marker.hideturtle()

    if game_winner(game_data) != 0: # Check if there is a winner and stop the game
        game_play = False
    line = 0 # used to determine the number of lines with no available positions
    for i in range(3):
        if 0 not in game_data[i]:
            line += 1
    if line == 3: # check if all the lines are filled and stop the game if so
        game_play = False

    if not game_play: # to be performed only when the game is over
        final_marker = turtle.Turtle()  # create a marker turtle to write on the game board
        final_marker.speed(0)
        final_marker.color("red") # red color for the game result
        final_marker.penup()
        final_marker.hideturtle()
        final_marker.setposition(-45, 200) # position for the result to be shown
        if game_winner(game_data) == 1: # Player wins
            final_marker_string = "You WON"
        if game_winner(game_data) == -1: # Computer wins
            final_marker_string = "You LOST"
        if game_winner(game_data) == 0: # tie
            final_marker_string = "You TIED"
        final_marker.write(final_marker_string, False, align="left", font=("Arial", 20, "normal"))

# Function to check the winner
def game_winner(data):
    # Check if any horizontal line has been filled by the same player
    for i in range(3):
        if data[i][0] == data[i][1] and data[i][0] == data[i][2] and data[i][0] != 0:
            return data[i][i] # return the winner 1 for the player and -1 for the computer

    # Check if any vertical line has been filled by the same player
    for j in range(3):
        if data[0][j] == data[1][j] and data[0][j] == data[2][j] and data[0][j] != 0:
            return data[j][j] # return the winner for the player and -1 for the computer

    # Check if the forward diagonal has been filled by the same player
    if data[0][0] == data[1][1] and data[0][0] == data[2][2] and data[0][0] != 0:
        return data[0][0] # return the winner for the player and -1 for the computer

    # Check if the backward diagonal has been filled by the same player
    if data[0][2] == data[1][1] and data[0][2] == data[2][0] and data[0][2] != 0:
        return data[0][2] # return the winner for the player and -1 for the computer

    return 0

# Get user game input on mouse click
def user_input(x, y):
    global player_turn # global variable to be used to know whether it is the player's turn or computer
    global game_play # global variable to be used to know whether the game is over or still on
    if player_turn and game_play:
        global game_data
        i, j, z = -150, 150, 100 # Top left corner position on the game board and z the width of each box
        for a in range(3):
            for b in range(3):
                if (x > (i + (z * b))) and (x < (i + (z * (b + 1)))) and (y > (j - (z * (1 + a)))) and (y < (j - (z * a))): # get the position on the screen and translate it to a specific position on our game baord
                    if game_data[a][b] == 0: # check whether the position chosen is available for play
                        game_data[a][b] = 1 # set the position with the player marker
                        draw_marker(game_data, a, b) # call the function to draw the new position
    player_turn = False # set the turn to the computer
    cpu_turn() # Call the computer to play

#Get the CPU to play with basic random position
def cpu_turn():
    global player_turn # global variable to be used to know whether it is the player's turn or computer
    global game_play # global variable to be used to know whether the game is over or still on
    global game_data # get the game data list to determine available spots for the computer to play
    possible_moves = [] # list to get all available positions
    if not player_turn and game_play:
        x = 0 # used to get indexes of available positions
        for i in range(3):
            for j in range(3):
                if game_data[i][j] == 0:
                    possible_moves.append(x) # create a list with indexes of available positions
                x += 1
        if (len(possible_moves)) > 0: # make sure there is still available positions
            y = random.choice(possible_moves) # select randomly an index among the available positions
            s = 0 # used to check the index of the game board to match it with the selected
            for m in range(3):
                for n in range(3):
                    if s == y:
                        game_data[m][n] = -1 # set the game board list with the computer choice
                        draw_marker(game_data, m, n) # call the function to draw the new position
                    s = s + 1
        player_turn = True # set the turn to the computer

# Bind the function to the mouse click event and set the listener
turtle.onscreenclick(user_input,1)
turtle.listen()

# ----------- End of Functions ---------------

# -------------- Start Game ------------------

setup_screen() # Draw screen
draw_lines() # Draw game borders
cpu_turn() # Request the computer to start

turtle.mainloop() # Main loop of the game

# ------------- End of Game ------------------


