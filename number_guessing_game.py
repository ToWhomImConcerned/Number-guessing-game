import time   #import current PC time
import random   #generates a random digit

def set_difficulty(difficulty):
    if difficulty == "easy":
        max_number = 100
        max_attempts = 8
        time_limit = 90
    elif difficulty == "medium":
        max_number = 200
        max_attempts = 7
        time_limit = 60
    elif difficulty == "hard":
        max_number = 300
        max_attempts = 6
        time_limit = 45
    elif difficulty == "hardcore":
        max_number = 250
        max_attempts = 5
        time_limit = 30
    else:
        print("Invalid choice, defaulting to easy.")
        max_number = 100
        max_attempts = 8
        time_limit = 90

    return max_number, max_attempts, time_limit

def display_intro(difficulty, max_number, max_attempts, time_limit):
    print(f"I'm thinking of a number between 1 and {max_number}.")
    print(f"You have {max_attempts} attempts to guess the number and {time_limit} seconds to complete the round.")
    if difficulty != "hardcore":
        print("Type 'quit' anytime to exit, or 'hint' for up to 3 hints at a cost.")
    if difficulty == "hardcore":
        print("No hints, keep the streak to stay alive!")
        print("Type 'quit' anytime to exit.")

def get_hint(difficulty, available_hints, attempts, max_attempts, number, max_number):
    if difficulty != "hardcore":    #this makes it only let you use hints when not in hardcore mode
            if len(available_hints) == 0:
                print(f"You've used up all your hints! {max_attempts - attempts} attempts remaining.")
                return available_hints, attempts
            hint_type = random.choice(available_hints)
            available_hints.remove(hint_type)
            if hint_type == "even_odd":
                if number % 2 == 0:
                    print(f"The number is even! {len(available_hints)} hints remaining, {max_attempts - attempts} attempts remaining.")
                else:
                    print(f"The number is odd! {len(available_hints)} hints remaining, {max_attempts - attempts} attempts remaining.")
                return available_hints, attempts
            elif hint_type == "range":
                lower = max(1, number - 10)
                upper = min(max_number, number + 10)
                print(f"The number is between {lower} and {upper}! {len(available_hints)} hints remaining, {max_attempts - attempts} attempts remaining.")
                return available_hints, attempts
            elif hint_type == "divisible":
                if number % 3 == 0:
                    print(f"The number is divisible by 3! {len(available_hints)} hints remaining, {max_attempts - attempts} attempts remaining.")
                elif number % 5 == 0:
                    print(f"The number is divisible by 5! {len(available_hints)} hints remaining, {max_attempts - attempts} attempts remaining.")
                elif number % 7 == 0:
                    print(f"The number is divisible by 7! {len(available_hints)} hints remaining, {max_attempts - attempts} attempts remaining.")
                else:
                    print(f"The number is not divisible by 3, 5, or 7! {len(available_hints)} hints remaining, {max_attempts - attempts} attempts remaining.")
                return available_hints, attempts

            return available_hints, attempts
        
def process_guess(user_input, max_attempts, attempts): #marks any input that isnt hint, quit, or a number between 1 and max number as invalid and makes you try again.
        try:
            guess = int(user_input)
            return guess
        except ValueError:
            print(f"Please enter a valid number! {max_attempts - attempts} attempts remaining.")
            return None
        
def check_proximity(guess, number, max_attempts, attempts):
        difference = abs(guess - number) #track how far the guess is from the correct number
        #if guess is 10, 20, or 30 lower than the correct number it gives you small hints accordingly.
        if guess < number:
            if difference <= 10:
                print(f"Too low... but VERY close! 🔥 {max_attempts - attempts} attempts remaining.")
            elif difference <= 20:
                print(f"Too low... but close! 🔥 {max_attempts - attempts} attempts remaining.")
            elif difference <= 30:
                print(f"Too low... but getting there! 👀 {max_attempts - attempts} attempts remaining.")
            else:
                print(f"Too low! {max_attempts - attempts} attempts remaining.")
        elif guess > number:
            if difference <= 10:
                print(f"Too high... but VERY close! 🔥 {max_attempts - attempts} attempts remaining.")
            elif difference <= 20:
                print(f"Too high... but close! 🔥 {max_attempts - attempts} attempts remaining.")
            elif difference <= 30:
                print(f"Too high... but getting there! 👀 {max_attempts - attempts} attempts remaining.")
            else:
                print(f"Too high! {max_attempts - attempts} attempts remaining.") #if guess is 10, 20, or 30 higher than the correct number it gives you small hints accordingly.

