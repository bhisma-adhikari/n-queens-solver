import numpy as np 
import random 

def initialize(n):
    """Return a nxn array such that each row and each column 
    has exactly one 1 (queen), and 0 elsewhere"""
    chessboard = np.zeros((n,n), dtype=np.int8)
    available_cols = list(range(n))
    for row in chessboard:
        # set one random available column to 1 
        col = random.choice(available_cols)
        available_cols.remove(col)
        row[col] = 1
    return chessboard
    
    
def possible_moves(position, n, vertical_only):
    """Return a list of all possible squares, 
    where the queen could move. 
    Assumption: all possible moves are unoccupied
    Parameters:
        position ((row,col)): current position
        n (int): chessboard size 
        vertical_only: (bool): if True, moves are
            constrained vertically only 
    """
    row, col = position
    moves = []
    for i in range(n):
        moves.append((i, col)) # all vertical moves 
        
    if not vertical_only:
        for i in range(n):
            moves.append((row, i)) # all horizontal moves 
        for i in range(-n+1,n):
            for j in range(-n+1,n):
                row_new = row + i
                col_new = col +j 
                if abs(i)==abs(j) and row_new in range(0,n) and col_new in range(0,n):
                    moves.append((row_new, col_new))
          
    moves = set(moves) # remove duplicates 
    moves.remove((row, col)) # remove current position 
    return list(moves)
        
    
def conflict_count(chessboard, destn):
    """Return conflict count that would occur for a queen if it moved to destn"""
    count = 0 
    moves = possible_moves(position=destn, n=chessboard.shape[0], vertical_only=False)
    for move in moves:
        i,j = move
        if chessboard[i][j] == 1:
            count += 1 
    return count 
    

def queens_with_conflicts(chessboard):
    """Return the list of all queens having at least 1 conflict. 
    Each queen is a tuple (row, col)"""
    queens = np.nonzero(chessboard)
    queens = [(i,j)for i,j in zip(queens[0], queens[1])]
    queens = [q for q in queens if conflict_count(chessboard, q)]
    return queens 
        
    
def display_chessboard(chessboard):
    print()
    for row in chessboard:
        for col in row:
            char = u'\u25a0' if col == 1 else u'\u25a1'  # black square or white square 
            print(char, end=' ')
        print()    
    print()
    
    
def solve(chessboard):
    """Return solved chessboard, steps if solution found. Else return None, None 
    Parameters: 
        chessboard (nxn numpy array)
    """
    i = 0
    while i < 1000: # 1000 is the maximum steps allowed 
        queens_with_conflicts_ = queens_with_conflicts(chessboard)
        if queens_with_conflicts_:
            i += 1
            if i in [1,10,20,30,50,70] or not i%50:
                print(f"Step: {i: > 5}")
            queen = random.choice(queens_with_conflicts_) # 1 random queen with conflict 
            possible_moves_ = possible_moves(position=queen, n=chessboard.shape[0], vertical_only=True)
            # -1 is done, because the queen would have moved, so cannot conflict with itself
            move_conflict = {m:conflict_count(chessboard,m) - 1 for m in possible_moves_}
            move = min(move_conflict, key=move_conflict.get)  # move with minimum conflict

            # move queen 
            chessboard[queen[0]][queen[1]] = 0 
            chessboard[move[0]][move[1]] = 1
        else: 
            print(f"Step: {i: > 5}")
            return chessboard, i
    return None, None  # solution not found in 1000 steps, so abort 
    

def next():
    print(f"\nContinue with another chessboard: [Y/N] ? ", end='')
    while True:
        cmd = input()
        if cmd in ['', 'y', 'Y']:
            return True
        elif cmd in ['n', 'N']:
            return False
        else:
            print("\nPlease press either Y or N :", end='')


def main():
    while True:
        size = input("\nEnter chessboard size: ")
        try:
            size = int(size)
        except ValueError:
            print("\nOops, that's an invalid number.\nPlease, enter a valid number:")
            continue 
        if size in [2,3]:
            print("Size 2 and 3 are not allowed.")
            continue 

        chessboard = initialize(size)
        print('\nINITIAL STATE:\n--------------')
        display_chessboard(chessboard)
        chessboard, steps = solve(chessboard)
        if chessboard is not None:
            print(f"\nSolution found in {steps} steps.")
            print('\nFINAL STATE:\n------------')
            display_chessboard(chessboard)
        else: 
            print("\nOops, for this particular initialization of the chessboard,")
            print("no solution was found in 1000 steps. So, the procedure was ABORTED.")
            print("Please, TRY AGAIN. You can use the same chessboard size.")
                  
        if next():
            continue 
        else:
            break 
    return 

if __name__=='__main__':
    main() 
