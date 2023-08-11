import pygame as p
import setting as s
import loadimg as l
import chessEngine
import button as b
import playWithMachine as pWM
chessManImg = l.loadChessMan()
boardImg = l.loadBoard()
lightImg = l.loadLight()
squareImg = l.loadSquare()
st = False
pa = False
def startGame():
    global st
    st= True
    print("start game")
def playAgainGame():
    global pa
    pa = True
    print("play again game")
def setup():
    global pa
    global st
    p.init()
    pa = False
    st = False
    p.display.set_caption('Chinese Chess')
def shutDown():
    p.quit()

def mainLoop():

    screen = p.display.set_mode((s.SCREEN_WIDTH,s.SCREEN_HEIGHT))
    clock = p.time.Clock()
    gs = chessEngine.State()
    run = True
    listClick=[]
    cell =()
    
    objects=()
    backwardBut = b.Button(s.BACKWARD_X, s.BACKWARD_Y, s.BUT_WIDTH, s.BUT_HEIGHT,'re', l.loadButton('backward'), gs.reMove)
    nextstepBut = b.Button(s.NEXTSTEP_X, s.NEXTSTEP_Y, s.BUT_WIDTH, s.BUT_HEIGHT,'ne', l.loadButton('nextstep'), gs.nextMove)
    reverseBut = b.SButton(s.REVERSE_X, s.REVERSE_Y, s.BUT_WIDTH, s.BUT_HEIGHT,'ex', l.loadButton('reverse'), gs.reverse)
    startBut = b.Button(s.START_X, s.START_Y, s.BUT_WIDTH, s.BUT_HEIGHT,'st', l.loadButton('start'), startGame)
    playAgainBut = b.SButton(s.REPLAY_X, s.REPLAY_Y, s.BUT_WIDTH, s.BUT_HEIGHT,'pa', l.loadButton('replay'), playAgainGame)
    
    # objects.append(backwardBut)
    # objects.append(nextstepBut)
    # objects.append(reverseBut)
    # objects.append(startBut)
    objects += (backwardBut,nextstepBut,reverseBut,startBut,playAgainBut)
    while run:
        drawGameState(screen,gs)
        global st
        global pa
        
        for e in p.event.get():
            
            if e.type == p.QUIT:
                run = False
            
            elif e.type == p.MOUSEBUTTONDOWN:
                print("clickk")
                if st == False: continue
                print("click success")
                start = s.GRID
                pos = p.mouse.get_pos() 
              
                row = int((pos[1]-start[0])//start[2])
                col = int((pos[0]-start[1])//start[2])
                if row >9 or col >8 or row <0 or col <0:
                    # if row ==4 and col ==11:
                    #     drawClick(screen,'backward')
                    # elif row == 4 and col ==12:
                    #     drawClick(screen,'nextstep')
                    break
                if listClick ==[]:
                    if (gs.redMove and gs.board[row][col][0] == 'b') or (not gs.redMove and gs.board[row][col][0] == 'r'): break
                
                listClick.append((row,col))
                if 0<= row <=9 and 0<= col <=8:
                    if gs.board[listClick[0][0]][listClick[0][1]]=='---':
                        listClick =[]
                    else:
                        gs.selectedCell = listClick[0]
                        
                    if len(listClick) ==2:
                        if listClick[0] == listClick[1]:
                            listClick =[]
                        else:
                            listValid = gs.checkValid(gs.selectedCell)
                            if listClick[1] in listValid:
                                move = chessEngine.Move(gs,listClick[0], listClick[1])
                                gs.makeMove(move)
                                if not gs.checkEnd():
                                    print("AI turn: ", not gs.redMove)
                                    gs.playWithAI()
                                else:
                                    print("you win")
                                    if pa:
                                        print("start game")
                                        
                                        
                                        
                                #drawChessMate(screen,gs)
                            listClick =[]
                        gs.selectedCell = ()
            elif gs.after and st:
                gs.playWithAI()
        if pa:
            pa = False
            print("play again chuaw")
            main()    
        for o in objects:
            o.process(screen,gs)
        drawFoot(screen,gs)
        clock.tick(s.MAX_FPS)
        p.display.flip()

def main():
    setup()
    mainLoop()
    shutDown()
        
        
def drawValid(screen,gs):
    listValid = gs.checkValid(gs.selectedCell)
    start = s.GRID
    for i in listValid:
        screen.blit(lightImg, p.Rect(start[1]+ i[1]*start[2],start[0]+i[0]*start[2], s.CELL_SIZE, s.CELL_SIZE))
def drawGameState(screen,gs):
    screen.blit(boardImg,(0,0))
    drawChessMan(screen,gs.board)
    if gs.selectedCell != ():
        drawValid(screen,gs)
        screen.blit(squareImg, p.Rect(s.GRID[1]+ gs.selectedCell[1]*s.GRID[2],s.GRID[0]+gs.selectedCell[0]*s.GRID[2], s.CELL_SIZE, s.CELL_SIZE))
    if gs.checkMate():
        drawChessMate(screen,gs)
    if gs.checkEnd():
        drawEndGame(screen,gs)
def drawChessMan(screen,board):
    start = s.GRID
    for i in range(s.DIMENSION+1):
        for j in range(s.DIMENSION):
            chessMan = board[i][j]
            if chessMan != '---':  
                screen.blit(chessManImg[chessMan],p.Rect(start[1]+j*start[2],start[0]+i*start[2],s.CELL_SIZE,s.CELL_SIZE))
def drawFoot(screen, gs: chessEngine.State):
    if gs.moveLog == []:
        return
    startRow = gs.moveLog[-1].startRow
    startCol = gs.moveLog[-1].startCol
    endRow = gs.moveLog[-1].endRow
    endCol = gs.moveLog[-1].endCol
    screen.blit(squareImg, p.Rect(s.GRID[1]+ startCol*s.GRID[2],s.GRID[0]+startRow*s.GRID[2], s.CELL_SIZE, s.CELL_SIZE))
    screen.blit(squareImg, p.Rect(s.GRID[1]+ endCol*s.GRID[2],s.GRID[0]+endRow*s.GRID[2], s.CELL_SIZE, s.CELL_SIZE))
def drawChessMate(screen, gs: chessEngine.State):
    if gs.checkMate():
        p.font.init()
        myFont = p.font.SysFont('Comic Sans MS', 30)
        textSurface = myFont.render('Checkmate', False, (0, 0, 0))
        screen.blit(textSurface,(s.WIDTH/2 - textSurface.get_width()/2, s.SCREEN_HEIGHT/2 - textSurface.get_height()/2))
def drawEndGame(screen, gs: chessEngine.State):
    if gs.checkEnd():
        p.font.init()
        myFont = p.font.SysFont('Comic Sans MS', 30)
        textSurface = myFont.render('End game', False, (0, 0, 0))
        screen.blit(textSurface,(s.WIDTH/2 - textSurface.get_width()/2, s.SCREEN_HEIGHT/2 - textSurface.get_height()/2))


if __name__ == '__main__':
    main()
    