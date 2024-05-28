# PipeMania

## Artificial Intelligence Project

This project involves solving a grid-based puzzle similar to Pipe Mania. The goal is to ensure water flows through all the pipes on the board without creating any cycles. This project implements various algorithms to explore the board and check connectivity.

<p align="center">
  <img src="report/test15/Figure_0.png" alt="Puzzle Before" width="300" />
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="report/test15/Figure_15.png" alt="Puzzle After" width="300" />
</p>
<p align="center">
  Fig1. Before solving the puzzle. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Fig2. After solving the puzzle.
</p>


### Getting Started

Clone the repository to your local machine using the following command in your terminal or command prompt:

```bash
git clone https://github.com/mariamfmr/pipemania-ai/
```

### Dependencies

The project uses **Python3** and requires the following dependencies:

    numpy: For numerical operations and handling grids efficiently.
    matplotlib: For plotting and visualizations.
    pandas: For handling CSV files and data manipulation.
    colorama: Used for colored terminal output to enhance readability and highlight explored pipes.
    Jupyter: For creating and running Jupyter notebooks.

To install all the dependencies, run:

    pip install -r src/requirements.txt

Ensure you have **Python3** installed on your system before setting up and installing dependencies.

### Project Structure

The project repository contains the following structure:
  
    src: Code to solve the game. Contains the logic for the actions and result implemented by the search algorithms.
    report: A jupyter notebook with the analysis of algorithms' perfomance and the csv tables with the data.
    tests: A set of tests for testing the code.
    visualizer: Code for visualizing the board state and other relevant data.

### Run the application:

To run the program on all inputs:

    make clean
    make run

To run the program on a specific input:

    python3 src/pipe.py < tests/test-xx.txt 

To run the program on a specific input with colorama:

    python3 src/pipe_colorama.py < tests/test-xx.txt

### Conclusion

We solved the PipeMania with multiple algorithms as shown in the report, however the one that performed best was the greedy search with an efficient heuristic. More can be found in **report/analysis**.
