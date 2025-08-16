# 🧪 Water Sort Puzzle – Python Simulation

## 🔍 Overview

Water Sort Puzzle is a color-sorting logic game. The objective is simple:  
**Sort the liquids in the bottles so that each bottle contains only one color.**

You can play the **original Water Sort Puzzle game** and see how it works here:  [Fun Water Sorting on Poki](https://poki.com/en/g/fun-water-sorting)

## 🎮 Game Rules

- Each bottle can hold **up to 4 units** of colored liquid.
- You can **pour** the top portion of a liquid from one bottle into another **if**:
  - The destination bottle is **empty**, or  
  - The destination bottle's top liquid **matches in color**, and it has **enough space** to accommodate the poured units.
- You **cannot** pour onto a different color or into a full bottle.
- The game is **won** when all bottles are either empty or contain **only one color**.

## 📌 Game Options

**0. Generate tree**
   → Builds a game tree from the current state using depth-first search (DFS).
     This must be done before making moves, getting hints, or showing a solution.

**1. Make a move**
   → Prompts you to enter the source and target bottle indices.
     The move will be validated based on the game rules and tree structure.

**2. View tree**
   → Displays all possible game states generated in the tree, level by level.
     Useful for visualizing how the game evolves with each move.

**3. Hint**
   → Shows the next move that leads toward a solution (if available).
     Only works if a solution path exists.

**4. Show one solution**
   → Displays one valid solution path from the current state to a win condition.
     Only works if the current state lies on a known solution path.

**5. Show current game state**
   → Displays the current bottle configuration, color-coded for clarity.

**6. Exit program**
   → Ends the game and exits the program.

## 🧠 Game Logic

The simulation uses **depth-first search (DFS)** to generate all valid game states up to a defined move limit.

- A `TreeNode` class is used to **build and traverse** the game state tree.
- Each node represents a **new game state** resulting from a valid move.
- **Solution paths** (winning branches) are automatically **marked** in the tree.
- **Hints** and **complete solutions** are extracted by traversing the tree structure.
- You can **follow one solution path** from the current node or request the **next best move** via the hint system.




