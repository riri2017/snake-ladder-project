import random


def roll_dice():
    """Return a random dice roll from 1 to 6."""
    return random.randint(1, 6)


def show_board_info(snakes, ladders):
    """Display all snake and ladder locations."""
    print("\nSnake Locations:")
    for head, tail in snakes.items():
        print(f"{head} -> {tail}")

    print("\nLadder Locations:")
    for bottom, top in ladders.items():
        print(f"{bottom} -> {top}")
    print()


def print_board(player1_pos, player2_pos, snakes, ladders, p1_name, p2_name):
    """Display a visual 10x10 Snake and Ladder board with colored player symbols."""
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

    p1_symbol = p1_name[:2].upper()
    p2_symbol = p2_name[:2].upper()

    print("\n========== BOARD ==========")

    rows = []
    num = 100

    for row in range(10):
        current_row = []

        for col in range(10):
            cell_num = num - col

            if cell_num == player1_pos and cell_num == player2_pos:
                symbol = f"{GREEN}{p1_symbol}{RESET}/{RED}{p2_symbol}{RESET}"
            elif cell_num == player1_pos:
                symbol = f"{GREEN}{p1_symbol}{RESET}"
            elif cell_num == player2_pos:
                symbol = f"{RED}{p2_symbol}{RESET}"
            elif cell_num in snakes:
                symbol = " S "
            elif cell_num in ladders:
                symbol = " L "
            else:
                symbol = f"{cell_num:>3}"

            current_row.append(f"{symbol:^6}")

        if row % 2 == 1:
            current_row.reverse()

        rows.append(current_row)
        num -= 10

    for row in rows:
        print(" | ".join(row))
        print("-" * 95)

    print(
        f"{GREEN}{p1_symbol}{RESET} = {p1_name}   "
        f"{RED}{p2_symbol}{RESET} = {p2_name}   "
        f"{GREEN}{p1_symbol}{RESET}/{RED}{p2_symbol}{RESET} = Both Players   "
        f"S = Snake   L = Ladder\n"
    )


def apply_snake_or_ladder(position, snakes, ladders):
    """Apply snake or ladder effect if present."""
    if position in snakes:
        new_position = snakes[position]
        print(f"Oops! Snake at {position}. Slide down to {new_position}.")
        return new_position

    if position in ladders:
        new_position = ladders[position]
        print(f"Nice! Ladder at {position}. Climb up to {new_position}.")
        return new_position

    return position


def move_player(player_name, current_position, snakes, ladders):
    """Move a player based on dice roll and board rules."""
    input(f"{player_name}, press Enter to roll the dice...")
    dice = roll_dice()
    print(f"{player_name} rolled a {dice}.")

    if current_position + dice > 100:
        print(f"{player_name} cannot move because the roll goes past 100.")
        print(f"{player_name} stays at {current_position}.\n")
        return current_position

    current_position += dice
    print(f"{player_name} moved to {current_position}.")

    current_position = apply_snake_or_ladder(current_position, snakes, ladders)
    print(f"{player_name} is now at {current_position}.\n")

    return current_position


def get_player_names():
    """Ask both players for their names."""
    player1 = input("Enter the name of Player 1: ").strip()
    player2 = input("Enter the name of Player 2: ").strip()

    if player1 == "":
        player1 = "Player 1"
    if player2 == "":
        player2 = "Player 2"

    return player1, player2


def ask_replay():
    """
    Ask the user if they want to play again.

    Pressing Enter with no input will be treated as 'no' so the game exits cleanly.
    """
    while True:
        choice = input("Do you want to play again? (yes/no): ").strip().lower()

        if choice == "" or choice == "no" or choice == "n":
            return False

        if choice == "yes" or choice == "y":
            return True

        print("Invalid input. Please enter yes or no.")


def play_game(player1_name, player2_name):
    """Run one round of Snake & Ladder and return the winner's name."""
    snakes = {
        16: 6,
        48: 30,
        62: 19,
        88: 24,
        95: 56,
        97: 78
    }

    ladders = {
        3: 22,
        20: 38,
        27: 84,
        36: 57,
        51: 72,
        71: 92
    }

    player1_position = 1
    player2_position = 1
    current_player = 1

    print("\n--- New Game Started ---")
    print("Both players start at position 1.")
    print("A player must reach exactly 100 to win.")
    show_board_info(snakes, ladders)

    while True:
        print_board(
            player1_position,
            player2_position,
            snakes,
            ladders,
            player1_name,
            player2_name
        )
        print(f"{player1_name}: {player1_position} | {player2_name}: {player2_position}")
        print("-" * 30)

        if current_player == 1:
            player1_position = move_player(
                player1_name,
                player1_position,
                snakes,
                ladders
            )
            if player1_position == 100:
                print_board(
                    player1_position,
                    player2_position,
                    snakes,
                    ladders,
                    player1_name,
                    player2_name
                )
                print(f"Congratulations! {player1_name} wins this round!\n")
                return player1_name
            current_player = 2
        else:
            player2_position = move_player(
                player2_name,
                player2_position,
                snakes,
                ladders
            )
            if player2_position == 100:
                print_board(
                    player1_position,
                    player2_position,
                    snakes,
                    ladders,
                    player1_name,
                    player2_name
                )
                print(f"Congratulations! {player2_name} wins this round!\n")
                return player2_name
            current_player = 1


def main():
    """Run the full game with replay and scoreboard."""
    player1_name, player2_name = get_player_names()

    scores = {
        player1_name: 0,
        player2_name: 0
    }

    while True:
        winner = play_game(player1_name, player2_name)
        scores[winner] += 1

        print("=== SCOREBOARD ===")
        for player, wins in scores.items():
            print(f"{player}: {wins} wins")
        print("==================\n")

        if not ask_replay():
            break

        print()

    print("\nFinal Scores:")
    for player, wins in scores.items():
        print(f"{player}: {wins} wins")

    print("\nThanks for playing Snake & Ladder!")


if __name__ == "__main__":
    main()
