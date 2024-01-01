import tkinter as tk
import random
import time

class SnakeGame:
    def __init__(self, master):
        # Initialize the SnakeGame
        self.gamelevel = 200
        self.leve = "Simple Level"
        self.max_duration = 60
        self.start_time = time.time()
        self.master = master
        self.ai_score = 0
        self.master.title("Snake Game")
        self.master.geometry("400x400")
        self.master.resizable(False, False)

        # Create a canvas for the game
        self.canvas = tk.Canvas(self.master, bg="black", width=400, height=400)
        self.canvas.pack()
        self.canvas.create_rectangle(0, 0, 400, 400, outline="purple", width=20, tags="border")

        # Initialize the player snake with three segments and set the initial direction to "Right"
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"

        # Initialize the AI snake with three segments and set the initial direction to "Left"
        self.ai_snake = [(200, 200), (190, 200), (180, 200)]
        self.ai_direction = "Left"

        # Create the initial food and hurdles
        self.food = self.create_food()
        self.hurdles = self.create_hurdles()

        # Initialize the score
        self.score = 0

        # Initialize the game_over attribute
        self.game_over = False

        # Bind the keypress event to the change_direction method
        self.master.bind("<KeyPress>", self.change_direction)

        # Start the game loop
        self.update()

    # ... (rest of the code remains unchanged)


    def create_food(self):
        # Create a red rectangle representing the food at a random position
        x = random.randint(0, 18) * 20
        y = random.randint(0, 18) * 20
        food = self.canvas.create_oval(x, y, x + 20, y + 20, fill="green", tags="food")
        return food

    def create_hurdles(self):
        # Create blue rectangles representing hurdles at random positions
        hurdles = []
        for _ in range(5):  # You can adjust the number of hurdles as needed
            x = random.randint(0, 18) * 20
            y = random.randint(0, 18) * 20
            hurdle = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="blue", tags="hurdle")
            hurdles.append(hurdle)
        return hurdles

    def move_snake(self):
        # Move the player snake based on its current direction
        head = self.snake[0]
        if self.direction == "Right":
            new_head = (head[0] + 20, head[1])
        elif self.direction == "Left":
            new_head = (head[0] - 20, head[1])
        elif self.direction == "Up":
            new_head = (head[0], head[1] - 20)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 20)

        # Check if the new head touches a hurdle
        if any(self.canvas.coords(hurdle) == new_head for hurdle in self.hurdles):
            self.show_game_over()
            return

        # Update the player snake's position
        self.snake.insert(0, new_head)

        # Check if the head touches the food
        food_coords = self.canvas.coords(self.food)
        if head[0] == food_coords[0] and head[1] == food_coords[1]:
            # If the player snake eats the food, create a new food
            self.canvas.delete("food")
            self.food = self.create_food()
            # Increase the score
            self.score += 10
            # Update the score display
            self.update_score()
        else:
            # If the player snake did not eat the food, redraw the snake and remove the last segment
            self.canvas.delete("snake")
            for segment in self.snake:
                self.canvas.create_oval(
                    segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="orange", tags="snake"
                )
            self.snake = self.snake[:-1]

    def move_ai_snake(self):
        # Move the AI snake toward the food
        ai_head = self.ai_snake[0]
        food_coords = self.canvas.coords(self.food)

        # Calculate the direction to move towards the food
        if ai_head[0] < food_coords[0]:
            self.ai_direction = "Right"
        elif ai_head[0] > food_coords[0]:
            self.ai_direction = "Left"
        elif ai_head[1] < food_coords[1]:
            self.ai_direction = "Down"
        elif ai_head[1] > food_coords[1]:
            self.ai_direction = "Up"

        # Move the AI snake based on the calculated direction
        if self.ai_direction == "Right":
            new_head = (ai_head[0] + 20, ai_head[1])
        elif self.ai_direction == "Left":
            new_head = (ai_head[0] - 20, ai_head[1])
        elif self.ai_direction == "Up":
            new_head = (ai_head[0], ai_head[1] - 20)
        elif self.ai_direction == "Down":
            new_head = (ai_head[0], ai_head[1] + 20)

        # Check if the AI snake collides with itself or hurdles
        if any(self.canvas.coords(hurdle) == new_head for hurdle in self.hurdles) or new_head in self.snake:
            self.show_game_over()
            return


        # Update the AI snake's position
        self.ai_snake.insert(0, new_head)

        # If the AI snake eats the food, create a new food
        if ai_head[0] == food_coords[0] and ai_head[1] == food_coords[1]:
            self.canvas.delete("food")
            self.food = self.create_food()
            self.ai_score += 10

        # Redraw the AI snake
        self.canvas.delete("ai_snake")
        for segment in self.ai_snake:
            self.canvas.create_oval(
                segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="blue", tags="ai_snake"
            )
        self.ai_snake = self.ai_snake[:-1]

    def play_death_sound(self):
        # Play the death sound
        # Assuming you have a sound player method here
        pass

    def update_score(self):
        # Update the score display on the canvas
        self.canvas.delete("score")
        if self.score == 50:
            self.gamelevel = 100
            self.leve = "Medium Level"
        elif self.score == 100:
            self.gamelevel = 50
            self.leve = "Hard Level"
        elif self.score == 130:
            self.gamelevel = 10
            self.leve = "Bomb Level"
        self.canvas.create_text(200, 60, text="Score 300 to win Buffet", fill="White", font=("Helvetica", 9), tags="score")
        self.canvas.create_text(200, 20, text=f"Score: {self.score}", fill="White", font=("Helvetica", 9), tags="score")
        self.canvas.create_text(200, 40, text=f"{self.leve}", fill="White", font=("Helvetica", 9), tags="score")

    def update(self):
        # Check if the game is already over or the time limit has been reached
        if not self.game_over:
            elapsed_time = time.time() - self.start_time

            if elapsed_time >= self.max_duration:
                self.show_game_over()
                return

            # Update the game state and schedule the next update
            if self.check_collision():
                self.show_game_over()
                return

            self.move_snake()
            self.move_ai_snake()

            self.master.after(self.gamelevel, self.update)
    def change_direction(self, event):
        # Change the player snake's direction based on the key pressed
        if event.keysym == "Right" and not self.direction == "Left":
            self.direction = "Right"
        elif event.keysym == "Left" and not self.direction == "Right":
            self.direction = "Left"
        elif event.keysym == "Up" and not self.direction == "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and not self.direction == "Up":
            self.direction = "Down"

    def check_collision(self):
        # Check if the player snake collides with the boundaries, itself, or hurdles
        head = self.snake[0]
        return (
                head[0] < 0 or head[0] >= 400 or
                head[1] < 0 or head[1] >= 400 or
                head in self.snake[1:] or
                any(self.canvas.coords(hurdle) == [head[0], head[1], head[0] + 20, head[1] + 20] for hurdle in
                    self.hurdles)
        )

    def save_score(self):
        # Save the score to a text file
        with open("scores.txt", "a") as file:
            file.write(f"{self.score}\n")

    def show_game_over(self):
        # Save the score before displaying the "Game Over" dialog
        self.save_score()
        self.message = "Game Over"
        if self.score == 0:
            self.message = "Better Luck Next Time"
        # Display a "Game Over" window with a restart button and score ranking
        game_over_window = tk.Toplevel(self.master)
        game_over_label = tk.Label(game_over_window, text=self.message, font=("Helvetica", 16))
        game_over_label.pack(pady=10)

        # Display the final scores for both player and AI
        player_score_label = tk.Label(game_over_window, text=f"Player Score: {self.score}", font=("Helvetica", 12))
        player_score_label.pack(pady=5)

        ai_score_label = tk.Label(game_over_window, text=f"AI Score: {self.ai_score}", font=("Helvetica", 12))
        ai_score_label.pack(pady=5)

        # Display the ranking of scores
        ranking_label = tk.Label(game_over_window, text="Score Ranking", font=("Helvetica", 14, "bold"))
        ranking_label.pack(pady=10)

        # Read scores from the file and display them
        scores = self.read_scores()
        scores = sorted(scores, reverse=True)
        for i, score in enumerate(scores, start=1):
            if i < 5:
                score_label = tk.Label(game_over_window, text=f"{i}. {score}", font=("Helvetica", 12))
                score_label.pack()

        # Restart button
        restart_button = tk.Button(game_over_window, text="Restart", command=self.restart_game)
        restart_button.pack(pady=20)

        # Set game_over to True
        self.game_over = True

    def read_scores(self):
        # Read scores from the text file and return a list
        try:
            with open("scores.txt", "r") as file:
                scores = [int(line.strip()) for line in file]
        except FileNotFoundError:
            scores = []
        return scores

    def restart_game(self):
        # Restart the game by destroying the current window and creating a new one
        self.master.destroy()
        root = tk.Tk()
        game = SnakeGame(root)
        root.mainloop()

if __name__ == "__main__":
    # Run the game when the script is executed
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
