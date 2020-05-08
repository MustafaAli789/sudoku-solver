import pygame, sys

pygame.init()
clock = pygame.time.Clock()

screen_width = 520
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sudoku Solver")
bg_color = pygame.Color('white')
black_color = pygame.Color('black')
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
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            self.innerColor = white_color
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

class Cell():
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.width=55
        self.height=55
        self.x=col*self.width+12
        self.y=row*self.height+10
        self.cellRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text = button_font.render(f"{value}", False, black_color)

    def setValue(self, value):
        self.value = value

    def drawCell(self):
        pygame.draw.rect(screen,black_color, self.cellRect, 1)
        textX = (self.x+(self.x+self.width))/2 - 2
        textY = (self.y+(self.y+self.height))/2 - 2
        screen.blit(self.text, (textX, textY))

class Board():

    def __init__(self):
        self.width = screen_width - 25
        self.height = screen_height - 105
        self.surface = pygame.Rect(12, 10, self.width, self.height)
        self.cells = []
        self.resetBoard()

    def resetBoard(self):
        self.cells = []
        for i in range(9):
            self.cells.append([])
            for j in range(9):
                self.cells[i].append(Cell(i, j, 0))

    def drawBoard(self):
        pygame.draw.rect(screen, black_color, self.surface, 3)

        #drawing cells
        for i in range(9):
            for j in range(9):
                self.cells[i][j].drawCell()

        # bold lines
        pygame.draw.line(screen, black_color, (55*3 + 12, 10), (55*3+12, self.height+10), 3)
        pygame.draw.line(screen, black_color, (55*6 + 12, 10), (55*6+12, self.height+10), 3)

        pygame.draw.line(screen, black_color, (12, 55*3 + 10), (self.width+10, 55*3+10), 3)
        pygame.draw.line(screen, black_color, (12, 55*6 + 10), (self.width+10, 55*6+10), 3)

board = Board()
resetButton = Button(10, "Reset")
solveButton = Button(270, "Solve")

def main():
    while True:
        for event in pygame.event.get():  # list of all user inputs, pygame calls all actions events
            if event.type == pygame.QUIT:
                pygame.quit()  # uninitialize pygame module
                sys.exit()  # close window

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