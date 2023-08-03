import pygame as p
import setting as s
import loadimg as l

class Button:
    def __init__(self, x, y, width, height,type,img, onClickFunction =None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onClickFunction = onClickFunction
        self.img = {
            'normal': img[0],
            'hover': img[1],
            'pressed': img[2],
            'active': img[3]
        }
        self.state = 'normal'
        self.isPress = False
        self.active = False
        self.type = type
    def process(self, screen, gs):
        pos = p.mouse.get_pos()
        if self.type =='re':
            if gs.moveLog ==[]:
                self.state = 'normal'
            else:
                self.state = 'active'
                
        else:
            if gs.store == []:
                self.state = 'normal'
            else:
                self.state = 'active'
        if self.state =='active':
            if self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height:
                self.state = 'hover'
                if p.mouse.get_pressed()[0] and not self.isPress:
                    self.state = 'pressed'
                    self.isPress =True
                    self.onClickFunction()
                else:
                    self.isPress = False
            
                
        screen.blit(self.img[self.state], (self.x, self.y))

