import os
import subprocess
import datetime

# Define the paths to the bot scripts (replace with the actual paths)
random_bot_path = "D:\Wits\Honours\AI\AI-Assignment\Part 4\RandomBot.py"
trout_bot_path = "D:\Wits\Honours\AI\AI-Assignment\Part 4\TroutBot.py"
random_sensing_path = "D:\Wits\Honours\AI\AI-Assignment\Part 4\RandomSensing.py"
# improved_agent_path = "path/to/improved_agent.py"

# Define the bots participating in the tournament
bots = [
    ("RandomSensing", random_sensing_path),
    ("RandomBot", random_bot_path)
    # ("TroutBot", trout_bot_path)
    # ("ImprovedAgent", improved_agent_path)
]

# Define the number of matches to play between each pair of bots
num_matches = 10

# Create a file to store the tournament results
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
results_file = f"tournament_results_{timestamp}.txt"

# Run the round-robin tournament
with open(results_file, "w") as file:
    for white_bot, white_bot_path in bots:
        for black_bot, black_bot_path in bots:
            if white_bot != black_bot:
                for match_num in range(1, num_matches + 1):
                    print(f"Match {match_num}: {white_bot} (White) vs {black_bot} (Black)")
                    file.write(f"Match {match_num}: {white_bot} (White) vs {black_bot} (Black)\n")

                    start_time = datetime.datetime.now()
                    result = subprocess.run(["rc-bot-match", white_bot_path, black_bot_path], capture_output=True, text=True)
                    end_time = datetime.datetime.now()

                    game_duration = end_time - start_time
                    minutes, seconds = divmod(game_duration.total_seconds(), 60)
                    game_status = "Completed" if result.returncode == 0 else "Crashed"
                    winner = "White" if "white!" in result.stdout else "Black" if "black!" else "Error" if "ERROR!" in result.stdout else "Draw"

                    file.write(f"Game Duration: {int(minutes)} minutes {int(seconds)} seconds\n")
                    file.write(f"Game Status: {game_status}\n")
                    file.write(f"Winner: {winner}\n")
                    file.write(f"Stdout:\n{result.stdout}\n")
                    file.write(f"Stderr:\n{result.stderr}\n")
                    file.write("\n")

                    print(f"Game Duration: {int(minutes)} minutes {int(seconds)} seconds")
                    print(f"Game Status: {game_status}")
                    print(f"Winner: {winner}")
                    print()

print(f"Tournament completed! Results saved to {results_file}")