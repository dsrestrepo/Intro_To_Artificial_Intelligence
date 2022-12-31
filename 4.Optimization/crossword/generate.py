import sys
import copy
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        words_to_remove_dict = dict()
        # Take the domains:
        for domain in self.domains:
            # Take actual domain
            actual_domain = self.domains[domain]
            # Take length of the actual domain
            domain_length = domain.length
            # Take the words
            words_to_remove = []
            for word in actual_domain:
                word_length = len(word)
                # Compare the length of word V. length of domain
                if (word_length != domain_length):
                    # Store the words in the list to avoid python error
                    words_to_remove.append(word)
                # Store the list in a dictionary
                words_to_remove_dict[domain] = words_to_remove

        # Remove words using the dictionary
        for domain in words_to_remove_dict:
            # For each domain
            actual_domain = words_to_remove_dict[domain]
            # Remove the word
            for word in actual_domain: 
                self.domains[domain].remove(word) 
        #print(self.domains)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Check if not overlap
        revised = False
        if not (self.crossword.overlaps[x, y]):
            return revised

        # Get overlaps
        i, j = self.crossword.overlaps[x, y]

        #print(self.crossword.overlaps[x, y])

        found = False
        domains_aux = copy.deepcopy(self.domains[x])
        # For each variable in x
        for X in domains_aux: 
            # For each variable in y
            for Y in self.domains[y]:
                # If we found the value no need to keep going
                if X[i] == Y[j]:
                    found = True
                    break
            # Check if we found the value
            if found:
                continue
            # If we didn't found the value remove the actual
            else:
                self.domains[x].remove(X)
                revised = True
            
        return revised       


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Create qeue
        queue = []

        # If not arcs; create our own arcs
        if arcs == None:
            # For each x
            for X in self.domains:
                # Find a Y that overlaps with X
                for Y in self.crossword.neighbors(X): 
                    if (X != Y):           
                        queue.append((X, Y))
        else:
            # If arcs then the queue will be the arcs
            queue = arcs

        # If still values in queue do:
        while queue:
            # Remove item from queue
            X, Y = queue.pop()
            # Revise using the function
            revise = self.revise(X, Y)
            # If is True
            if revise:
                # See if updated domains after revised function are empty
                if not self.domains[X]:
                    return False
                # Check for neighbours of x
                for neighbour in self.crossword.neighbors(X):
                    # Append to the queue new neighbours
                    if not(neighbour == Y):
                        queue.append((neighbour, X))

            return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for domain in self.domains:
            if domain not in assignment:
                return False 
        return True        


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        words = []
        # For each variable
        for variable in assignment:
            # Get the word
            word = assignment[variable]
            variable_length = variable.length
            word_length = len(word)
            # Verify if the word is in words
            if word in words:
                # If word in words return false
                return False
            else:
                # Then add the word
                words.append(word)
            # check if both, Variable and word have same length
            if not(variable_length == word_length):
                return False
            # Check the possible neighbors:
            for neighbor in self.crossword.neighbors(variable):
                # Get the overlap of the variable and neighbor
                i, j = self.crossword.overlaps[variable, neighbor]
                if neighbor in assignment:
                    neighbor_word = assignment[neighbor]
                    # If neighbor is in assignment but the words doesn't overlap
                    if (neighbor in assignment) and not(neighbor_word[j] == word[i]):
                        # Return false
                        return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        total_count = {}
        # For each word
        for word in self.domains[var]:
            # Just count if word not in assignment
            # Check if word not assigned
            if not(word in assignment):
                total_count[word] = 0
            # If word assigned continue
            else:
                continue
            # See the neighbors of var
            for neighbor in self.crossword.neighbors(var):
                # See the words in the neighbors of var
                for other_word in self.domains[neighbor]:
                    # Check if words overlap
                    i, j = self.crossword.overlaps[var, neighbor]
                    # Check if words don't overlap then add 1
                    if word[i] != other_word[j]:
                        total_count[word] = total_count[word] + 1

        #print(total_count)
        sorted_total_count = sorted(total_count, key=lambda x: total_count[x])
        #print(sorted_total_count)
        return sorted_total_count



    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        words_to_choose = []
        # For each possible domain in the domains
        for domain in self.domains:
            # Discard the domain already assigned
            if domain in assignment:
                continue
            # Add the domain not assigned
            else:
                words_to_choose.append(domain)

        for i, domain in enumerate(words_to_choose):
            # In the first iteration choose the actual domain (default)
            if i == 0:
                heuristic = len(self.domains[domain])
                variable_to_choose = domain
            else:
                # If the actual domain was less words assign that one
                if heuristic > len(self.domains[domain]):
                    heuristic = len(self.domains[domain])
                    variable_to_choose = domain
                # If we have a tie
                elif heuristic == len(self.domains[domain]):
                    # Compare neighbors:
                    # If The actual variable has more neighbors that the actual to choose 
                    if len(self.crossword.neighbors(domain)) > len(self.crossword.neighbors(variable_to_choose)):
                        heuristic = len(self.domains[domain])
                        variable_to_choose = domain
                    else:
                        heuristic = len(self.domains[domain])
                        variable_to_choose = domain

        return variable_to_choose


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if assignment is complete
        if self.assignment_complete(assignment):
            return assignment
        
        # Select a domain with unassigned variable
        domain = self.select_unassigned_variable(assignment)

        # Take a list of words
        words = self.order_domain_values(domain, assignment)
        # go trough the domins in the order of less assigned
        for word in words:
            # Assign that word to the domain
            assignment[domain] = word
            # If is conistent
            if self.consistent(assignment):
                # Do the backtrack
                result = self.backtrack(assignment)
                if result:
                    return result
            assignment.pop(domain)
        
        return None        



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
