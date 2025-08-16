import random
import copy

def display_matrix(game_matrix):
    """
    Displays the current state of the game matrix (bottles and colors) in a formatted way.
    """
    print()
    num_bottles = len(game_matrix)

    for row in range(4):
        for col in range(num_bottles):
            color = game_matrix[col][row]

            if color != 0:
                color_code = color_set.get(color, "")
                colored_text = f"{color_code}{color:^8s}{RESET}"
            else:
                colored_text = "******".center(8)

            end_char = "\t" if col < num_bottles - 1 else "\n"
            print(f"| {colored_text} |", end=end_char)

    for _ in range(num_bottles):
        print("\\  ______  /", end="\t")
    print()


def find_top_color(bottle):
    """
    Returns the top-most color in a bottle (i.e., first non-zero value).
    """
    for i in range(4):
        if bottle[i] != 0:
            return bottle[i]
    return 0


def get_all_valid_combinations(matrix):
    """
    Returns all valid moves (combinations of bottles) where a pour is possible.
    - Either pouring into an empty bottle
    - Or pouring onto a matching color with space
    """
    combinations_list = []

    for ii in range(len(matrix) - 1):
        first_color = find_top_color(matrix[ii])
        if first_color == 0:
            continue
        for jj in range(ii + 1, len(matrix)):
            second_color = find_top_color(matrix[jj])
            if second_color == 0:
                combinations_list.append([ii, jj])
            elif first_color == second_color and matrix[jj].count(0) != 0:
                combinations_list.append([ii, jj])

    for ii in range(len(matrix) - 1, 0, -1):
        first_color = find_top_color(matrix[ii])
        if first_color == 0:
            continue
        for jj in range(ii - 1, -1, -1):
            second_color = find_top_color(matrix[jj])
            if second_color == 0:
                combinations_list.append([ii, jj])
            elif first_color == second_color and matrix[jj].count(0) != 0:
                combinations_list.append([ii, jj])
    return combinations_list


def is_game_over(matrix):
    """
    Checks if the game is complete — all full bottles contain 4 same-color elements.
    """
    complete_bottles = 0

    for bottle in matrix:
        if 0 in bottle:
            continue
        same_color_count = 0
        for ii in range(1, 4):
            if bottle[ii] == bottle[ii - 1]:
                same_color_count += 1
        if same_color_count == 3:
            complete_bottles += 1
    if complete_bottles == full_bottles:
        return True
    return False


def apply_move(matrix, from_bottle, to_bottle, from_color, to_color):
    """
    Executes a move by pouring from one bottle to another, following game rules.
    Handles both pouring into empty or same-color partial bottles.
    """
    if to_color == 0:
        count = 0
        for ii in range(4):
            if matrix[from_bottle][ii] != 0:
                index = ii
                break
        first_empty = 3
        for ii in range(index, 4):
            if matrix[from_bottle][ii] == from_color:
                matrix[to_bottle][first_empty] = from_color
                first_empty -= 1
                count += 1
            else:
                break
        while count > 0:
            matrix[from_bottle][index] = 0
            index += 1
            count -= 1
        return matrix

    elif from_color == to_color:
        count = 0
        empty_slots = matrix[to_bottle].count(0)
        first_empty = empty_slots - 1
        for ii in range(4):
            if matrix[from_bottle][ii] != 0:
                index = ii
                break
        start_index = index
        while matrix[to_bottle].count(0) > 0 and matrix[from_bottle][index] == from_color:
            matrix[to_bottle][first_empty] = from_color
            index += 1
            count += 1
            first_empty -= 1
            if index == 4:
                break
        while count > 0:
            matrix[from_bottle][start_index] = 0
            start_index += 1
            count -= 1
        return matrix


class TreeNode:
    """
    Represents a node in the game state tree.
    Each node contains a matrix (state), level (move depth), and links to child/sibling/parent.
    """
    def __init__(self, matrix, level):
        self.matrix = matrix
        self.sibling = None
        self.child = None
        self.level = level
        self.solution_flag = None
        self.parent = None

    def get_matrix(self, parent_matrix):
        return self.matrix

    def get_level(self, node):
        return self.level

    def add_child(self, child_node):
        self.child = child_node

    def add_sibling(self, sibling_node):
        self.sibling = sibling_node

    def set_level(self, level):
        self.level = level

    def show_matrix(self):
        return self.matrix

    def get_child(self):
        return self.child

    def set_parent(self, parent_node):
        self.parent = parent_node

    def mark_solution_path(self):
        current = self
        current.solution_flag = 1
        while current.parent:
            current.parent.solution_flag = 1
            current = current.parent

    def get_solution_flag(self):
        return self.solution_flag

    def find_hint(self):
        current = self.child
        found = False
        if current is None:
            return None
        while current:
            if current.solution_flag == 1:
                found = True
                break
            current = current.sibling
        if found:
            return current
        else:
            return None

    def is_solution(self):
        return self.solution_flag

    def get_solution_path(self):
        current = self
        path_list = [current]
        while current.get_child():
            current = current.get_child()
            while current:
                if current.solution_flag == 1:
                    path_list.append(current)
                    break
                current = current.sibling
        return path_list

    def navigate_tree(self, matrix_view):
        current = self
        found = False
        if current.matrix == matrix_view:
            return current
        if current.sibling is None:
            print("Move is not valid")
            return 0
        while current:
            if current.matrix == matrix_view:
                found = True
                break
            current = current.sibling
        if not found:
            print("Move is not valid")
            return 0
        else:
            return current

    def get_child_node(self):
        return self.child

    def get_sibling_node(self):
        return self.sibling

    def get_siblings_list(self):
        current = self
        siblings_list = []
        while current:
            siblings_list.append(current)
            current = current.sibling
        return siblings_list


