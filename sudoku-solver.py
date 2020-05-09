import pygame, sys

pygame.init()
clock = pygame.time.Clock()

screen_width = 520
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sudoku Solver")
bg_color = pygame.Color('white')
black_color = pygame.Color('black')
grey_color = pygame.Color('grey12')
blue_color = pygame.Color('blue')
white_color = pygame.Color('white')
inner_hover_color = (224, 224, 224)
button_font = pygame.font.Font("freesansbold.ttf", 15)

class Button():

    def __init__(self, xPos, text):

        self.width = screen_width/2 - 20
        self.height = 70
        self.xPos = xPos
        self.yPos = screen_height - 80

        self.innerButtonSurface = pygame.Rect(xPos+3, self.yPos+3, self.width-6, self.height-6)
        self.outerButtonSurface = pygame.Rect(xPos, self.yPos, self.width, self.height)

        self.innerColor = white_color
        self.outerColor = black_color

        self.text = button_font.render(text, False, black_color)

    def drawButton(self):
        pygame.draw.rect(screen, self.outerColor, self.outerButtonSurface)
        pygame.draw.rect(screen, self.innerColor, self.innerButtonSurface)
        x = (self.xPos+3 + (self.xPos+self.width))/2
        y = (self.yPos + (self.yPos+self.height))/2
        screen.blit(self.text, (x, y))

    def updateOnHover(self):
        if self.innerButtonSurface.collidepoint(pygame.mouse.get_pos()):
            self.innerColor = inner_hover_color
        else:
            self.innerColor = white_color

    def clicked(self):
        return self.innerButtonSurface.collidepoint(pygame.mouse.get_pos())

class Cell():
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.width=55
        self.analyzing = False
        self.clicked = False
        self.height=55
        self.x=col*self.width+12
        self.y=row*self.height+10
        self.cellRect = pygame.Rect(self.x, self.y, self.width, self.height)

    def setValue(self, value):
        self.value = value

    def setAnalyzing(self, val):
        self.analyzing = val

    def setClicked(self, val):
        self.clicked = val

    def getValue(self):
        return self.value

    def drawCell(self):
        if (not self.analyzing):
            if (not self.clicked):
                pygame.draw.rect(screen, grey_color, self.cellRect, 1)
            else:
                pygame.draw.rect(screen, blue_color, self.cellRect)
        else:
            pygame.draw.rect(screen, grey_color, self.cellRect)
        textX = (self.x+(self.x+self.width))/2 - 2
        textY = (self.y+(self.y+self.height))/2 - 2
        text = button_font.render(f"{self.value}", False, black_color)
        screen.blit(text, (textX, textY))

    def wasClicked(self):
        return self.cellRect.collidepoint(pygame.mouse.get_pos())


class Board():

    def __init__(self):
        self.width = screen_width - 25
        self.height = screen_height - 105
        self.surface = pygame.Rect(12, 10, self.width, self.height)
        self.cells = []
        self.resetBoard()

    def resetBoard(self):
        self.cells = []
        startingBoard=[[3, 0, 6, 5, 0, 8, 4, 0, 0],
         [5, 2, 0, 0, 0, 0, 0, 0, 0],
         [0, 8, 7, 0, 0, 0, 0, 3, 1],
         [0, 0, 3, 0, 1, 0, 0, 8, 0],
         [9, 0, 0, 8, 6, 3, 0, 0, 5],
         [0, 5, 0, 0, 9, 0, 6, 0, 0],
         [1, 3, 0, 0, 0, 0, 2, 5, 0],
         [0, 0, 0, 0, 0, 0, 0, 7, 4],
         [0, 0, 5, 2, 0, 6, 3, 0, 0]]
        for i in range(9):
            self.cells.append([])
            for j in range(9):
                self.cells[i].append(Cell(i, j, startingBoard[i][j]))

    def autoGenerate(self):
        print('TODO AUTOGENERATE BOARD')

    def verifyConstraints(self, row, col, value):

        # verifying unique nums in row
        for i in range(9):
            if self.cells[row][i].value == value:
                return False

        #verifying unique nums in col
        for i in range(9):
            if self.cells[i][col].value == value:
                return False

        # verifying unique nums in square group
        squareRow = row // 3
        squareCol = col // 3
        valuesInGroup = []

        # all cells in group
        for i in range(9):
            row = i // 3
            col = i % 3
            valuesInGroup.append(self.cells[squareRow*3+row][squareCol*3 + col].getValue())

        return value not in valuesInGroup

    def solveBoard(self, cellPos):

        pygame.time.wait(1)

        row = cellPos // 9
        col = cellPos % 9

        if (row >= 9):
            return True

        self.cells[row][col].setAnalyzing(True)

        screen.fill(bg_color)
        board.drawBoard()
        pygame.display.flip()  # does something?

        if (self.cells[row][col].value == 0):
            for i in range(1, 10):
                if (self.verifyConstraints(row, col, i)):
                    self.cells[row][col].setValue(i)

                    self.cells[row][col].setAnalyzing(False)
                    win = self.solveBoard(cellPos+1)
                    self.cells[row][col].setAnalyzing(True)

                    # if win is found, no need to try out other numbers
                    # only one unique solution anyways
                    if win:
                        break

                    # backtracking in case where input of i in cur cell
                    # results in a non win, therefore, undoing it and moving onto next i
                    else:
                        self.cells[row][col].setValue(0)
                else:
                    win = False
        else:
            self.cells[row][col].setAnalyzing(False)
            win = self.solveBoard(cellPos+1)
            self.cells[row][col].setAnalyzing(True)

        self.cells[row][col].setAnalyzing(False)
        return win

    # kinda redundant
    def clickCell(self):
        for i in range(81):
            row = i // 9
            col = i % 9
            if self.cells[row][col].wasClicked():
                self.cells[row][col].setClicked(True)
            else:
                self.cells[row][col].setClicked(False)

    def cellClicked(self):
        for i in range(81):
            row = i // 9
            col = i % 9
            if self.cells[row][col].wasClicked():
                return True

        return False

    def drawBoard(self):
        pygame.draw.rect(screen, black_color, self.surface, 3)

        #drawing cells
        for i in range(9):
            for j in range(9):
                self.cells[i][j].drawCell()

        # bold lines
        pygame.draw.line(screen, black_color, (55*3 + 12, 10), (55*3+12, self.height+10), 4)
        pygame.draw.line(screen, black_color, (55*6 + 12, 10), (55*6+12, self.height+10), 4)

        pygame.draw.line(screen, black_color, (12, 55*3 + 10), (self.width+10, 55*3+10), 4)
        pygame.draw.line(screen, black_color, (12, 55*6 + 10), (self.width+10, 55*6+10), 4)

board = Board()
resetButton = Button(10, "Reset")
solveButton = Button(270, "Solve")

def main():
    while True:
        for event in pygame.event.get():  # list of all user inputs, pygame calls all actions events
            if event.type == pygame.QUIT:
                pygame.quit()  # uninitialize pygame module
                sys.exit()  # close window
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resetButton.clicked():
                    board.autoGenerate()
                if solveButton.clicked():
                    board.solveBoard(0)
                if board.cellClicked():
                    board.clickCell()

        screen.fill(bg_color)

        board.drawBoard()
        resetButton.drawButton()
        resetButton.updateOnHover()
        solveButton.drawButton()
        solveButton.updateOnHover()

        pygame.display.flip()  # does something?
        clock.tick(60)  # limits loop speed

if __name__ == "__main__":
    main()