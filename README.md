# AI Assignment: Importance of Sensing Strategies in Reconnaissance Chess Agents

This repository contains the code and documentation for an AI assignment focused on the importance of sensing strategies in reconnaissance chess agents. The project involves developing a baseline chess agent using the Reconchess framework, implementing enhancements to create an improved agent, and evaluating their performance against each other and reference bots.

## Table of Contents

- [Introduction](#introduction)
- [Methodology](#methodology)
- [Sensing Strategy Improvements](#sensing-strategy-improvements)
- [Results](#results)
- [Conclusion](#conclusion)
- [Usage](#usage)
- [Contributors](#contributors)

## Introduction

The objective of this project is to compare the performance of different chess agents, with a focus on the effect of improvements made to the sensing strategy in the ImprovedAgent. All the bots, except for RandomBot, use Stockfish as part of their move selection policy, but each bot applies a unique sensing strategy.

## Methodology

Both RandomSensing and ImprovedAgent use a combination of move selection strategies with Stockfish to reduce the number of possible boards and moves. These strategies include majority voting, move filtering, king capture, piece-specific strategies, and capture handling.

## Sensing Strategy Improvements

The primary enhancement in ImprovedAgent revolves around its sensing strategy. Instead of selecting sensing moves randomly like RandomSensing, ImprovedAgent employs a more robust approach to minimize uncertainty about the opponent's board state. It calculates the number of unknown pieces for each square on the board and selects the sensing square that minimizes the total number of unknown pieces in the surrounding 3x3 region.

## Results

A round-robin tournament was conducted involving all four bots. The findings of the tournament showed that RandomSensing surpassed RandomBot, TroutBot proved superior to RandomSensing, and ImprovedAgent demonstrated strong performance against all other bots, suggesting the significance of the improved sensing strategy.

## Conclusion

The development of the RandomSensing agent provided a solid foundation for understanding the core aspects of reconnaissance chess. However, the implementation of an improved sensing strategy in the ImprovedAgent highlighted the significance of strategic sensing in reducing uncertainty and improving overall performance.

## Usage

To run the chess agents and conduct your own experiments, follow these steps:

1. Clone the repository: `git clone https://github.com/yourusername/chess-agents.git`
2. Run the desired chess agent: `python agent_name.py`
3. Analyze the results and compare the performance of different agents.

## Contributors

- Altaaf Ally (2424551)
- Rayhaan Hanslod (2430979)
- Hamdullah Dadabhoy (2441030)

Feel free to contribute to this project by submitting pull requests or opening issues for any improvements or bug fixes.
