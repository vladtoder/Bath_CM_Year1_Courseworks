import sys
import random


# This function checks if the provided guess is valid.
def is_valid_code(words, code_length, colours):
    return len(words) == code_length and all(word in colours for word in words)


# This function compares the player's guess with the actual code and returns feedback.
def compare_guess_with_code(guess, code, colours, code_length):
    if not is_valid_code(guess, code_length, colours):
        return "Ill-formed guess provided"

    remaining_code = list(code)
    black_pegs = 0
    white_pegs = 0

    # Calculate black pegs (correct color in correct position).
    for i in range(code_length):
        if guess[i] == remaining_code[i]:
            black_pegs += 1
            remaining_code[i] = None

    # Calculate white pegs (correct color in wrong position).
    for i in range(code_length):
        if guess[i] != code[i] and guess[i] in remaining_code:
            white_pegs += 1
            remaining_code[remaining_code.index(guess[i])] = None

    peg_results = ["black"] * black_pegs + ["white"] * white_pegs
    result = " ".join(peg_results).strip()

    if black_pegs == code_length:
        return f"You won in {black_pegs} guesses. Congratulations!"
    
    return result


# Generates a random guess based on the available colours and code length.
def generate_random_guess(available_colours, code_length):
    return [random.choice(available_colours) for _ in range(code_length)]


# Processes the game by reading guesses, comparing them, and writing the results.
def process_game(input_file, output_file, code_length, maximum_guesses, available_colours, player_type):
    with open(input_file, "r") as file:
        lines = file.readlines()

    code = lines[0].strip().split()[1:]
    results = []
    game_won = False

    # If the player is computer, generate guesses up to the maximum allowed.
    if player_type == "computer":
        lines = lines[:2]  # Keep only the first two lines (code and player)
        for _ in range(maximum_guesses):
            computer_guess = generate_random_guess(available_colours, code_length)
            lines.append(' '.join(computer_guess))
    
    # Process each guess and provide feedback.
    for guess_number, guess_line in enumerate(lines[2:], start=1):
        if guess_number > maximum_guesses:
            break  # Stop if maximum guesses are reached

        guess = guess_line.strip().lower().split()
        guess_result = compare_guess_with_code(guess, code, available_colours, code_length)
        results.append(f"Guess {guess_number}: {guess_result}")
        
        if "won" in guess_result:
            game_won = True
            results[-1] = f"Guess {guess_number}: " + " ".join(["black"] * code_length)
            results.append(f"You won in {guess_number} guesses. Congratulations!")
            break

    # Provide final game results.
    if not game_won:
        results.append("You lost. Please try again.")
        if guess_number > maximum_guesses:
            results.append(f"You can only have {maximum_guesses} guesses.")
        
    if game_won and len(lines[2:]) > guess_number:
        results.append("The game was completed. Further lines were ignored.")
        
    # Write the game results to the output file.
    with open(output_file, "w") as file:
        for result in results:
            file.write(f"{result}\n")

    # If computer was the player, log the game for analysis.
    if player_type == "computer":
        with open("computerGame.txt", "w") as file:
            file.write(f"code {' '.join(code)}\n")
            file.write("player human\n")
            for guess in lines[2:]:
                file.write(' '.join(guess.split()) + "\n")

    return results


# Main function to handle command line inputs and run the game.
def main():
    if len(sys.argv) < 3:
        print("Not enough programme arguments provided")
        sys.exit(1)
        
    # Extracting command line arguments.
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    code_length = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    maximum_guesses = int(sys.argv[4]) if len(sys.argv) > 4 else 12
    available_colours = sys.argv[5:] if len(sys.argv) > 5 else ["red", "blue", "yellow", "green", "orange"]

    try:
        with open(input_file, "r") as file:
            lines = file.readlines()
            
        code = lines[0].strip().split()[1:]
        if not lines[0].startswith("code") or len(code) != code_length:
            with open(output_file, "w") as file:
                file.write("No or ill-formed code provided\n")
            sys.exit(4)

        player_line = lines[1].strip().lower()
        if player_line not in ["player human", "player computer"]:
            with open(output_file, "w") as file:
                file.write("No or ill-formed player provided\n")
            sys.exit(5)

        process_game(input_file, output_file, code_length, maximum_guesses, available_colours, player_line.split()[1])

    except FileNotFoundError:
        print("There was an issue with the input file")
        sys.exit(2)
    except IOError:
        print("There was an issue with the output file")
        sys.exit(3)

    sys.exit(0)

if __name__ == "__main__":
    main()


        
        


            

            



