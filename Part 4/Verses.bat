
REM THIS IS USED TO PLAY MULTIPLE GAMES BETWEEN TWO BOTS
REM RESULTS GET SAVED IN THE game_results FOLDER

REM Define number of games
set num_games=10

REM Set the path to the game results folder
set results_folder=D:\Wits\Honours\AI\AI-Assignment\Part 4\game_results

REM Define the consolidated results file
@REM set consolidated_results=%results_folder%\Results_RandomBot_vs_ImprovedBot.txt
set consolidated_results=%results_folder%\Results_TroutBot_vs_ImprovedAgent.txt
REM Delete existing files in the game results folder, if it exists
if exist "%results_folder%" (
    del /q "%results_folder%\*"
) else (
    mkdir "%results_folder%"
)

@REM REM Clear the consolidated results file if it exists
@REM if exist "%consolidated_results%" (
@REM     del "%consolidated_results%"
@REM )

REM Set the path to the Python scripts
set MyBot=D:\Wits\Honours\AI\AI-Assignment\Part 4\Improved Agent\ImprovedAgent.py
set MyBotImproved =D:\Wits\Honours\AI\AI-Assignment\Part 4\RandomSensing.py
set TroutBot=D:\Wits\Honours\AI\AI-Assignment\Part 4\TroutBot.py

REM Loop to run multiple games
for /l %%i in (1, 1, %num_games%) do (
    echo Match %%i >> "%consolidated_results%"
    echo White: Trout_bot, Black: RandomSensingBot >> "%consolidated_results%"
    rc-bot-match "%TroutBot%" "%MyBot%" > "%results_folder%\game%%i_result.txt"
    type "%results_folder%\game%%i_result.txt" >> "%consolidated_results%"
    echo. >> "%consolidated_results%"
)

echo All matches have been completed and results are saved in %consolidated_results%.
pause
