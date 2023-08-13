from turtle import *
from random import randrange
from freegames import square, vector

food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)
timer_interval = 300
timer = 0
current_score = 0
high_score = 0
snake_speed = 1  # Initial speed of the snake

timer_turtle = Turtle()
timer_turtle.color('white')
timer_turtle.hideturtle()
timer_turtle.penup()
timer_turtle.goto(200, 250)

score_turtle = Turtle()
score_turtle.color('white')
score_turtle.hideturtle()
score_turtle.penup()
score_turtle.goto(-200, 250)  # Adjusted y-coordinate to move the score down

high_score_turtle = Turtle()
high_score_turtle.color('white')
high_score_turtle.hideturtle()
high_score_turtle.penup()
high_score_turtle.goto(0, 250)

restart_turtle = Turtle()
restart_turtle.color('white')
restart_turtle.hideturtle()
restart_turtle.penup()
restart_turtle.goto(100, -100)
restart_turtle.hideturtle() 

def change(x, y):
    aim.x = x
    aim.y = y

def inside(head):
    return -290 < head.x < 290 and -290 < head.y < 290
def interpolate_color(start_color, end_color, fraction):
    r = start_color[0] + (end_color[0] - start_color[0]) * fraction
    g = start_color[1] + (end_color[1] - start_color[1]) * fraction
    b = start_color[2] + (end_color[2] - start_color[2]) * fraction
    return int(r), int(g), int(b)
def move():
    global timer, current_score, snake_speed

    timer += timer_interval / 1000  # Update timer correctly in milliseconds
    timer_turtle.clear()
    timer_turtle.write(f"Timer: {timer:.1f}s", align="center", font=("Arial", 16, "normal"))

    score_turtle.clear()
    score_turtle.write(f"Score: {current_score}", align="center", font=("Arial", 16, "normal"))

    high_score_turtle.clear()
    high_score_turtle.write(f"High Score: {high_score}", align="center", font=("Arial", 16, "normal"))

    head = snake[-1].copy()
    head.move(aim)

    if not inside(head) or head in snake:
        end_game()
        return

    snake.append(head)

    if head == food:
        current_score += 1
        print('Snake:', len(snake))
        food.x = randrange(-28, 28) * 10
        food.y = randrange(-28, 28) * 10
    else:
        snake.pop(0)

    clear()

    # Draw boundary
    for x in range(-290, 300, 10):
        square(x, 290, 9, 'white')
        square(x, -290, 9, 'white')
    for y in range(-290, 300, 10):
        square(290, y, 9, 'white')
        square(-290, y, 9, 'white')
    for i, body in enumerate(snake):
        fraction = i / len(snake)  # Calculate fraction for color interpolation
        color_gradient = interpolate_color((0, 0, 255), (128, 0, 128), fraction)  # Blue to purple
        color = "#{:02x}{:02x}{:02x}".format(*color_gradient)
        square(body.x, body.y, 9, color)
    square(food.x, food.y, 9, 'red')  
    update()

    ontimer(move, timer_interval // snake_speed)  # Adjust the timer interval based on the snake's speed
def start_game():
    global current_score, snake, timer, snake_speed
    current_score = 0
    snake = [vector(10, 0)]
    timer = 0
    snake_speed = 1  # Reset snake speed to default
    move()

def end_game():
    global high_score
    if current_score > high_score:
        high_score = current_score

    clear()
    write(f"Game Over\nScore: {current_score}\nHigh Score: {high_score}\nPress 'R' to Restart", align="center", font=("Arial", 16, "normal"))

    listen()
    onkey(start_game, 'r')
    onkey(speed_up, 's')  # Listen for 'S' key to speed up the snake

def speed_up():
    global snake_speed
    if snake_speed < 5:  # Set a maximum speed limit (adjust as needed)
        snake_speed += 1

def main():
    bgcolor("black")
    setup(600, 600)
    hideturtle()
    tracer(False)
    listen()

    onkey(lambda: change(10, 0), 'Right')
    onkey(lambda: change(-10, 0), 'Left')
    onkey(lambda: change(0, 10), 'Up')
    onkey(lambda: change(0, -10), 'Down')

    ontimer(start_game, timer_interval)

    done()

if __name__ == "__main__":
    main()