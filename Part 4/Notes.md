#Stuff we did to our bot so far

- Used the trout bot a basline to help put bot to make moves 
- prioritize_sensing_actions, which generates a list of prioritized sensing actions based on the current game state and strategic considerations. The choose_sense method then selects a sensing action based on the prioritized list if available, otherwise, it falls back to choosing a sense action randomly. The handle_sense_result method is kept to update the bot's board with the sensed information as before.