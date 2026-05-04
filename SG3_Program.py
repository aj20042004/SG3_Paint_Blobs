# SG3 Paint Blobs Group Project
# Language - Python
# IDE - Developed in VScode, PyCharm & Thonny
#
# Python Packages Required:
# (In Thonny IDE add the following packages under "Tools > Manage Packages")
#   - tkinter
#   - matplotlib
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

import tkinter as tk
import random
import time
import matplotlib.pyplot as plt

"""
Maps a color name to a tkinter hex color string.
Parameters:
    color — "red", "green", "blue", or None
Returns:
    Hex color string (white if None)
"""


def GetColorHex(color):
    mapping = {
        "red": "#FF4444",
        "green": "#44BB44",
        "blue": "#4488FF",
        None: "#FFFFFF"  # unpainted square = white
    }
    return mapping.get(color, "#FFFFFF")


"""
Creates a tkinter window with an NxN white grid.
Parameters:
    N — grid size
    title — window title
Returns:
(root, tk_canvas, cell_px, cells_dict)
"""


def CreateAnimationWindow(N, title="Paint Blob Simulation"):
    # Scale cell size so the grid fits comfortably on screen (max 600px wide)
    cell_px = max(6, min(60, 600 // N))
    grid_px = N * cell_px

    root = tk.Tk()
    root.title(title)
    root.resizable(False, False)

    # Label above the grid
    lbl = tk.Label(root, text=title, font=("Arial", 11, "bold"), pady=4)
    lbl.pack()

    tk_canvas = tk.Canvas(root, width=grid_px, height=grid_px, bg="white",
                          highlightthickness=1, highlightbackground="#888888")
    tk_canvas.pack(padx=8, pady=8)

    cells_dict = {}
    for row in range(N):
        for col in range(N):
            x1 = col * cell_px
            y1 = row * cell_px
            x2 = x1 + cell_px
            y2 = y1 + cell_px
            rect_id = tk_canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="white", outline="#CCCCCC", width=1
            )
            cells_dict[row * N + col] = rect_id

    root.update()
    return root, tk_canvas, cell_px, cells_dict


"""
Runs a paint-blob simulation on an NxN grid for MaxT drops.
• Each step: drop a random color on a random square
• Prints stats when all squares are first painted (if before MaxT)
• Always prints stats at MaxT
• animate=True → shows tkinter animation
• animate=False → prints progress indicator
Returns:
(min, avg, max, canvas, full_canvas_done, root, tk_canvas, cells)
"""


def RunSimulation(N, MaxT, animate=False):
    colors = ["red", "green", "blue"]
    canvas = []
    for _ in range(N * N):
        canvas.append({"red": 0, "green": 0, "blue": 0, "top_color": None})

    total_blobs = 0
    unpainted_count = N * N
    full_canvas_done = False

    # ── animation setup ──────────────────────────────────────
    root = tk_canvas_widget = cells_dict = None
    if animate:
        root, tk_canvas_widget, _, cells_dict = CreateAnimationWindow(
            N, f"Paint Blob Simulation — {N}×{N} grid, MaxT={MaxT}"
        )
        # Target: finish well under 2 minutes. Cap delay at 0.3 s/blob.
        delay_s = min(0.30, 20.0 / MaxT)
    else:
        delay_s = 0

    # ── main drop loop ───────────────────────────────────────
    for t in range(1, MaxT + 1):
        sq_idx = random.randint(0, N * N - 1)
        color = random.choice(colors)

        sq = canvas[sq_idx]

        # Track coverage: decrement unpainted only on first visit
        if sq["red"] == 0 and sq["green"] == 0 and sq["blue"] == 0:
            unpainted_count -= 1

        # Drop the blob
        sq[color] += 1
        sq["top_color"] = color
        total_blobs += 1

        # Update animation frame
        if animate:
            tk_canvas_widget.itemconfig(cells_dict[sq_idx], fill=GetColorHex(color))

            tk_canvas_widget.update()
            if delay_s > 0:
                time.sleep(delay_s)

        # ── FIRST STOP: all squares covered ─────────────────
        if unpainted_count == 0 and not full_canvas_done:
            full_canvas_done = True
            print(f"\n{'─' * 100}")
            print(f"  STOP 1 — All {N * N} squares painted after {total_blobs} blobs!")
            print(f"{'─' * 100}")
            GetStatistics(canvas, total_blobs, N)
            print(f"{'─' * 100}")
            if animate:
                print("  (Simulation continues — watch the canvas...)\n")
                # Brief pause so user can read the printed stats
                time.sleep(2.5)

    # ── SECOND (or only) STOP: MaxT reached ─────────────────
    print(f"\n{'═' * 100}")
    if full_canvas_done:
        print(f"  STOP 2 — MaxT={MaxT} blobs dropped on {N}×{N} canvas.")
    else:
        print(f"  STOP 1 — MaxT={MaxT} blobs dropped on {N}×{N} canvas.")
        print(f"  Note: Not all squares were painted by MaxT. "
              f"  ({unpainted_count} square(s) still unpainted.)")
    print(f"{'═' * 100}")
    min_b, avg_b, max_b = GetStatistics(canvas, total_blobs, N)
    print(f"{'═' * 100}")

    # Ensure final grid is fully rendered
    if animate:
        for idx, square in enumerate(canvas):
            tk_canvas_widget.itemconfig(cells_dict[idx], fill=GetColorHex(square["top_color"]))

        tk_canvas_widget.update()

    return min_b, avg_b, max_b, canvas, full_canvas_done, root, tk_canvas_widget, cells_dict


"""
Runs experiments again but increases N based on increment submitted by user 
each time, stores current_N, min, avg, & max into lists, then calls PlotGraph 
function using those lists.

Returns: nothing
"""


def RunExperimentChangeN():
    # Prompts user for N, increment of N, & MaxT
    # N = GetValidInteger("Enter grid size N: ")
    N = int(input("Enter starting grid size N: "))  # temporary line until GetValidInteger is implemented
    N_increment = GetValidIncrement("Enter valid increment (1, 10, 100, or 1000): ")
    # max_t = GetValidInteger("Enter starting MaxT: ")
    max_t = int(input("Enter MaxT: "))  # temporary line until GetValidInteger is implemented

    # Lists to store values from simulations
    N_values = []  # grid sizes (N)
    min_list = []  # minimums
    avg_list = []  # averages
    max_list = []  # maximums

    # Runs simulations 10 times while incrementing N each time
    for i in range(9):
        current_N = N + i * N_increment
        min_b, avg_b, max_b, _, _, _, _, _ = RunSimulation(current_N, max_t, animate=False)

        # Appends values from simulation into lists
        N_values.append(current_N)
        min_list.append(min_b)
        avg_list.append(avg_b)
        max_list.append(max_b)

    # Plots the results
    PlotGraph(N_values, min_list, avg_list, max_list)


"""
Runs experiments again but increases MaxT based on increment submitted by user 
each time, stores current_t, min, avg, & max into lists, then calls PlotGraph 
function using those lists.

Returns: nothing
"""


def RunExperimentChangeMaxT():
    # Prompts user for MaxT, increment of MaxT, & N
    # max_t = GetValidInteger("Enter starting MaxT: ")
    max_t = int(input("Enter starting MaxT: "))  # temporary line until GetValidInteger is implemented
    t_increment = GetValidIncrement("Enter valid increment (1, 10, 100, or 1000): ")
    # N = GetValidInteger("Enter grid size N: ")
    N = int(input("Enter grid size N: "))  # temporary line until GetValidInteger is implemented

    # Lists to store values from simulations
    maxt_values = []  # MaxT values
    min_list = []  # minimums
    avg_list = []  # averages
    max_list = []  # maximums

    # Runs simulations 10 times while incrementing MaxT each time
    for i in range(9):
        current_t = max_t + i * t_increment
        min_b, avg_b, max_b, _, _, _, _, _ = RunSimulation(N, current_t, animate=False)

        # Appends values from simulation into lists
        maxt_values.append(current_t)
        min_list.append(min_b)
        avg_list.append(avg_b)
        max_list.append(max_b)

    # Plots the results
    PlotGraph(maxt_values, min_list, avg_list, max_list)


"""
Prompts and validates an increment for MaxT or N from user.

Parameter(s): 
    user_increment
Returns: 
    user_increment
"""
def GetValidIncrement(prompt):
    while True:  # re-prompts until valid input is submitted
        user_input = input(prompt)
        user_increment = int(user_input) # converts string to integer

        if user_increment == 1 or user_increment == 10 or user_increment == 100 or user_increment == 1000:
            break
        else:
            print("Invalid input. Your only options are 1, 10, 100, or 1000.")

    return user_increment


"""
Computes and prints canvas statistics, then returns min/avg/max.
Includes:
• Total blobs
• Min, max, average per square
• Color counts (red, green, blue)
• Single-color square count
Parameters:
    canvas, total_blobs, N
Returns:
    (min_blobs, avg_blobs, max_blobs)
"""


def GetStatistics(canvas, total_blobs, N):
    # determine total blob count by square
    totals_by_square = [
        sq["red"] + sq["green"] + sq["blue"]
        for sq in canvas
    ]

    min_square_blobs = min(totals_by_square)  # compute min/max/avg
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

    #  print all values, well-labelled
    print(f"  Canvas state at time t={total_blobs}:")
    print(f"  Total blobs dropped              = {total_blobs}")
    print(f"  Fewest  blobs on any one square  = {min_square_blobs}")
    print(f"  Most    blobs on any one square  = {max_square_blobs}")
    print(f"  Average blobs per square         = {avg_square_blobs:.4f}")
    print(f"  Red   blobs                      = {totals_by_color['red']}")
    print(f"  Green blobs                      = {totals_by_color['green']}")
    print(f"  Blue  blobs                      = {totals_by_color['blue']}")
    print(f"  Squares with only one color      = {total_one_color}")

    return min_square_blobs, avg_square_blobs, max_square_blobs


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
    # ── Program explanation ──────────────────────
    print("--------------------------------------------------------------")
    print("          SG3: PAINT BLOBS  —  CS 4500  Spring 2026           ")
    print("--------------------------------------------------------------")
    print("""
Welcome to the Paint Blobs Simulation!

What this program does:
  - Simulates random drops of red, green, or blue paint on a square
    grid canvas. One blob lands on a random square each "second."
  - Statistics are shown:
    1) when all squares are first painted, and
    2) after MaxT total blobs are dropped.
  - After two animated simulations you can run a batch of 10 experiments,
    varying either the grid size or the number of blobs, and view a graph
    comparing the results.

Experiments:
1. Default simulation: 10x10 grid, MaxT = 300

2. User simulation: user enters N and MaxT, then sees final canvas

3. Ten simulations with one changing variable:
   a) Change N (grid grows, MaxT fixed) - graph results
   b) Change MaxT (longer runs, N fixed) - graph results
""")
    
    # ── Simulation 1: fixed 10×10, MaxT=300 ─────────────────
    print("Starting Simulation 1  (10x10, MaxT=300)...\n")
    min_b, avg_b, max_b, canvas1, full1, root1, tkc1, cells1 = \
        RunSimulation(10, 300, animate=True)

    if root1:
        input("\nSimulation 1 complete. "
              "Press ENTER to close the canvas window and continue... ")
        try:
            root1.destroy()
        except tk.TclError:
            pass  # window was already closed manually


    # Simulation 3: change user N or MaxT for 10 simulations
    print("\nStarting Simulation 3 (change one variable...\n")

    print("\ta) Change N (grid grows, MaxT fixed)")
    print("\tb) Change MaxT (longer runs, N fixed)")
    choice = input("\nChoose an option: ")

    while True:
        if choice == "a" or choice == 'A':
            RunExperimentChangeN()
            break
        elif choice == "b" or choice == 'B':
            RunExperimentChangeMaxT()
            break
        else:
            choice = input("Choose (a) Change N or (b) Change MaxT: ")

# main guard
if __name__ == "__main__":
    main()
