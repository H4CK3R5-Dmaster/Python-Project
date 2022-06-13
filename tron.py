import pygame
import sys
import database
 
class spieler:
    def __init__(self, name, farbe, startX, startY, leben):
        self.name = name
        self.farbe = farbe
        self.x = startX
        self.y = startY
        self.startX = startX
        self.startY = startY
        self.xBeweg = 0
        self.yBeweg = 0
        self.leben = leben
        self.start = True
    def moveDrawCol(self):
        self.x += self.xBeweg
        self.y += self.yBeweg
 
        if self.x < 0 or self.x >= 699 or self.y < 0 or self.y >= 699:
            self.leben -= 1
            return False
        farbe = screen.get_at((self.x, self.y))
        if (farbe == (0,150,255) or farbe == (255,150,0)) and self.start != True:
            self.leben -= 1
            return False
        else:
            screen.set_at((self.x, self.y), self.farbe)
            return True
    def richtung(self, xBeweg, yBeweg):
        self.start = False
        self.xBeweg = xBeweg
        self.yBeweg = yBeweg
    def richtungGeben(self):
        return (self.xBeweg,self.yBeweg)
    def lebenGeben(self):
        return self.leben
    def reset(self):
        self.start = True
        self.x = self.startX
        self.y = self.startY
        self.xBeweg = 0
        self.yBeweg = 0
    def nameGeben(self):
        return self.name
 
def textObjekt(text, font):
    textFlaeche = font.render(text, True, (255,255,255))
    return textFlaeche, textFlaeche.get_rect()
def select_name(i):
    if i == 1:
        
        return database.Database().select_limit("joueur", "joueur1")
    elif i == 2:  
        return database.Database().select_limit("joueur", "joueur2")  
     
print("premier joueur : ")


name = select_name(1)[0]
print(name)
sp1 = spieler(name, (255,150,0), 200, 300, 5)
print("2e joueur : ")
name = select_name(2)[0]
print(name)
sp2 = spieler(name, (0,150,255), 500, 300 ,5)
print("gooooo !")
 
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont('calibri', 40)
screen = pygame.display.set_mode([700,700])
 
while sp1.lebenGeben() > 0 and sp2.lebenGeben() > 0:
    go = True
    while go:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and sp1.richtungGeben()[1] != 1:
                    sp1.richtung(0, -1)
                elif event.key == pygame.K_RIGHT and sp1.richtungGeben()[0] != -1:
                    sp1.richtung(1, 0)
                elif event.key == pygame.K_DOWN and sp1.richtungGeben()[1] != -1:
                    sp1.richtung(0, 1)
                elif event.key == pygame.K_LEFT and sp1.richtungGeben()[0] != 1:
                    sp1.richtung(-1, 0)
 
                if event.key == pygame.K_z and sp2.richtungGeben()[1] != 1:
                    sp2.richtung(0, -1)
                elif event.key == pygame.K_d and sp2.richtungGeben()[0] != -1:
                    sp2.richtung(1, 0)
                elif event.key == pygame.K_s and sp2.richtungGeben()[1] != -1:
                    sp2.richtung(0, 1)
                elif event.key == pygame.K_q and sp2.richtungGeben()[0] != 1:
                    sp2.richtung(-1, 0)
 
        if sp1.moveDrawCol() == False or sp2.moveDrawCol() == False:
            screen.fill((0,0,0))
            sp1.reset()
            sp2.reset()
            go = False
 
        textGrund,textKasten = textObjekt(sp1.nameGeben() + ": " + str(sp1.lebenGeben()) + "     " + sp2.nameGeben() + ": " + str(sp2.lebenGeben()), font)
        textKasten.center = ((350,40))
        screen.blit(textGrund, textKasten)
 
        pygame.display.update()
        clock.tick(190)
 
if sp1.lebenGeben() == 0:
    name = sp2.nameGeben()
    name2 = sp1.nameGeben()
    task = (name, name2, 5, 0)
    database.Database().create_rq_insert("tron", task)
else:
    name = sp1.nameGeben()
    name2 = sp2.nameGeben()
    task = (name, name2, 5, 0)
    database.Database().create_rq_insert("tron", task)
 
textGrund, textKasten = textObjekt(name + " a gagné !", font)
textKasten.center = ((350,350))
screen.blit(textGrund, textKasten)
 
pygame.display.update()
pygame.time.wait(3000)