import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # Is true if both number of cells and count are True
        if (self.count == len(self.cells)):
            return self.cells
        else:
            return set()    

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # It's True when count in set is 0
        if (self.count == 0):
            return self.cells
        else:
            return set()    


    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # If cell is in list; Remove the cell
        if ((cell in self.cells) and (self.count > 0)):
            self.cells.remove(cell)
            # Update count
            self.count = self.count - 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # If cell in cells remove the cell
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)



    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Add cell to moves
        self.moves_made.add(cell)
        # Add cell to safes
        self.safes.add(cell)
        # Calculate neighbors cells
        neighbors = self.get_neighbors(cell)
        # Check 
        neighbors, count = self.check_neighbors(neighbors, count)
        # Creates and add the new Sentence
        sentence = Sentence(neighbors, count)

        if sentence not in self.knowledge:
            self.knowledge.append(sentence)

        # Check mines and saves
        self.check_mine_and_safe()

                 
        
        self.check_mine_and_safe()
        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        possible_moves = self.safes - self.moves_made
        possible_moves = list(possible_moves)

        # Not safe moves
        if not(len(possible_moves)):
            return None

        # Choose a random move in safe moves
        index = random.randint(0, len(possible_moves) - 1)
        print(f'possible moves are {possible_moves}, index is {index}')
        move = possible_moves[index]
        return move

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = self.check_possible_moves()
        possible_moves = list(possible_moves)

        # If possible moves is empty, random move can not be done
        if not(len(possible_moves)):
            return None

        # Return available
        index = random.randint(0, len(possible_moves) - 1)
        move = possible_moves[index]
        return move



    def get_neighbors(self, cell):
        """
        Verify all the possible neighbor cells
        Return a set of those cells
        """
        i, j = cell
        neighbors = []
        
        # Cell not in a corner in i axis
        if (i > 0 and i < self.height - 1):
            neighbors.append((i-1, j))
            neighbors.append((i+1, j))
            # Cell not in a corner in j axis
            if (j > 0 and j < self.width - 1):
                neighbors.append((i+1, j-1)) 
                neighbors.append((i-1, j-1))
                neighbors.append((i, j-1))
                neighbors.append((i+1, j+1)) 
                neighbors.append((i-1, j+1))
                neighbors.append((i, j+1))
            # Cell in left corner in j axis
            elif (j == 0):
                neighbors.append((i+1, j+1)) 
                neighbors.append((i-1, j+1))
                neighbors.append((i, j+1))
            # Cell in right corner in j axis 
            elif (j == self.width - 1):
                neighbors.append((i+1, j-1)) 
                neighbors.append((i-1, j-1))
                neighbors.append((i, j-1))
        # Cell in top corner in i axis
        elif (i == 0):
            neighbors.append((i+1, j))
            if (j > 0 and j < self.width - 1):
                neighbors.append((i+1, j-1)) 
                neighbors.append((i, j-1))
                neighbors.append((i+1, j+1)) 
                neighbors.append((i, j+1))
            elif (j == 0):
                neighbors.append((i+1, j+1)) 
                neighbors.append((i, j+1))
            elif (j == self.width - 1):
                neighbors.append((i+1, j-1)) 
                neighbors.append((i, j-1))
        #   Cell in top corner or bottom  
        elif (i == self.height - 1):
            neighbors.append((i-1, j))
            if (j > 0 and j < self.width - 1):
                neighbors.append((i-1, j-1)) 
                neighbors.append((i, j-1))
                neighbors.append((i-1, j+1)) 
                neighbors.append((i, j+1))
            elif (j == 0):
                neighbors.append((i-1, j+1)) 
                neighbors.append((i, j+1))
            elif (j == self.width - 1):
                neighbors.append((i-1, j-1)) 
                neighbors.append((i, j-1))
                 
        neighbors = set(neighbors)
        return neighbors

    def check_neighbors(self, neighbors, count):
        """
        Check if neighbors are not safes or mines
        If are mines rest 1 in count
        Returns new count and the checked list
        """
        neighbors = list(neighbors)
        neighbors_aux = []
        for neighbor in neighbors:
            if (neighbor in self.mines):
                count = count - 1
            if (neighbor not in self.safes) and (neighbor not in self.mines):
                neighbors_aux.append(neighbor)
        return neighbors_aux, count

    def check_possible_moves(self):
        """
        Check all possible moves to do
        """
        possible_moves = set()
        for i in range(self.height):
            for j in range(self.width):
                cell_aux = (i, j)
                if ((cell_aux not in self.mines) and (cell_aux not in self.moves_made)):
                    possible_moves.add(cell_aux)
        return possible_moves
        
    def check_mine_and_safe(self):
        safes_aux = []
        mines_aux = []

        for sentence in self.knowledge:
            for safe in sentence.known_safes():
                if safe not in self.safes:
                    safes_aux.append(safe)
            for mine in sentence.known_mines():
                if mine not in self.mines:
                    mines_aux.append(mine)  
         
        # Get unique values
        safes_aux = set(safes_aux)
        mines_aux = set(mines_aux)
        safes_aux = list(safes_aux)
        mines_aux = list(mines_aux)
        
        # Mark
        for save_aux in safes_aux:
            self.mark_safe(save_aux)
        for mine_aux in mines_aux:
            self.mark_mine(mine_aux)  

    def check_sentences(self):
        """
        Compare sentence w sentence except if
        1. Are the same
        2. Are empty
        3. Doesn't have subset relation
        Then compare subsets to find new sentences and append those to knowledge
        """
        new_sentences = []

        for sentence in self.knowledge:
            for sentence_aux in self.knowledge:
                if (not(sentence == sentence_aux) and ((len(sentence.cells) > 0) and (len(sentence_aux.cells) > 0)) and (sentence.cells.issubset(sentence_aux.cells))):
                    modifiedSet = sentence_aux.cells - sentence.cells 
                    modifiedCount = sentence_aux.count - sentence.count
                    if (len(modifiedSet) > 0 and modifiedCount > -1):
                        new_sentences.append(Sentence(modifiedSet, modifiedCount))

        for sentence in new_sentences:
            if sentence not in self.knowledge:
                self.knowledge.append(sentence) 