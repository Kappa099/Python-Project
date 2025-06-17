import random
import turtle

# turtle model
drawer = turtle.Turtle()  
drawer.hideturtle()       
drawer.speed(0)           

# turtle model
def setup_turtle(): 
    turtle.bgcolor("white") 
    drawer.clear()           
    drawer.pensize(5)        
    draw_gallows()          

# turtle model
def draw_gallows():
    # Base
    drawer.penup()           
    drawer.goto(-100, -150)  
    drawer.setheading(0)     
    drawer.pendown()         
    drawer.forward(200)      

    # Pole
    drawer.penup()           
    drawer.goto(-50, -150)   
    drawer.setheading(90)    
    drawer.pendown()         
    drawer.forward(250)      

    # Top bar
    drawer.right(90)         
    drawer.forward(100)      

    # Rope
    drawer.right(90)         
    drawer.forward(30)       

# turtle model
def draw_hangman(lives_left):
    if lives_left == 5:
        drawer.penup()       
        drawer.goto(50, 70)  
        drawer.setheading(0) 
        drawer.pendown()     
        drawer.circle(20)    
    elif lives_left == 4:
        drawer.penup()       
        drawer.goto(50, 70)  
        drawer.setheading(-90)  
        drawer.pendown()     
        drawer.forward(50)   
    elif lives_left == 3:
        drawer.penup()       
        drawer.goto(50, 50)  
        drawer.setheading(-45)  
        drawer.pendown()     
        drawer.forward(30)   
    elif lives_left == 2:
        drawer.penup()       
        drawer.goto(50, 50)  
        drawer.setheading(-135) 
        drawer.pendown()     
        drawer.forward(30)   
    elif lives_left == 1:
        drawer.penup()       
        drawer.goto(50, 20)  
        drawer.setheading(-45)  
        drawer.pendown()     
        drawer.forward(30)   
    elif lives_left == 0:
        drawer.penup()       
        drawer.goto(50, 20)  
        drawer.setheading(-135) 
        drawer.pendown()     
        drawer.forward(30)   

# turtle model
def show_message(text, color):
    drawer.penup()
    drawer.goto(0, 120)
    drawer.color(color)
    drawer.write(text, align="center", font=("Arial", 50, "bold"))
    drawer.color("black")

def correct_answer():
    return random.choice(["hippo", "hangman", "directory", "problem", "python", "beatles"])

def encrypt(word):
    hidden = ["_"] * len(word)
    print(f"Your guessing word is: {hidden}")
    return hidden

def guesser(char, chosen, hidden, lives):
    found = False
    for i in range(len(chosen)):
        if char == chosen[i]:
            hidden[i] = char
            found = True
    if found:
        print(f"{char} is in the word! {hidden}")
    else:
        lives -= 1
        draw_hangman(lives)  # turtle model
        print(f"{char} is not in the word! You have {lives} lives left.")
    return lives

def play_again():
    again = input("Play again? (y/n): ").lower()
    return again == "y"

def main():
    while True:
        setup_turtle()  # turtle model

        sityva = correct_answer()
        hidden = encrypt(sityva)
        lives = 6
        guessed_letters = []

        while lives > 0 and "_" in hidden:
            game = input("Please enter a letter: ").lower()

            if not game.isalpha() or len(game) != 1:
                print("Invalid input. Enter a single letter (a-z).")
                continue

            if game in guessed_letters:
                print("You already guessed that letter.")
                continue

            guessed_letters.append(game)
            lives = guesser(game, sityva, hidden, lives)

            if "_" not in hidden:
                print("You won!")
                show_message("You won!", "green")  # turtle model
                break

            if lives == 0:
                print(f"Game Over! The word was: '{sityva}'.")
                show_message("You lost! Try again!", "red")  # turtle model
                break

        if not play_again():
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()

