import copy

# Name: BOLIN MA
# STUDENT ID: 30090474

direction_option = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]


def new_board():

    maxRows = 8
    row = maxRows * [0]
    board = []
    for i in range(maxRows):
        newTable = copy.deepcopy(row)
        board.append(newTable)

    board[3][3] = 2
    board[3][4] = 1
    board[4][3] = 1
    board[4][4] = 2

    return board


def score(board):

    s1 = 0
    s2 = 0

    for row in board:

        s1 += row.count(1)
        s2 += row.count(2)

    return s1, s2


def print_board(board):

    for i in range(len(board)):
        res = ''

        for j in range(len(board[i])):

            res += (str(board[i][j]) + ' ')
        print(i+1, res)

    print(' ', 'a b c d e f g h')


def enclosing(board, player, pos, direct):

    if player == 1:
        enemy = 2
    else:
        enemy = 1

    r = pos[0]
    c = pos[1]
    dr = direct[0]
    dc = direct[1]

    temp = []

    while ((r+dr) in range(8)) and ((c+dc) in range(8) and (board[r + dr][c + dc] != 0)):
        temp.append(board[r + dr][c + dc]) #load every connected stone in a temp list

        if temp[0] == player:
            return False

        if temp[0] == enemy and temp[-1] == player:
            return True

        r += dr
        c += dc

    return False


def valid_moves(board, player):

    """
    :param board:
    :param player:
    :return: a list of valid moves as tupple format
    """

    retVal = []

    for r in range(len(board)):

        for c in range(len(board[0])):

            if board[r][c] == 0: #check if the current pos doesnt have any stone
                i = 0

                while i in range(len(direction_option)):

                    if enclosing(board, player, (r,c), direction_option[i]) is True:

                        retVal.append((r,c))
                        break
                    i += 1

    return retVal


def valid_direction(board, player, pos):

    r = pos[0]
    c = pos[1]
    retVal = []
    for direction in direction_option:

        if enclosing(board, player, (r, c), direction) is True:
            retVal.append(direction)

    return retVal


def next_state(board, player, pos):

    """

    :param board:
    :param player:
    :param pos: the move of player place a stone
    :return: next_board, next_player
    """

    next_player = 0
    if player == 1:
        enemy = 2
    else:
        enemy = 1

    board[pos[0]][pos[1]] = player #place a stone
    # need to check valid direction
    directionLst = valid_direction(board,player,pos)

    for direction in directionLst:
        dr = direction[0]
        dc = direction[1]
        r = pos[0]
        c = pos[1]
        #from the starting point move the pointer towards direction, once the are not out of board and == enemy stone,change it
        while ((r + dr) in range(8)) and ((c + dc) in range(8) and (board[r + dr][c + dc] != player)):

            board[r+dr][c + dc] = player #change the enemy stone to player stone

            r += dr
            c += dc

    if valid_moves(board, enemy) != []:
        next_player = enemy

    elif valid_moves(board, player) != []:
        next_player = player

    return board, next_player


def position(string):

    strCol_lst = ['a','b','c', 'd', 'e', 'f', 'g', 'h']

    retVal = None

    if len(string) == 2:
        strRow = string[1]
        strCol = string[0]

        if strCol in strCol_lst and strRow.isdigit() and int(strRow) in range(1,9):
            r = int(strRow) - 1
            c = strCol_lst.index(strCol)

            retVal = (r, c)

    if retVal is None:
        print('Invalid move, tray again!')

    return retVal


def run_two_players():

    cur_board = new_board()
    print_board(cur_board)
    player = int(input('Whose turn it is: '))

    while valid_moves(cur_board,1) !=[] or valid_moves(cur_board,2)!= []:

        strPos = input('Enter where to place your stone: ')
        if strPos != 'q':

            pos = position(strPos)
            if pos in valid_moves(cur_board,player):
                (next_board, player) = next_state(cur_board,player,pos)

                cur_board = next_board
                print_board(cur_board)

        elif player == 1:
            player = 2

        else:
            player = 1

        print('Now is player ', player, 'turn')

    print(score(cur_board))


def best_move(board, player):

    max_score = 0
    max_pos = 0
    for pos in valid_moves(board, player):

        temp_board = copy.deepcopy(board)
        (temp_board, player) = next_state(temp_board, player, pos)

        temp_score = score(temp_board)[1]

        if temp_score > max_score:
            max_score = temp_score
            max_pos = pos

    return max_pos


def run_single_player():

    cur_board = new_board()
    print_board(cur_board)
    player = int(input('Whose turn it is: '))

    while valid_moves(cur_board,1) !=[] or valid_moves(cur_board,2)!= []:

        if player == 1:
            strPos = input('Enter where to place your stone: ')
            if strPos != 'q':

                pos = position(strPos)
                if pos in valid_moves(cur_board,player):
                    (next_board, player) = next_state(cur_board,player,pos)

                    cur_board = next_board
                    print_board(cur_board)

            else:
                player = 2

        elif player == 2:

            max_pos = best_move(cur_board, 2)
            (next_board, player) = next_state(cur_board, player, max_pos)

            cur_board = next_board
            print_board(cur_board)
            print('Player 2 has placed a stone')

        print('Now is player ', player, 'turn')

    print(score(cur_board))


run_single_player()

