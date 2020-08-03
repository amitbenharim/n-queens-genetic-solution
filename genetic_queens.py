import random
from copy import deepcopy
import math
#mutate, breed, do nothing.

dilation_factor = 8
def probability(dil_fact, scores):
    probabilities = []
    e_scores = []
    for score in scores:
        # we want to dilate the function in terms of how far apart the scores should be.
        e_scores.append(math.e**(score*dil_fact))

    total = sum(e_scores)

    for e_score in e_scores:
        probabilities.append(e_score/total)

    return probabilities


def print_board(board):
    printout = ""
    for i in range(len(board)**2):
        if i in board:
            printout += "Q "
        else:
            printout += "X "
        if (i + 1) % len(board) == 0:
            printout += "\n"
    print(printout)


def gen0(n, n_boards):
    positions = []
    for k in range(n):
        for j in range(n):
            positions.append(k*n + j)
    boards = []
    for i in range(n_boards):
        in_loop_pos = deepcopy(positions)
        #create a board
        board = []
        for j in range(n):
            element = random.choice(in_loop_pos)
            in_loop_pos.remove(element)
            board.append(element)
        boards.append(board)

    return boards

def is_diagonal(i,j,n):
    #this is like enclosing.
    #translate into coordinate
    i_coor = i//n, i%n
    j_coor = j//n, j%n
    if i_coor[0] + i_coor[1] == j_coor[0] + j_coor[1] or i_coor[0] - i_coor[1] == j_coor[0] - j_coor[1]:
        return True
    return False





def is_solution(board):
    n = len(board)

    for i in board:
        for j in board:
            if i != j:
                if i//n == j//n:
                    return False
                elif i%n == j%n:
                    return False
                elif is_diagonal(i,j,n):
                    return False

    return True

def find_correct_boards(boards):
    correct_boards = []
    for i in range(len(boards)):
        if is_solution(boards[i]):
            correct_boards.append(boards[i])

    return correct_boards

def give_score_board(board):
    n = len(board)
    score = 0
    # check horizontally
    for i in board:
        for j in board:
            if i != j:
                if i // n == j // n:
                    score += 1
                if i % n == j % n:
                    score += 1
                if is_diagonal(i,j,n):
                    score += 1
    return score

def give_scores(boards):
    score_and_board = []
    for board in boards:
        score_and_board.append((board, give_score_board(board)))
    return score_and_board


def give_score_queens(board):
    n = len(board)
    queens_pos_score = []
    for i in board:
        queens_pos_score.append(give_score_queen(board, i, n))

    return queens_pos_score


def give_score_queen(board, i, n):
    score = 0
    for j in board:
        if i != j:
            if i // n == j // n:
                score += 1
            if i % n == j % n:
                score += 1
            if is_diagonal(i,j,n):
                score += 1
    return score

#00 00 02 00
#00 00 00 00
#00 00 00 11
#12 00 14 00


def queen_probabilities(queens_pos_score):
    sum_scores = 0
    queens_pos_prob = []
    for i in queens_pos_score:
        sum_scores += i[1]
    for j in queens_pos_score:
        queens_pos_prob.append((j[0], j[1]/sum_scores))
    return queens_pos_prob


# How do we think about improving the algorithm genetically.
# for each of the 100 boards;
# chose the elite.
# generate 100 boards by either mutating an elite or merging two elite members

# how do we decide the elite? Take the top 10%
# how do we choose whether to mutate or to merge elite members.
# how do we merge.
# how do we mutate.
    # give each queen a score.
    # then assign a probability of mutation to each. pick randomly amongst the queens influenced by prob.
    # pick a random location to mutate to.


