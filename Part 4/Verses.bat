@echo off

REM THIS IS USED TO PLAY MULTIPLE GAMES BETWEEN TWO BOTS
REM RESULTS GET SAVED IN THE game_results FOLDER

REM Define number of games
set num_games=10

REM Set the path to the game results folder
set results_folder=C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 4\game_results

REM Delete existing files in the game results folder, if it exists
if exist "%results_folder%" (
    del /q "%results_folder%\*"
) else (
    mkdir "%results_folder%"
)

REM Set the path to the Python scripts
REM set MyBot=C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 4\RandomSensing.py
set MyBot=C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 4\Improved Agent\ImprovedAgentDraft.py
set TroutBot=C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 4\TroutBot.py
REM "%TroutBot%"
REM Loop to run multiple games
for /l %%i in (1, 1, %num_games%) do (
    rc-bot-match reconchess.bots.random_bot "%MyBot%"  > "%results_folder%\game%%i_result.txt"
)
