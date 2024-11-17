import turtle

# Set up the screen
screen = turtle.Screen()
screen.title("Tic-Tac-Toe")
screen.setup(width=600, height=600)

# Draw the board
board = turtle.Turtle()
board.speed(0)
board.hideturtle()
board.pensize(5)


def draw_board():
    # Horizontal lines
    board.penup()
    board.goto(-300, 100)
    board.pendown()
    board.goto(300, 100)
    board.penup()
    board.goto(-300, -100)
    board.pendown()
    board.goto(300, -100)

    # Vertical lines
    board.penup()
    board.goto(-100, 300)
    board.setheading(270)
    board.pendown()
    board.goto(-100, -300)
    board.penup()
    board.goto(100, 300)
    board.pendown()
    board.goto(100, -300)


draw_board()

# Game state variables
player = "X"
positions = {}  # Store moves in grid positions


# Draw X
def draw_x(x, y):
    t = turtle.Turtle()
    t.hideturtle()
    t.color("red")
    t.pensize(10)

    # Draw the first diagonal
    t.penup()
    t.goto(x - 50, y - 50)  # Top-left of the square
    t.pendown()
    t.goto(x + 50, y + 50)  # Bottom-right of the square

    # Draw the second diagonal
    t.penup()
    t.goto(x - 50, y + 50)  # Bottom-left of the square
    t.pendown()
    t.goto(x + 50, y - 50)  # Top-right of the square


# Draw O
def draw_o(x, y):
    t = turtle.Turtle()
    t.hideturtle()
    t.color("blue")
    t.pensize(10)
    t.penup()
    t.goto(x, y - 40)
    t.pendown()
    t.circle(40)


# Handle clicks and ensure moves are valid
def click_handler(x, y):
    global player
    # Determine which square was clicked
    col = int((x + 300) // 200)
    row = int((300 - y) // 200)
    key = (row, col)

    # Check if move is valid
    if key not in positions and 0 <= row < 3 and 0 <= col < 3:
        positions[key] = player
        x_center = col * 200 - 300 + 100
        y_center = 300 - row * 200 - 100

        # Draw X or O in the center of the square
        if player == "X":
            draw_x(x_center, y_center)
            player = "O"
        else:
            draw_o(x_center, y_center)
            player = "X"

        # Check for a winner after each move
        check_winner()


# Check for a winner
def check_winner():
    win_patterns = [
        [(0, 0), (0, 1), (0, 2)],  # Rows
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],  # Columns
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],  # Diagonals
        [(0, 2), (1, 1), (2, 0)],
    ]
    for pattern in win_patterns:
        values = [positions.get(pos) for pos in pattern]
        if values == ["X", "X", "X"] or values == ["O", "O", "O"]:
            winner = values[0]
            display_winner(winner)
            screen.onclick(None)  # Disable further clicks
            return

    # Check for a draw
    if len(positions) == 9:
        display_winner("No one")  # Display a draw message
        screen.onclick(None)


# Display the winner
def display_winner(winner):
    message = turtle.Turtle()
    message.hideturtle()
    message.color("green")
    message.penup()
    message.goto(0, 0)
    message.write(f"{winner} wins!", align="center", font=("Arial", 24, "bold"))


# Listen for clicks
screen.onclick(click_handler)

# Keep the window open
screen.mainloop()