# def mutate(board):
#     score = give_score_board(board)
#     queen_probs = probability(1, give_score_queens(board)[1])
#
#     # find possible mutations:
#     empty_squares = []
#     for i in range(len(board)**2):
#         if i not in board:
#             empty_squares.append(i)
#     mutation_square = random.choice(empty_squares)
#
#     # pick queen to move
#     arr_of_queens_to_pick = []
#     for j in queens:
#         number_of_jth_queens = int(100*j[1])
#         for k in range(number_of_jth_queens):
#             arr_of_queens_to_pick.append(j[0])
#
#     queen_sac = random.choice(arr_of_queens_to_pick)
#     ind = board.index(queen_sac)
#     board[ind] = mutation_square

def mutate(board):
     n = len(board)
     scores = give_score_queens(board)
     probabilities = probability(dilation_factor, scores)

     queens_chosen = False
     while not queens_chosen:
         for i in range(len(probabilities)):
             if random.random() < probabilities[i]:
                 queens_chosen = True
                 #mutate board[i]
                 scores = []
                 queens = []
                 new_board = board
                 del new_board[i]
                 while len(queens) == 0:
                     for iteration in range(100):
                         index = random.randint(0, n*n-1)
                         if (index not in queens) and (index not in board):
                             queens.append(index)
                             scores.append(-give_score_queen(new_board, index, n))
                 break
     queen_chosen = False
     individual_probabilities = probability(dilation_factor, scores)
     while not queen_chosen:
         for i in range(len(individual_probabilities)):
             if random.random() < individual_probabilities[i]:
                 if queens[i] not in board:
                     new_board.append(queens[i])
                     queen_chosen = True
                     break
     return new_board

##def mutate(board):
##    #print(f"board before mutation {board}")
##    #print(give_score_board(board))
##    #print_board(board)
##    scores = give_score_queens(board)
##    probabilities = probability(dilation_factor,scores)
##
##    #pick one queen.
##    total = 0
##    rand = random.random()
##    index = 0
##    for i in range(len(probabilities)):
##        total += probabilities[i]
##        if total > rand:
##            index = i
##            break
##
##    empty_spots = []
##    empty_spots_scores = []
##    new_board = deepcopy(board)
##    del new_board[index]
##    #remember to change this to 100 boards.
##    for j in range(len(board)**2):
##        if j not in board:
##            empty_spots.append(j)
##            empty_spots_scores.append(-give_score_queen(new_board, j, len(board)))
##
##    #give probabilities
##    empty_spots_probabilities = probability(dilation_factor, empty_spots_scores)
##
##    #pick a spot.
##    empty_total = 0
##    empty_rand = random.random()
##    for i in range(len(empty_spots_probabilities)):
##        empty_total += empty_spots_probabilities[i]
##        if empty_total > empty_rand:
##            new_board.append(empty_spots[i])
##            break
##    #print(f"board after mutation {new_board}")
##    #print(give_score_board(new_board))
##    #print_board(new_board)
##    return new_board

def merge(board1, board2):
    resulting_board = []




def next_gen(boards):
    solutions = []
    new_boards = []
    for board in boards:
        new_boards.append(mutate(board))
    return new_boards



def run_genetic(n, n_boards):
    boards = gen0(n, n_boards)
    gen = 0
    while True:
        print(gen)
        for board in boards:
            if is_solution(board):
                return board
        boards = next_gen(boards)
        gen += 1

print_board(run_genetic(8,1))
#board1 = gen0(4, 1)[0]
#print_board(board1)
#print(give_score_queens(board1))



def inversions(board):
    n = len(board)
    counter = 0
    for row in range(n):
        for column in range(n):
            new_board = board[:]
            for item in range(n):
                new_board[item] = ((new_board[item]//n+row)%n)*n + (new_board[item]%n+column)%n
            if is_solution(new_board):
                counter += 1
    return counter

def solution(n):
    board = [(n%2)*n]
    for i in range(n-1):
        if board[i]+2*n >= n*n:
##            if (n+1//2)%2 == 0 and n > 7:
##                if i != n-2:
##                    board.append(board[i]%n+1 + 3*n - board[0])
##                else:
##                    board.append(board[i]%n+1 + n - board[0])
##            else:
                board.append(board[i]%n+1 + n - board[0])
        else:
            board.append(board[i]+2*n+1)
    return board