RED = "\033[38;5;196m"
GREEN = "\033[38;5;46m"
ORANGE = "\033[38;5;208m"
RESET = "\033[0m"
print()
print(f"{ORANGE}" + "=" * 60)
print("      Welcome to Water Sort Puzzle Game Simulation!")
print("=" * 60 + f"{RESET}")

color_set = {
    "red": "\033[38;5;196m",
    "yellow": "\033[38;5;226m",
    "blue": "\033[38;5;21m",
    "green": "\033[38;5;46m",
    "white": "\033[38;5;231m",
    "rose": "\033[38;5;205m",
    "golden": "\033[38;5;220m",
    "purple": "\033[38;5;129m",
    "orange": "\033[38;5;208m",
    "aqua": "\033[38;5;51m"
}

game_matrix = []
max_full_bottles = len(color_set)

while True:
    try:
        full_bottles = int(input(f"Number of full bottles (max {max_full_bottles}): "))
        if 1 <= full_bottles <= max_full_bottles:
            break
        else:
            print(f"\n{RED}Please enter a number between 1 and {max_full_bottles}.{RESET}\n")
    except ValueError:
        print(f"\n{RED}Invalid input. Please enter a valid number.{RESET}\n")


empty_bottles = int(input("Number of empty bottles: "))
max_moves = int(input("Maximum number of moves: "))
print()
mask = 3
count_moves = 0
generated_colors = []
t = 0

# Generate pseudo-random color indices using a simplified Blum Blum Shub (BBS) method. M=253
while t < (4 * full_bottles):
    mask = 3
    seed = random.randint(100, 1000)
    first = pow(seed, 2) % 253
    second = pow(first, 2) % 253
    third = pow(second, 2) % 253
    first = first & mask
    second = second & mask
    third = third & mask
    sequence = (first << 4) | (second << 2) | third
    sequence = sequence % full_bottles
    if generated_colors.count(sequence) >= 4:
        continue
    else:
        generated_colors.append(sequence)
        t += 1

temp_list = []
color_names = list(color_set.keys())
for i in range(full_bottles):
    for j in range(4):
        temp_list.append(color_names[generated_colors[4 * i + j]])
    game_matrix.append(temp_list)
    temp_list = []

for _ in range(empty_bottles):
    game_matrix.append([0, 0, 0, 0])

display_matrix(game_matrix)

if is_game_over(game_matrix):
    print(f"\n{GREEN}🎉 GAME OVER! You got lucky 😉{RESET}")
    exit()

make_move = False
tree_generated = False
retry_move = False

