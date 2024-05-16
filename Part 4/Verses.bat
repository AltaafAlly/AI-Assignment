@REM @echo off

@REM REM THIS IS USED TO PLAY MULTIPLE GAMES BETWEEN TWO BOTS
@REM REM RESULTS GET SAVED IN THE game_results FOLDER

@REM REM Define number of games
@REM set num_games=6

@REM REM Set the path to the game results folder
@REM set results_folder=C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 4\game_results

@REM REM Delete existing files in the game results folder, if it exists
@REM if exist "%results_folder%" (
@REM     del /q "%results_folder%\*"
@REM ) else (
@REM     mkdir "%results_folder%"
@REM )

@REM REM Set the path to the Python scripts
@REM set MyBot=C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 4\RandomSensing.py
@REM set MyBotImproved =C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 4\Improved Agent\ImprovedAgentDraft.py
@REM set TroutBot=C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 4\TroutBot.py
@REM REM "%MyBotImproved%""%TroutBot%"
@REM REM 
@REM REM Loop to run multiple games
@REM for /l %%i in (1, 1, %num_games%) do (
@REM     rc-bot-match reconchess.bots.random_bot "%MyBot%"  > "%results_folder%\game%%i_result.txt"
@REM )


@echo off

REM THIS IS USED TO PLAY MULTIPLE GAMES BETWEEN TWO BOTS
REM RESULTS GET SAVED IN THE game_results FOLDER

REM Define number of games
set num_games=6

REM Set the path to the game results folder
set results_folder=C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 4\game_results

REM Define the consolidated results file
set consolidated_results=%results_folder%\all_games_results.txt

REM Delete existing files in the game results folder, if it exists
if exist "%results_folder%" (
    del /q "%results_folder%\*"
) else (
    mkdir "%results_folder%"
)

REM Clear the consolidated results file if it exists
if exist "%consolidated_results%" (
    del "%consolidated_results%"
)

REM Set the path to the Python scripts
set MyBot=C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 4\RandomSensing.py
set MyBotImproved=C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 4\Improved Agent\ImprovedAgentDraft.py
set TroutBot=C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 4\TroutBot.py

REM Loop to run multiple games
for /l %%i in (1, 1, %num_games%) do (
    echo Match %%i >> "%consolidated_results%"
    echo White: Random_bot, Black: RandomSensingBot >> "%consolidated_results%"
    rc-bot-match reconchess.bots.random_bot "%MyBot%" > "%results_folder%\game%%i_result.txt"
    type "%results_folder%\game%%i_result.txt" >> "%consolidated_results%"
    echo. >> "%consolidated_results%"
)

echo All matches have been completed and results are saved in %consolidated_results%.
pause
