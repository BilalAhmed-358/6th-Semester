def Solution():

    N = int(input(("Enter the value of n (Make sure its  4<=n<=8 )\n")))

    while N < 4 or N > 8:
        N = int(input(('The value must be  4<=n<=8\n')))
    chessBoard = [[] for i in range(N)]
    for i in range(N):
        for j in range(N):
            chessBoard[i].append(0)

    if keepSolvingUntil(chessBoard, 0, N) == False:
        print("The solution to the given problem doesnot exist")
        return False

    printSolution(chessBoard, N)
    return True


def keepSolvingUntil(chessBoard, col, N):
    if col >= N:
        return True

    for i in range(N):

        if safePositionCheck(chessBoard, i, col, N):
            chessBoard[i][col] = 1

            if keepSolvingUntil(chessBoard, col + 1, N) == True:
                return True

            chessBoard[i][col] = 0

    return False


def safePositionCheck(chessBoard, row, col, N):
    for i in range(col):
        if chessBoard[row][i] == 1:
            return False

    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if chessBoard[i][j] == 1:
            return False

    for i, j in zip(range(row, N, 1), range(col, -1, -1)):
        if chessBoard[i][j] == 1:
            return False

    return True


def printSolution(chessBoard, N):
    print("The final solution to the given problem is:\n")
    for i in range(N):
        for j in range(N):
            print(chessBoard[i][j], end=' ')
        print()
    print()


Solution()