def display_win(wins, streak, last_difficulty, best_streak, best_attempts, difficulty, max_attempts, losses, attempts):
            wins += 1
            streak += 1

            if streak > best_streak:
                best_streak = streak

            streak_message = "No streak yet, keep going!" if streak <= 1 else f"Win streak - {streak}" #ternary operator one line if/else that assigns a value based on a condition
            best_streak_message = "No best streak yet!" if best_streak <= 1 else f"Best streak - {best_streak}"

            if difficulty == "hardcore":
                last_difficulty = "hardcore"
                print(f"Keep up the streak, you got it in {attempts} tries! 🎉  {streak_message}")

            if best_attempts is None or attempts < best_attempts: # if no best score exists yet, set it. Or if current is better, update it.
                best_attempts = attempts

            if difficulty != "hardcore":
                if attempts <= max_attempts / 2:   #get under max_attempts divided by 2 to get 3 stars
                    print("⭐⭐⭐ Amazing!")
                elif attempts <= max_attempts - 2:
                    print("⭐⭐ Not Bad!")   #get under max_attempts minus 2 to get 2 stars
                else:
                    print("⭐ Close call!") #everything else besides a loss is a close call

                print(f"You got it in {attempts} tries! 🎉  wins - {wins}, losses - {losses}, {streak_message}")
                print(best_streak_message)
                print(f"Lowest number of attempts - {best_attempts}")
                    # ALWAYS RETURN
            return wins, streak, last_difficulty, best_streak, best_attempts
            
def display_loss(wins, best_attempts, number, attempts, streak, best_streak, max_attempts, timed_out, cheated, losses, difficulty, game_running):
        streak_message = "No streak yet, keep going!" if streak <= 1 else f"Win streak - {streak}" #ternary operator one line if/else that assigns a value based on a condition
        best_streak_message = "No best streak yet!" if best_streak <= 1 else f"best streak - {best_streak}"
        losses += 1
        streak = 0
        if difficulty == "hardcore":   #if you lose when in hardcore mode this makes the game end automatically, bypassing the play again option.
            game_running = False
            print(f"Failed to keep up the streak, game over! 💀  {number} was the correct answer!")
        elif timed_out and not cheated:
            print(f"You ran out of time! ⏱️   Game over! {number} was the correct answer!")
        elif cheated:
            print(f"{number} is the answer you cheater! Taking the loss! 💀  ")
        else:
            print(f"You ran out of tries, game over! 💀  {number} was the correct answer! wins - {wins}, losses - {losses}, {streak_message}")
            print(best_streak_message)
        if best_attempts is not None:
            print(f"Lowest number of attempts - {best_attempts}")
        else:
            print("No wins yet, set a lowest attempts record!")

        return losses, streak, best_attempts, game_running
    


game_running = True

print("Welcome to the Number Guessing Game!") #prints once at the beginning of the game and doesn't repeat when user plays again

wins = 0
losses = 0
streak = 0
best_streak = 0
best_attempts = None
last_difficulty = ""     #defines variables used throughout the game

while game_running:

    if last_difficulty == "hardcore":    #if user wins in hardcore mode, automatically choose hardcore again so they have to keep the win streak to stay alive.
        difficulty = "hardcore"

    else:
        difficulty = input("Choose difficulty (easy/medium/hard/hardcore): ").lower()   #list of difficulty to choose from, .lower() makes it not case sensitive.

    max_number, max_attempts, time_limit = set_difficulty(difficulty)

    number = random.randint(1, max_number)   #this is what tells the random digit to be a number, 1 through whatever the max number is depending on difficulty.
    guess = 0
    attempts = 0
    timed_out = False
    first_guess = True   #makes the first guess start the timer instead of at the beginning of the game
    cheated = False

    if difficulty == "hardcore" and last_difficulty == "hardcore":
        input("Another round? Press enter when ready! 🔥 ")   #makes it so after winning in hardcore, it doesnt ask for a new guess in a new game immediately, must input ready first.

    display_intro(difficulty, max_number, max_attempts, time_limit)

    available_hints = ["even_odd", "range", "divisible"]   #list of hint types it can randomly choose from when user input is hint

    while guess != number and attempts < max_attempts:
        user_input = input("Enter your guess: ")
        if first_guess:
            start_time = time.time()
            first_guess = False
        elapsed = time.time() - start_time
        if elapsed >= time_limit:
            timed_out = True
            break
            #makes the game stop immediately when the user decides to quit
        if user_input == "quit":
            print("Quitting on me?")
            game_running = False
            break
            #cheat code the gives you the answer but also makes you lose
        if user_input == "letmewin":
            cheated = True
            timed_out = True
            break
        
        if difficulty != "hardcore":
            if user_input == "hint":
                attempts += 1
                available_hints, attempts = get_hint(difficulty, available_hints, attempts, max_attempts, number, max_number)
                continue

        guess = process_guess(user_input, max_attempts, attempts)
        if guess is None:
            continue
        attempts += 1

        check_proximity(guess, number, max_attempts, attempts)

    if guess == number:
        wins, streak, last_difficulty, best_streak, best_attempts = display_win(wins, streak, last_difficulty, best_streak, best_attempts, difficulty, max_attempts, losses, attempts)

    if not game_running:
        break

    if guess != number and (attempts >= max_attempts or timed_out):   #adds a loss and breaks the win streak if you time out or pass the attempt limit
        losses, streak, best_attempts, game_running = display_loss(wins, best_attempts, number, attempts, streak, best_streak, max_attempts, timed_out, cheated, losses, difficulty, game_running)

    if difficulty != "hardcore":
        play_again = input("Play again? (yes/no): ")   #makes it only ask play again when not in hardcore
        if play_again != "yes":
            print("Thanks for playing!")
            break