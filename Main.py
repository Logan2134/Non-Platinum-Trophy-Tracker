def display_list(filename):
    """Display the formatted list of games sorted by completion percentage."""
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        games = []

        for line in lines:
            # Strip whitespace from the line
            line = line.strip()

            # Skip empty lines or lines that don't contain trophy data
            if not line or '(' not in line or 'Trophies' not in line:
                continue

            # Split the line into game name and trophy data
            parts = line.rsplit('(', 1)
            game_name = parts[0].strip()
            trophy_data = parts[1].split(')')[0].replace("Trophies", "").strip()

            # Extract the number of trophies completed and total trophies
            try:
                completed, total = map(int, trophy_data.split(' of '))
            except ValueError:
                print(f"Skipping invalid entry: {line}")
                continue

            # Calculate the completion percentage and round it to a float (not string)
            if total == 0:  # Avoid division by zero
                completion_percent = 0.0
            else:
                completion_percent = (completed / total) * 100  # Calculate as float

            # Store game data as a tuple (name, completed, total, percent)
            games.append((game_name, completed, total, completion_percent))

        # Remove duplicates by converting the list of tuples to a set and back to a list
        # This ensures each game is only processed once
        games = list({game[0]: game for game in games}.values())

        # Sort the games list by completion percentage (ascending order)
        games.sort(key=lambda game: game[3])  # Sort by the 4th item (completion percent)

        # Print table header
        print(f"{'Name:':<35} {'Trophy:':<25} {'Percent:'}")
        print("-" * 70)

        for game_name, completed, total, completion_percent in games:
            # Format and print each row
            print(f"{game_name:<35} {completed} out of {total:<20} {completion_percent:.2f}%")

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except ValueError as ve:
        print(f"Data formatting error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")



def modify_list(filename):
    """Allow the user to modify the list."""
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        game_data = {}
        for line in lines:
            if '(' in line and 'Trophies' in line:
                parts = line.rsplit('(', 1)
                game_name = parts[0].strip()
                trophy_data = parts[1].split(')')[0].replace("Trophies", "").strip()
                completed, total = map(int, trophy_data.split(' of '))
                game_data[game_name] = (completed, total)

        while True:
            print("\n--- Modify List ---")
            print("1. Update trophies for an existing game")
            print("2. Add a new game")
            print("3. Back to main menu")

            choice = input("Enter your choice: ").strip()

            if choice == '1':
                # Update an existing game
                game_name = input("Enter the name of the game to update: ").strip()
                if game_name in game_data:
                    new_completed = input(f"Enter new completed trophies (current: {game_data[game_name][0]}): ").strip()
                    new_total = input(f"Enter new total trophies (current: {game_data[game_name][1]}): ").strip()

                    if not new_completed.isdigit() or not new_total.isdigit():
                        print("Invalid input. Completed and total trophies must be numbers.")
                        continue

                    game_data[game_name] = (int(new_completed), int(new_total))
                    print(f"Updated {game_name}: {new_completed} of {new_total} trophies.")
                else:
                    print(f"Game '{game_name}' not found in the list.")

            elif choice == '2':
                # Add a new game
                game_name = input("Enter the name of the new game: ").strip()
                if game_name in game_data:
                    print(f"Game '{game_name}' already exists in the list.")
                    continue

                new_completed = input("Enter completed trophies: ").strip()
                new_total = input("Enter total trophies: ").strip()

                if not new_completed.isdigit() or not new_total.isdigit():
                    print("Invalid input. Completed and total trophies must be numbers.")
                    continue

                game_data[game_name] = (int(new_completed), int(new_total))
                print(f"Added {game_name}: {new_completed} of {new_total} trophies.")

            elif choice == '3':
                # Save changes and exit
                with open(filename, 'w') as file:
                    for game, (completed, total) in game_data.items():
                        file.write(f"{game} ({completed} of {total} Trophies)\n")
                print("Changes saved. Returning to main menu.")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    filename = "NoPlatinum.txt"

    while True:
        print("\n--- Trophy Tracker ---")
        print("1. View List")
        print("2. Modify List")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            display_list(filename)
        elif choice == '2':
            modify_list(filename)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


# Run the program
if __name__ == "__main__":
    main()
