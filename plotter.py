import csv
import matplotlib.pyplot as plt

# Read the CSV data
with open('data.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    data = list(csv_reader)

# Get the list of unique bots
bots = list(set(row['White Player'] for row in data) | set(row['Black Player'] for row in data))

# Initialize a dictionary to store win counts
win_counts = {bot: {opponent: 0 for opponent in bots if opponent != bot} for bot in bots}

# Calculate the win counts
for row in data:
    white_player = row['White Player']
    black_player = row['Black Player']
    winner = row['Winner']

    if winner == 'White':
        win_counts[white_player][black_player] += 1
    elif winner == 'Black':
        win_counts[black_player][white_player] += 1

# Assign specific colors to each bot
color_map = {
    'RandomBot': '#1f77b4',
    'RandomSensing': '#ff7f0e',
    'TroutBot': '#2ca02c',
    'ImprovedAgent': '#d62728'
}

# Create the joint bar graph
fig, ax = plt.subplots(figsize=(10, 8))

bar_width = 0.8 / (len(bots) - 1)
opacity = 0.8

for i, bot in enumerate(bots):
    bot_wins = [win_counts[bot].get(opponent, 0) for opponent in bots if opponent != bot]
    bot_positions = [i + j * bar_width for j in range(len(bots) - 1)]
    ax.bar(bot_positions, bot_wins, bar_width, alpha=opacity, color=[color_map[opponent] for opponent in bots if opponent != bot])

ax.set_xlabel('Bot')
ax.set_ylabel('Number of Wins')
ax.set_title('Win Counts of Each Bot against Every Other Bot')
ax.set_xticks([i + (len(bots) - 2) * bar_width / 2 for i in range(len(bots))])
ax.set_xticklabels(bots)

# Create a custom legend
legend_elements = [plt.Rectangle((0, 0), 1, 1, facecolor=color_map[bot], edgecolor='none', alpha=opacity) for bot in bots]
ax.legend(legend_elements, bots, title='Bot', bbox_to_anchor=(0.15, -0.09), loc='best')

plt.tight_layout()
plt.show()