while True:
    print(f"\n{GREEN}OPTIONS:{RESET}")
    print("0. Generate tree")
    print("1. Make a move")
    print("2. View tree")
    print("3. Hint")
    print("4. Show one solution")
    print("5. Show current game state")
    print("6. Exit program\n")

    while True:
        try:
            x = int(input("Choose an option: "))
            if 0 <= x <= 6:
                break
            else:
                print(f"\n{RED}Invalid option. Please enter a number between 0 and 6.{RESET}\n")
        except ValueError:
            print(f"\n{RED}Invalid input. Please enter a valid number.{RESET}\n")

    if x == 0:
        tree_generated = True
        first_move = True
        # DFS traversal
        stack = []
        root = TreeNode(game_matrix, 0)
        stack.append(root)

        while stack:
            temp = stack.pop()
            parent_node = temp
            level = temp.get_level(temp)
            matrix = copy.deepcopy(temp.get_matrix(temp))
            combinations = get_all_valid_combinations(matrix)
            next_level = level + 1
            if next_level > max_moves:
                continue

            for i in range(len(combinations)):
                matrix = copy.deepcopy(temp.get_matrix(temp))
                from_idx = combinations[i][0]
                to_idx = combinations[i][1]
                color1 = find_top_color(matrix[from_idx])
                color2 = find_top_color(matrix[to_idx])

                updated_matrix = apply_move(matrix, from_idx, to_idx, color1, color2)
                is_solution = is_game_over(updated_matrix)

                new_node = TreeNode(updated_matrix, next_level)
                new_node.set_level(next_level)

                if i == 0:
                    temp.add_child(new_node)
                    new_node.set_parent(parent_node)
                    previous_node = new_node
                else:
                    previous_node.add_sibling(new_node)
                    new_node.set_parent(parent_node)
                    previous_node = new_node

                if is_solution:
                    previous_node.mark_solution_path()
                else:
                    stack.append(new_node)

    if x == 1:
        if not tree_generated:
            print(f"\n{RED}You must generate the tree first (option 0) before making a move.{RESET}\n")
            continue

        make_move = True
        print(f"{ORANGE}Note: Bottle numbering starts from 0 up to {full_bottles + empty_bottles - 1}{RESET}")
        from_bottle = int(input("From bottle: "))
        to_bottle = int(input("To bottle: "))

        if first_move or retry_move:
            first_move = False
            root_matrix = root.show_matrix()

            color1 = find_top_color(root_matrix[from_bottle])
            color2 = find_top_color(root_matrix[to_bottle])

            if color1 == 0 or (color1 != color2 and color2 != 0) or root_matrix[to_bottle].count(0) == 0:
                retry_move = True
                print(f"\n{RED}Invalid move{RESET}\n")
                continue

            new_matrix = apply_move(root_matrix, from_bottle, to_bottle, color1, color2)
            position = root
            first_child = position.get_child_node()
            if first_child is None:
                retry_move = True
                print(f"\n{RED}Invalid move{RESET}\n")
                continue
            current_position = first_child.navigate_tree(new_matrix)
            if current_position == 0:
                retry_move = True
                continue
            else:
                retry_move = False
                matrix_in_play = current_position.show_matrix()
                display_matrix(matrix_in_play)
                if current_position.get_level(current_position) == max_moves:
                    print("\nGAME OVER!")
                    if is_game_over(matrix_in_play):
                        print(f"\n{GREEN}YOU WON{RESET} 😁")
                    else:
                        print(f"\n{RED}YOU LOST{RESET} 😭")
                    exit()
        else:
            parent_matrix = current_position.show_matrix()
            color1 = find_top_color(parent_matrix[from_bottle])
            color2 = find_top_color(parent_matrix[to_bottle])

            if color1 == 0 or (color1 != color2 and color2 != 0) or parent_matrix[to_bottle].count(0) == 0:
                print(f"\n{RED}Invalid move{RESET}\n")
                continue

            new_matrix = apply_move(parent_matrix, from_bottle, to_bottle, color1, color2)
            position = current_position
            first_child = position.get_child_node()
            if first_child is None:
                print(f"\n{RED}Invalid move{RESET}\n")
                continue
            current_position = first_child.navigate_tree(new_matrix)
            if current_position == 0:
                continue
            else:
                matrix_in_play = current_position.show_matrix()
                display_matrix(matrix_in_play)
                if current_position.get_level(current_position) == max_moves:
                    print("\nGAME OVER!")
                    if is_game_over(matrix_in_play):
                        print(f"\n{GREEN}YOU WON{RESET} 😁")
                    else:
                        print(f"\n{RED}YOU LOST{RESET} 😭")
                    exit()

    if x == 2:
        if not tree_generated:
            print(f"\n{RED}You must generate the tree first (option 0) before viewing it.{RESET}\n")
            continue
        queue = [root]
        while queue:
            node = queue.pop(0)
            display_matrix(node.show_matrix())
            print()
            child = node.get_child_node()
            if child:
                siblings = child.get_siblings_list()
                queue.extend(siblings)

    if x == 3:
        if not make_move:
            print(f"\n{RED}You must make a move first before using hint.{RESET}\n")
            continue
        hint_node = current_position.find_hint()
        if hint_node is None:
            print(f"{RED}No hint available{RESET}")
            continue
        else:
            current_position = hint_node
            display_matrix(current_position.show_matrix())
            if is_game_over(current_position.show_matrix()):
                print("\nGAME OVER!")
                print(f"\n{GREEN}YOU WON{RESET} 😁")
                exit()

    if x == 4:
        if not make_move:
            print(f"\n{RED}You must make a move first before showing a solution.{RESET}\n")
            continue
        if not current_position.is_solution():
            print(f"\n{RED}Solution does not exist{RESET}\n")
            continue
        solution_path = current_position.get_solution_path()
        for node in solution_path:
            display_matrix(node.show_matrix())
            print()

    if x == 5:
        if 'matrix_in_play' in globals():
            display_matrix(matrix_in_play)
        else:
            print(f"\n{RED}You must make a move first before showing current state.{RESET}\n")

    if x == 6:
        print(f"\n{RED}Program terminated.{RESET}")
        exit()
