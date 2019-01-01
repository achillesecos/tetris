# Updated Animation Starter Code

from tkinter import *
import random

#Name: Achilles Ecos
#AndrewID: aecos
####################################
# customize these functions
####################################

#initialize all the variables to make the game 
def init(data):
    data.rows, data.cols, data.cellSize, data.margin = gameDimensions()
    data.emptyColor = 'blue'
    data.score = 0
    data.board = []

    for i in range(data.rows):
        data.board.append([data.emptyColor] * data.cols)


    iPiece = [ [True,  True, True, True ] ]

    jPiece = [ [ True,  False,  False ],
               [True,  True, True ] ]
    
    lPiece = [ [ False,  False,  True ],
               [True,  True, True ] ]

    oPiece = [ [ True,  True],
               [True,  True] ]

    sPiece = [ [ False,  True,  True ],
               [True,  True, False ] ]

    tPiece = [ [ False,  True,  False ],
               [True,  True, True ] ]

    zPiece = [ [ True,  True,  False ],
               [False,  True, True ] ]

    data.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece,
                          zPiece ]

    data.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan",
                               "green", "orange" ]

    data.fallingPiece = []
    data.fallingPieceColor = ''

    newFallingPiece(data)
    data.gameOver = False



def mousePressed(event, data):
    # use event.x and event.y
    pass

#change the pieces and restart the game when keys are pressed
def keyPressed(event, data):
    if event.keysym == "r":
        init(data)
    if data.gameOver:
        return
    if event.keysym == "Up":
        rotateFallingPiece(data)
 
    if event.keysym == "Down":
        moveFallingPiece(data, 1, 0)
    if event.keysym == "Left":
        moveFallingPiece(data, 0, -1)
    if event.keysym == "Right":
        moveFallingPiece(data, 0, 1)
    

def timerFired(data):
    pass

#will redraw the board when all the parts of the game are considered
def redrawAll(canvas, data):
    drawBoard(canvas, data)
    drawFallingPiece(canvas, data)
    drawScore(canvas, data)
    if (data.gameOver):
        canvas.create_text(data.width / 2, data.height / 2,
                           text ="Game Over", font="Times 30", fill = "white")

#initial game dimensions
def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return (rows, cols, cellSize, margin)

#will loop through the board to draw the board to fit canvas
def drawBoard(canvas, data):
    s = data.cellSize
    for i in range(len(data.board)):
        for j in range(len(data.board[0])):
            drawCell(canvas, data.margin + (j * s) , data.margin + (i * s), s,
                     data.board[i][j])

#will draw the cell
def drawCell(canvas, x, y, s, color):
    canvas.create_rectangle(x, y, x + s, y + s, fill = color)

#runs the game with the board height and board width
def playTetris():
    rows, cols, cellSize, margin = gameDimensions()

    boardHeight = (cellSize * rows) + (2 * margin)
    boardWidth = (cellSize * cols) + (2 * margin)
    run(boardWidth, boardHeight)

#this function makes a new piece fall from the top of the game
def newFallingPiece(data):
    
    randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
    data.fallingPiece = data.tetrisPieces[randomIndex]
    data.fallingPieceColor = data.tetrisPieceColors[randomIndex]
    data.fallingPieceRow = 0
    data.fallingPieceCol = data.cols//2 - (pieceWidth(data.fallingPiece)//2)

#returns the width of the piece
def pieceWidth(piece):
    return len(piece[0])

#the falling piece will be drawn according to the specifications from the
#newFallingPiece() function
def drawFallingPiece(canvas, data):
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            if(data.fallingPiece[i][j]):
                drawCell(canvas, data.margin + (data.cellSize *
                                                (data.fallingPieceCol + j)),
                         data.margin + (data.cellSize * (data.fallingPieceRow
                         + i)), data.cellSize, data.fallingPieceColor)

#returns True and False if the falling piece is able to be moved
def moveFallingPiece(data, drow, dcol):
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    if not(fallingPieceIsLegal(data)):
        data.fallingPieceRow -= drow
        data.fallingPieceCol -= dcol
        return False
    return True

#returns True if the falling piece is legal after a move has been made so it
#doesnt interfere with other spaces around it
def fallingPieceIsLegal(data):
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            if(data.fallingPiece[i][j] and
               ((data.fallingPieceRow > data.rows-len(data.fallingPiece)) or
               (data.fallingPieceCol < 0) or
               (data.fallingPieceCol + len(data.fallingPiece[i])-1 > data.cols
                - 1) or
               (data.board[i+data.fallingPieceRow][j + data.fallingPieceCol]
                != data.emptyColor))
               ):
                return False 
    return True

#this will rotate the falling piece 
def rotateFallingPiece(data):
 
    data.tempDimensions = (len(data.fallingPiece), len(data.fallingPiece[0]))
    data.tempLocation = (data.fallingPieceRow, data.fallingPieceCol)
    data.tempPiece = data.fallingPiece 

    data.newDimensions = (data.tempDimensions[1], data.tempDimensions[0])

    newRow = data.fallingPieceRow + len(data.fallingPiece)//2 - \
    len(data.fallingPiece[0])//2

    newCol = data.fallingPieceCol + len(data.fallingPiece[0])//2 - \
    len(data.fallingPiece)//2

    newLst = []

    for i in range(data.newDimensions[0]):
        newLst.append([None] * data.newDimensions[1])

    for i in range(len(newLst)):
        for j in range(len(newLst[0])):
            newLst[i][j] = data.fallingPiece[j][(len(data.fallingPiece[0])-i)-1]
    data.fallingPiece = newLst
    data.fallingPieceRow = newRow
    data.fallingPieceCol = newCol
    if not(fallingPieceIsLegal(data)):
        data.fallingPiece = data.tempPiece
        data.fallingPieceRow = data.tempLocation[0]
        data.fallingPieceCol = data.tempLocation[1]

#it is called every time the timer delayed happens so that it update the game
def timerFired(data):
    if (not moveFallingPiece(data, 1, 0)):
        placeFallingPiece(data)
        if (not fallingPieceIsLegal(data)):
            data.gameOver = True

#this will change the board by placing the piece on the board
def placeFallingPiece(data):
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            if (data.fallingPiece[i][j]):
                data.board[i+data.fallingPieceRow][j+data.fallingPieceCol] = \
                data.fallingPieceColor
    data.score += removeFullRows(data)
    if (not(data.gameOver)):
        newFallingPiece(data)

#once a full row is filled up, it will remove that whole row and have everything
#move down one row
def removeFullRows(data):
    boardCopy = [] 
    fullRows = 0
    for i in range(len(data.board)):
        full = True
        for j in range(len(data.board[0])):
            if (data.board[i][j] == data.emptyColor):
                full = False
                break
        if not full:
            boardCopy.append(data.board[i])
        else:
            fullRows += 1     
    while len(boardCopy) < len(data.board):
        boardCopy.insert(0, [data.emptyColor] * data.cols)
    data.board = boardCopy
    return fullRows

#will just draw score
def drawScore(canvas, data):
    canvas.create_text(data.width / 2, 10, text = "Score: " + str(data.score))

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 500 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

playTetris()
