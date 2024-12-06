import turtle

# Set up the screen
win = turtle.Screen()
win.title("Pong by ChatGPT")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)  # Stops the screen from updating automatically

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=6, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=6, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(40)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 2
ball.dy = 2

# Score
score_a = 0
score_b = 0

# Score Display
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

# Functions to move paddles
def paddle_a_up():
    y = paddle_a.ycor()
    if y < 250:  # Limit paddle movement
        paddle_a.sety(y + 20)


def paddle_a_down():
    y = paddle_a.ycor()
    if y > -240:
        paddle_a.sety(y - 20)


def paddle_b_mouse_move(x, y):
    """Move Paddle B with the mouse, restricted within the window bounds."""
    if -250 <= y <= 250:  # Limit movement within screen height
        paddle_b.sety(y)


# Keyboard bindings
win.listen()
win.onkeypress(paddle_a_up, "w")
win.onkeypress(paddle_a_down, "s")

# Mouse bindings
win.onscreenclick(paddle_b_mouse_move, 1)  # Use left mouse button to move paddle

# Main game loop
while True:
    win.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border checking
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1  # Reverse direction

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
        pen.clear()
        pen.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 24, "normal"))

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        pen.clear()
        pen.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 24, "normal"))

    # Paddle collisions
    if (ball.xcor() > 340 and ball.xcor() < 350) and (
        ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() - 50
    ):
        ball.setx(340)
        ball.dx *= -1

    if (ball.xcor() < -340 and ball.xcor() > -350) and (
        ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() - 50
    ):
        ball.setx(-340)
        ball.dx *= -1ß