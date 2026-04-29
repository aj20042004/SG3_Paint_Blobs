# SG3 Paint Blobs Group Project
# Language - Python
# IDE - Developed in VScode, PyCharm & Thonny
#
# Python Packages Required:
# (In Thonny IDE add the following packages under "Tools > Manage Packages")
#
#
#
# Authors:
#   - Zachary Gmyr
#   - Mira Ysabela Ifurung
#   - Daniel McKinnis
#   - AJ Soma Ravichandran
#   - Devon Schrader
#
# Revision History:
#
#
# Course:
#   CS 4500 - Intro to the Software Profession
#
# Program Explanation:
#
#
# Data Structures:
#
#
# External Files Used:
#
#
# References Used:
#   - https://jakob-bagterp.github.io/colorist-for-python/ansi-escape-codes/effects/#cheat-sheet (underline text)




# /-- Helper Functions --/

#   DESCRIPTION:
#       Outputs information about blobs painted to the canvas in the current state, as stored in some data structure
#       (canvas) containing information on each square in an NxN grid. For each square in this grid, this data structure
#       should store the number of paint blobs by color (rgb), and the current blob (or last blob painted to this square).
#       Information displayed to the user includes:
#           1. total number of paint blobs dropped on the canvas so far
#           2. lowest, highest, and average # of paint blobs on a given square
#           3. total number of blobs for each color (rgb)
#           4. total number of squares painted with just one color
#       Should be called whenever a simulation ends (MaxT elapsed), or the first moment each square has one paint blob.
#   GLOBALS USED:
#       N/a
#   PARAMETERS:
#       totalBlobs -> total r+b+g blobs painted across entire canvas, or current time (seconds) in the simulation
#       (where 1 blob is painted per second). May be some value from NxN to MaxT of the given simulation.
#       N -> singular dimension of NxN grid used in this simulation.
#       canvas -> NxN grid storing {"red","green","blue","last"} key-values per square
#   RETURNS:
#       N/a
def GetStatistics(total_blobs, N, canvas):
    # determine total blob count by square
    totals_by_square = [sq["red"] + sq["green"] + sq["blue"] for sq in canvas]

    min_square_blobs = min(totals_by_square) # compute min/max/avg
    max_square_blobs = max(totals_by_square)
    avg_square_blobs = total_blobs / (N * N)

    # determine total blob count by color
    totals_by_color = {
        "red": sum(sq["red"] for sq in canvas),
        "green": sum(sq["green"] for sq in canvas),
        "blue": sum(sq["blue"] for sq in canvas),
    }

    # calculate number of single-colored squares in canvas
    total_one_color = 0
    colors = ["red", "green", "blue"]
    for sq in canvas:
        colors_this_sq = 0

        for color in colors:
            if sq[color] > 0:
                colors_this_sq += 1
        if colors_this_sq == 1:
            total_one_color += 1

    print(f"Canvas state at time t={total_blobs}:")
    print(f" > total of \x1b[4m{total_blobs}\x1b[24m blobs painted to the canvas")
    print(f" > lowest # blobs on a single square = \x1b[4m{min_square_blobs}\x1b[24m")
    print(f" > highest # blobs on a single square = \x1b[4m{max_square_blobs}\x1b[24m")
    print(f" > average of \x1b[4m{avg_square_blobs}\x1b[24m blobs per square")
    print(f" > color distribution: \x1b[4m{totals_by_color['red']}\x1b[24m Red, \x1b[4m{totals_by_color['green']}\x1b[24m Green, \x1b[4m{totals_by_color['blue']}\x1b[24m Blue")
    print(f" > total of \x1b[4m{total_one_color}\x1b[24m single-colored squares")


# /-- Main Driver --/

#   DESCRIPTION:
#       Main driver for SG3_Program.py
#   GLOBALS USED:
#       N/a
#   PARAMETERS:
#       N/a
#   RETURNS:
#       N/a
def main():

    print("""|==~ Paint Blobs Simulator ~==|
This program simulates random colored paint blobs dropping onto an initially empty NxN-sized canvas. Each simulation may
run for a given number of MaxT seconds, where every second a random color (red, green, or blue) may be randomly selected
and dropped onto the canvas & each square is equally likely to be painted. Every square in the canvas may store an RGB
count for each color dropped there, and multiple different colors dropped onto a single square do NOT mix together to
create other colors. Statistics will be reported for the canvas at two points during each simulation ran: (1) at the first
moment all squares have at least ONE paint blob, and/or (2) after the given MaxT seconds have elapsed and all blobs have
been dropped on the canvas.

Three experiments are conducted in the following order:
    1. An initial (single) simulation is ran, using a 10x10 sized grid (N) for 300 seconds (MaxT)

    2. A second (single) simulation is ran, using user-prompted values for an N-sized canvas, and MaxT seconds to run for.
    The user will be prompted with a final picture of the canvas after the simulation finishes.

    3. Ten simulations are ran after prompting the user to select either MaxT or N as an incrementing independent variable:
        3a. (N increments): the user is prompted for MaxT (which remains constant), an initial size N, and an N-increment
        from the choice of 1, 10, 100, or 1000. In each of the 10 simulations ran, the canvas size should grow while the
        MaxT time each simulation runs for remains constant. A following graph will illustrate summary statistics of paint
        blobs across the canvas in respect to a growing canvas size.
        
        3b. (MaxT increments): the user is prompted for N (which remains constant), an initial MaxT, and a T-increment
        from the choice of 1, 10, 100, or 1000. In each of the 10 simulations ran, every subsequent simulation should
        run longer than the previous while the canvas size remains constant. A following graph will illustrate summary
        statistics of paint blobs across the canvas in respect to an increasing simulation run time.
""")


    # /-- TESTING START --/
    # testing GetStatistics() function with hard-coded canvas states
    # 1. called at first moment all squares have at least one paint blob
    # 2. called when MaxT blobs have painted (t=MaxT)

    N = 2
    MaxT = 8

    # System State: first moment all squares have at least one paint blob (let t = 4)
    canvas = [
        {"red": 1, "green": 0, "blue": 0, "last": 0},  # square index 0
        {"red": 0, "green": 0, "blue": 1, "last": 1},  # square index 1
        {"red": 0, "green": 0, "blue": 1, "last": 1},  # square index 1
        {"red": 0, "green": 1, "blue": 0, "last": 2},  # square index 1
        # etc... (we use 2x2 N here)
    ]

    # N = 2 (2x2), MaxT = 8
    print("\nFirst moment (t=4) each square has at least ONE paint blob:")
    GetStatistics(4, 2, canvas)  # Called as soon as every square is painted once

    # System State: up to MaxT seconds have passed (MaxT blobs painted)
    canvas = [
        {"red": 1, "green": 2, "blue": 0, "last": 2},  # square index 0
        {"red": 0, "green": 0, "blue": 1, "last": 1},  # square index 1
        {"red": 0, "green": 0, "blue": 2, "last": 1},  # square index 1
        {"red": 0, "green": 1, "blue": 1, "last": 1},  # square index 1
        # etc... (we use 2x2 N here)
    ]

    print(f"\nAfter MaxT (Maxt={MaxT}) seconds have passed:")
    # N = 2 (2x2), MaxT = 8
    GetStatistics(MaxT, 2, canvas)
    # /-- TESTING END --/


# main guard
if __name__ == "__main__":
    main()




