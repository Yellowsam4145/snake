import random
from time import sleep as wait
import sys
import keyboard  # Requires the `keyboard` library

def clear_lines_above(n):
    """Clears the n lines immediately above the current cursor position."""
    for _ in range(n):
        # Move cursor up one line
        sys.stdout.write('\033[1A')
        # Erase the current line (from cursor to end)
        sys.stdout.write('\033[2K')
        sys.stdout.flush()

def waitloop(delay, direction):
    for currenttimes in range(delay):
        if keyboard.is_pressed('w'):  # Move up
            direction = [0, -1]
        elif keyboard.is_pressed('s'):  # Move down
            direction = [0, 1]
        elif keyboard.is_pressed('a'):  # Move left
            direction = [-1, 0]
        elif keyboard.is_pressed('d'):  # Move right
            direction = [1, 0]
        if keyboard.is_pressed('q'):  # Quit the program
            break
        wait(0.01)
    return direction

class Screen8x8:
    def __init__(self):
        # Initialize a 8x8 screen with '#' characters
        self.screen = [['' for _ in range(8)] for _ in range(8)]

    def display(self):
        # Erase the previous output for next frame
        clear_lines_above(10)
        # Print the screen row by row
        print('-' * 19)  # Separator for clarity
        for row in self.screen:
            print('|', ' '.join(row), '|')
        print('-' * 19)  # Separator for clarity

    def set_char(self, x, y, char):
        # Set a character at position (x, y)
        if 0 <= x < 8 and 0 <= y < 8:
            self.screen[y][x] = char
        else:
            print("Coordinates out of bounds!")

    def clear(self):
        # Clear the screen
        self.screen = [[' ' for _ in range(8)] for _ in range(8)]

snake = [[3, 3], [3, 2], [3, 1]]  # Initial snake position in center with length 3
direction = [0, 0]
apple = [4, 4]  # Initial apple position
extrachance = 1
lastsnake = snake.copy()
direction = [1, 0]  # Initial direction to the right

input("Press Enter to start...")  # Initial input before starting the game
clear_lines_above(2)  # Clear the input prompt

if __name__ == "__main__":
    screen = Screen8x8()
    screen.clear()  # Clear the screen
    screen.set_char(apple[0], apple[1], '@')  # Draw the apple
    while True:
        screen.display()  # Display the cleared screen
        last_direction = direction.copy()
        direction = waitloop(25, direction)  # Small delay to control speed

        if direction == [-last_direction[0], -last_direction[1]]:  # Inverse direction if snake is going back on itself
            direction = last_direction
        
        newpos = [snake[0][0] + direction[0], snake[0][1] + direction[1]]

        # Update snake position
        if not (0 <= newpos[0] < 8 and 0 <= newpos[1] < 8) or newpos in snake:  # Ensure snake stays within bounds and doesn't collide with itself
            if extrachance > 0:
                extrachance -= 1
                snake = lastsnake.copy()  # Revert to last valid position
                direction = waitloop(25, direction)  # Brief pause for effect
            else:
                print("Game Over! Snake crashed!")
                break
        else:
            extrachance = 1  # Reset extra chance if within bounds
            screen.set_char(snake[-1][0], snake[-1][1], ' ')  # Clear previous position
            snake.insert(0, newpos)

            if not snake[0] == apple:
                del snake[-1]  # Remove tail segment
            else:
                
                # Apple eaten, respawn it
                apple = [random.randint(0, 7), random.randint(0, 7)]
                while apple in snake:  # Ensure apple doesn't spawn on the snake
                    apple = [random.randint(0, 7), random.randint(0, 7)]
                screen.set_char(apple[0], apple[1], '@')  # Draw the new apple
            
            # Update screen with snake position
            screen.set_char(snake[0][0], snake[0][1], '0')
            screen.set_char(snake[1][0], snake[1][1], 'O')
            screen.set_char(snake[-1][0], snake[-1][1], 'o')
            lastsnake = snake.copy()  # Save last valid position