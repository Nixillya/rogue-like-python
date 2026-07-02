import pygame
import numpy
import random
import keyboard
import time

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
running = True
#----------------------------------------------------------------------------------------------------------------------------------------

# LORE

"""
O jogador se encontra em um desafio entre a vida e a morte e ele precisa chegar até o final para 
mostrar o seu verdadeiro significado e ir para o paraiso.

Pode se entender que o jogador se encontra em um tipo de punição
onde ele luta infinitamente contra a personificação dos seus proprios pecados. 

mas ele nunca percebeu isso e acredita que deve continuar lutando
cada morte é uma nova memoria e tentativa perdida de tentar chegar em algo que nunca existiu de verdade.
"""

# Dungeons Of Sin

#----------------------------------------------------------------------------------------------------------------------------------------
class POS:
    def __init__(self):
        self.x = -1
        self.y = -1
class ATTRIBUTES:
    def __init__(self):
        self.hp = 10
        self.hpMax = 10
        self.defense = 10
        self.strength = 10
        self.dexterity = 1
        self.intelligence = 1
class ITEM:
    def __init__(self):
        self.id = 0
        self.heal = 0
        self.hp = 0
        self.strength = 0
        self.defense = 0
        self.dexterity = 0
        self.intelligence = 0
        self.cursed = False
        self.reveled = False
        self.breakChance = 0
        self.goBreak = False
class PLAYER:
    def __init__(self):
        self.attPoints = 5
        self.level = 1
        self.gold = 0
        self.exp = 0
        self.nextExp = 1
        self.keyInput = 0
        self.clockSpeed = time.perf_counter()
        self.alive = True
        self.inventoryOpened = False
        self.fallen = False
        self.key = False
        self.firstAtt = True
        self.inventory = numpy.array([[ITEM() for _ in range(3)] for _ in range(4)])
        self.pos = POS()
        self.camPos = POS()
        self.inventorySelection = POS()
        self.inventorySelection.x = 0
        self.inventorySelection.y = 0
        self.attributes = ATTRIBUTES()
        self.dice = random.randint(1,100)
class MONSTER:
    def __init__(self):
        self.id = 0
        self.alive = False
        self.attacked = False
        self.key = False
        self.clockSpeed = time.perf_counter()
        self.pos = POS()
        self.camPos = POS()
        self.attributes = ATTRIBUTES()
        self.dice = random.randint(1,100)
class DAMAGESVIEW:
    def __init__(self):
        self.value = 0
        self.id = 0
        self.pos = POS()
        self.size = 0
class MAP:
    def __init__(self):
        self.tiles = numpy.zeros((1000,1000))
        self.memory = numpy.zeros((1000,1000))
        self.floor = 0
        self.player = PLAYER()
        self.key = POS()
        self.items = numpy.array([POS() for _ in range(1)])
        self.potionsColor = [(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255))]
        self.monsters = numpy.array([MONSTER() for _ in range(1)])
        self.damagesView = numpy.array([DAMAGESVIEW() for _ in range(50)])
class MENU:
    selection = 0
class GAME:
    attSelection = 0
    map = MAP()
    menu = MENU()
    play = False
    next = True
#----------------------------------------------------------------------------------------------------------------------------------------
def clear_slot(game = GAME(),y=0,x=0):
    game.map.player.inventory[y][x].id = 0
    game.map.player.inventory[y][x].defense = 0
    game.map.player.inventory[y][x].dexterity = 0
    game.map.player.inventory[y][x].heal = 0
    game.map.player.inventory[y][x].hp = 0
    game.map.player.inventory[y][x].intelligence = 0
    game.map.player.inventory[y][x].strength = 0
    game.map.player.inventory[y][x].cursed = False
    game.map.player.inventory[y][x].reveled = False
    game.map.player.inventory[y][x].breakChance = 0
    game.map.player.inventory[y][x].goBreak = False
#----------------------------------------------------------------------------------------------------------------------------------------
def render_inventory(game = GAME()):
    
    font = pygame.font.SysFont('Comic Sans MS', 20)
    defense_text = font.render(f'Defense: {game.map.player.attributes.defense}', True, (255, 255, 255))
    screen.blit(defense_text, (210,20))
    strength_text = font.render(f'strength: {game.map.player.attributes.strength}', True, (255, 255, 255))
    screen.blit(strength_text, (210,45))
    intelligence_text = font.render(f'Intelligence: {game.map.player.attributes.intelligence}', True, (255, 255, 255))
    screen.blit(intelligence_text, (210,70))
    dexterity_text = font.render(f'Dexterity: {game.map.player.attributes.dexterity:.1f}', True, (255, 255, 255))
    screen.blit(dexterity_text, (210,90))

    pygame.draw.rect(screen,"#1D1D1D",(10,10,190,250))
    pygame.draw.polygon(screen,"#FFFFFF",[[10,10],[200,10],[200,260],[10,260]],2)

    if(game.map.player.inventorySelection.y<0):
        game.map.player.inventorySelection.y = 0
    if(game.map.player.inventorySelection.y>3):
        game.map.player.inventorySelection.y = 3
    if(game.map.player.inventorySelection.x<0):
        game.map.player.inventorySelection.x = 0
    if(game.map.player.inventorySelection.x>2):
        game.map.player.inventorySelection.x = 2
    y = 20
    x = 20
    for j in range(4):
        for i in range(3):
            if(game.map.player.inventorySelection.y == j and game.map.player.inventorySelection.x == i):
                pygame.draw.rect(screen,"#424242",(x,y,50,50))
                pygame.draw.polygon(screen,"#FFFFFF",[[x,y],[x+50,y],[x+50,y+50],[x,y+50]],1)
            if(game.map.player.inventory[j][i].id==1):
                pygame.draw.rect(screen, "#8B5A2B", (x+20, y+5, 10, 5))
                pygame.draw.rect(screen, "#C8C8C8", (x+18, y+10, 14, 8))
                pygame.draw.rect(screen, "#C8C8C8", (x+10, y+18, 30, 20))
                pygame.draw.rect(screen, "#C8C8C8", (x+12, y+38, 26, 5)) 
                pygame.draw.rect(screen, game.map.potionsColor[0], (x+13, y+25, 24, 15))
                pygame.draw.rect(screen, "#FFFFFF", (x+15, y+22, 3, 12))
            if(game.map.player.inventory[j][i].id==2):
                pygame.draw.rect(screen, "#8B5A2B", (x+20, y+5, 10, 5)) 
                pygame.draw.rect(screen, "#C8C8C8", (x+18, y+10, 14, 8))
                pygame.draw.rect(screen, "#C8C8C8", (x+10, y+18, 30, 20))
                pygame.draw.rect(screen, "#C8C8C8", (x+12, y+38, 26, 5)) 
                pygame.draw.rect(screen, game.map.potionsColor[1], (x+13, y+25, 24, 15))
                pygame.draw.rect(screen, "#FFFFFF", (x+15, y+22, 3, 12))
            if(game.map.player.inventory[j][i].id==3):
                pygame.draw.rect(screen, "#8B5A2B", (x+20, y+5, 10, 5)) 
                pygame.draw.rect(screen, "#C8C8C8", (x+18, y+10, 14, 8))
                pygame.draw.rect(screen, "#C8C8C8", (x+10, y+18, 30, 20))
                pygame.draw.rect(screen, "#C8C8C8", (x+12, y+38, 26, 5)) 
                pygame.draw.rect(screen, game.map.potionsColor[2], (x+13, y+25, 24, 15)) 
                pygame.draw.rect(screen, "#FFFFFF", (x+15, y+22, 3, 12)) 
            if(game.map.player.inventory[j][i].id==4):
                pygame.draw.rect(screen, "#8B5A2B", (x+20, y+5, 10, 5)) 
                pygame.draw.rect(screen, "#C8C8C8", (x+18, y+10, 14, 8))
                pygame.draw.rect(screen, "#C8C8C8", (x+10, y+18, 30, 20))
                pygame.draw.rect(screen, "#C8C8C8", (x+12, y+38, 26, 5)) 
                pygame.draw.rect(screen, game.map.potionsColor[3], (x+13, y+25, 24, 15))
                pygame.draw.rect(screen, "#FFFFFF", (x+15, y+22, 3, 12))
            if(game.map.player.inventory[j][i].id==5):
                pygame.draw.rect(screen, "#8B5A2B", (x+20, y+5, 10, 5))
                pygame.draw.rect(screen, "#C8C8C8", (x+18, y+10, 14, 8))
                pygame.draw.rect(screen, "#C8C8C8", (x+10, y+18, 30, 20))
                pygame.draw.rect(screen, "#C8C8C8", (x+12, y+38, 26, 5)) 
                pygame.draw.rect(screen, game.map.potionsColor[4], (x+13, y+25, 24, 15))
                pygame.draw.rect(screen, "#FFFFFF", (x+15, y+22, 3, 12))
            if(game.map.player.inventory[j][i].id==6): # ESPADA
                pygame.draw.rect(screen, "#D8D8D8", (x+22, y+5, 6, 25)) 
                pygame.draw.rect(screen, "#D8D8D8", (x+23, y+3, 4, 2)) 
                pygame.draw.rect(screen, "#D8D8D8", (x+24, y+1, 2, 2)) 
                pygame.draw.rect(screen, "#C9A227", (x+15, y+30, 20, 4))
                pygame.draw.rect(screen, "#8B5A2B", (x+22, y+34, 6, 10))
                pygame.draw.rect(screen, "#C9A227", (x+21, y+44, 8, 3)) 
            if(game.map.player.inventory[j][i].id==7): # ESCUDO
                pygame.draw.circle(screen, "#707070", (x+25, y+25), 18)
                pygame.draw.circle(screen, "#C8C8C8", (x+25, y+25), 15)
                pygame.draw.rect(screen, "#E8E8E8", (x+23, y+12, 4, 26))
                pygame.draw.rect(screen, "#E8E8E8", (x+12, y+23, 26, 4))
                pygame.draw.circle(screen, "#AAAAAA", (x+25, y+25), 4)
            if(game.map.player.inventory[j][i].id==8): # ANEL
                pygame.draw.circle(screen, "#FFD700", (x+25, y+25), 12)
                pygame.draw.circle(screen, "#1D1D1D", (x+25, y+25), 8)
                if(game.map.player.inventorySelection.y == j and game.map.player.inventorySelection.x == i):
                    pygame.draw.circle(screen, "#424242", (x+25, y+25), 8)
                pygame.draw.circle(screen, "#FF4040", (x+25, y+11), 4)
                pygame.draw.circle(screen, "#FFFFFF", (x+24, y+10), 1)
            if(game.map.player.inventory[j][i].id==9): # TOTEM DE RESSUREIÇÃO
                pygame.draw.rect(screen, "#FFD700", (x+22, y+8, 6, 28)) 
                pygame.draw.rect(screen, "#FFD700", (x+12, y+16, 26, 6))
                pygame.draw.rect(screen, "#FFD700", (x+18, y+36, 14, 5))
                pygame.draw.rect(screen, "#FFFFFF", (x+20, y+15, 10, 6))
                pygame.draw.rect(screen, "#FFF3A0", (x+20, y+5, 10, 3)) 
            if(game.map.player.inventory[j][i].id==10): # TOTEM DA VIDA
                pygame.draw.rect(screen, "#43FF52", (x+22, y+8, 6, 28)) 
                pygame.draw.rect(screen, "#43FF52", (x+12, y+16, 26, 6))
                pygame.draw.rect(screen, "#43FF52", (x+18, y+36, 14, 5))
                pygame.draw.rect(screen, "#FFFFFF", (x+20, y+15, 10, 6))
                pygame.draw.rect(screen, "#BEFFA0", (x+20, y+5, 10, 3)) 
            if(game.map.player.inventory[j][i].id==11): # CAJADO
                pygame.draw.line(screen, "#8B5A2B", (x+18, y+42), (x+30, y+12), 5)
                pygame.draw.circle(screen, "#66CCFF", (x+32, y+10), 7)
                pygame.draw.circle(screen, "#AADDFF", (x+30, y+8), 2)
            if(game.map.player.inventory[j][i].id==12): # ESCUDO REFLETOR
                pygame.draw.polygon(screen, "#707070", [(x+25, y+5),(x+38, y+12),(x+40, y+25),(x+35, y+36),(x+25, y+45),(x+15, y+36),(x+10, y+25),(x+12, y+12)])
                pygame.draw.polygon(screen, "#C8C8C8", [(x+25, y+9),(x+35, y+15),(x+36, y+24),(x+32, y+33),(x+25, y+40),(x+18, y+33),(x+14, y+24),(x+15, y+15)])
                pygame.draw.rect(screen, "#E8E8E8", (x+23, y+12, 4, 24))
                pygame.draw.rect(screen, "#E8E8E8", (x+17, y+20, 16, 4))
            if(game.map.player.inventory[j][i].id==13): # ESCUDO ANTI-MALDIÇÃO
                pygame.draw.polygon(screen, "#707070", [(x+25, y+5),(x+39, y+15),(x+36, y+32),(x+25, y+45),(x+14, y+32),(x+11, y+15)])
                pygame.draw.polygon(screen, "#D0D0D0", [(x+25, y+9),(x+35, y+16),(x+33, y+30),(x+25, y+39),(x+17, y+30),(x+15, y+16)])
                pygame.draw.line(screen, "#FFFFFF", (x+18, y+12), (x+25, y+38), 2)
            if(game.map.player.inventory[j][i].cursed and game.map.player.inventory[j][i].reveled):
                pygame.draw.circle(screen,"#FF0000",[x+random.randint(10,40),y+random.randint(10,40)],random.randint(1,10))
            x+=60
        y+=60
        x = 20
#----------------------------------------------------------------------------------------------------------------------------------------
def move_monsters(game = GAME()):
    for monster in game.map.monsters:
        Y = 525
        X = 525
        if(game.map.player.keyInput==1):
            monster.camPos.y+=50
        if(game.map.player.keyInput==2):
            monster.camPos.y-=50
        if(game.map.player.keyInput==3):
            monster.camPos.x+=50
        if(game.map.player.keyInput==4):
            monster.camPos.x-=50
        if(game.map.player.keyInput==5):
            monster.camPos.y = (monster.pos.y*50-game.map.player.pos.y*50)
            monster.camPos.x = (monster.pos.x*50-game.map.player.pos.x*50)
        speed = int(monster.attributes.dexterity)
        if(speed>50):
            speed = 50
        if(speed<5):
            speed = 5
        if((monster.pos.y*50-game.map.player.pos.y*50)>monster.camPos.y):
            monster.camPos.y+=random.randint(2,speed)
        if((monster.pos.y*50-game.map.player.pos.y*50)<monster.camPos.y):
            monster.camPos.y-=random.randint(2,speed)
        if((monster.pos.x*50-game.map.player.pos.x*50)>monster.camPos.x):
            monster.camPos.x+=random.randint(2,speed)
        if((monster.pos.x*50-game.map.player.pos.x*50)<monster.camPos.x):
            monster.camPos.x-=random.randint(2,speed)
        if((monster.pos.y-game.map.player.pos.y>=0-11 and monster.pos.y-game.map.player.pos.y<=11) and (monster.pos.x-game.map.player.pos.x>=0-11 and monster.pos.x-game.map.player.pos.x<=11)):
            if(monster.id==0):
                pygame.draw.circle(screen,"#4E002B",[X+monster.camPos.x+random.randint(-2,2),Y+monster.camPos.y+random.randint(-2,2)],20)
                pygame.draw.circle(screen,"#4E002B",[X+monster.camPos.x+random.randint(10,40)-25,Y+monster.camPos.y+random.randint(10,40)-25],random.randint(1,10))
            if(monster.id==1):
                pygame.draw.circle(screen,"#700000",[X+monster.camPos.x+random.randint(-2,2),Y+monster.camPos.y+random.randint(-2,2)],20)
                pygame.draw.circle(screen,"#700000",[X+monster.camPos.x+random.randint(10,40)-25,Y+monster.camPos.y+random.randint(10,40)-25],random.randint(1,10))
            if(monster.id==2):
                pygame.draw.circle(screen,"#137000",[X+monster.camPos.x+random.randint(-2,2),Y+monster.camPos.y+random.randint(-2,2)],20)
                pygame.draw.circle(screen,"#137000",[X+monster.camPos.x+random.randint(10,40)-25,Y+monster.camPos.y+random.randint(10,40)-25],random.randint(1,10))
            if(monster.id==3):
                pygame.draw.circle(screen,"#706500",[X+monster.camPos.x+random.randint(-2,2),Y+monster.camPos.y+random.randint(-2,2)],20)
                pygame.draw.circle(screen,"#706500",[X+monster.camPos.x+random.randint(10,40)-25,Y+monster.camPos.y+random.randint(10,40)-25],random.randint(1,10))
            if(monster.id==4):
                pygame.draw.circle(screen,"#006C70",[X+monster.camPos.x+random.randint(-2,2),Y+monster.camPos.y+random.randint(-2,2)],20)
                pygame.draw.circle(screen,"#006C70",[X+monster.camPos.x+random.randint(10,40)-25,Y+monster.camPos.y+random.randint(10,40)-25],random.randint(1,10))
            if(monster.attacked):
                monster.attacked = False
                pygame.draw.circle(screen,"#FF0000",[X+monster.camPos.x+random.randint(-2,2),Y+monster.camPos.y+random.randint(-2,2)],20)
            font = pygame.font.SysFont('Comic Sans MS', 15)
            dice_text = font.render(f'{monster.dice}',True,"#ffffff")
            screen.blit(dice_text, (X+monster.camPos.x+random.randint(-1,1)-dice_text.get_size()[0]/2,Y+monster.camPos.y+random.randint(-1,1)-dice_text.get_size()[1]/2))

        if(monster.attributes.hp<1):
            if(monster.alive):
                if(monster.key):
                    game.map.key.y = monster.pos.y
                    game.map.key.x = monster.pos.x
                monster.pos.y = -1
                monster.pos.x = -1
                if(monster.id==0 or monster.id==2 or monster.id==4):
                    upMonster = random.randint(0,len(game.map.monsters)-1)
                    if(game.map.monsters[upMonster].id==1):
                        game.map.monsters[upMonster].attributes.hp*=2
                        game.map.monsters[upMonster].attributes.hpMax*=2
                        game.map.monsters[upMonster].attributes.defense*=2
                        game.map.monsters[upMonster].attributes.strength*=2
                        game.map.monsters[upMonster].attributes.intelligence*=2
                        game.map.monsters[upMonster].attributes.dexterity*=2
                if(monster.id==0 or monster.id==1 or monster.id==2 or monster.id==4):
                    upMonster = random.randint(0,len(game.map.monsters)-1)
                    if(game.map.monsters[upMonster].id==3):
                        game.map.monsters[upMonster].attributes.dexterity+=1
                game.map.player.exp+=random.randint(1,game.map.floor*game.map.player.attributes.intelligence)
                monster.alive = False
        if(monster.alive):
            if(monster.pos.y==game.map.key.y and monster.pos.x==game.map.key.x):
                game.map.key.y = -1
                game.map.key.x = -1
                monster.key = True
            if(time.perf_counter()-monster.clockSpeed>1/monster.attributes.dexterity):
                monster.clockSpeed = time.perf_counter()
                target = POS()
                target.y = 0
                target.x = 0
                forbiddenBlcoks = [0,3]
                direction = random.randint(0,3)
                if(game.map.player.attributes.hp>0):
                    if((monster.pos.y-game.map.player.pos.y>=0-monster.attributes.intelligence and monster.pos.y-game.map.player.pos.y<=monster.attributes.intelligence) and (monster.pos.x-game.map.player.pos.x>=0-monster.attributes.intelligence and monster.pos.x-game.map.player.pos.x<=monster.attributes.intelligence)):
                        if(random.random()<0.75):
                            if(monster.pos.y-game.map.player.pos.y==0):
                                if(monster.pos.x-game.map.player.pos.x>0):
                                    direction = 2
                                else:
                                    direction = 3
                            elif(monster.pos.x-game.map.player.pos.x==0):
                                if(monster.pos.y-game.map.player.pos.y>0):
                                    direction = 0
                                else:
                                    direction = 1
                            else:
                                if(random.random()<0.5):
                                    if(monster.pos.y-game.map.player.pos.y>0):
                                        direction = 0
                                        if(monster.id==2):
                                            direction = 1
                                    else:
                                        direction = 1
                                        if(monster.id==2):
                                            direction = 0
                                else:
                                    if(monster.pos.x-game.map.player.pos.x>0):
                                        direction = 2
                                        if(monster.id==2):
                                            direction = 3
                                    else:
                                        direction = 3
                                        if(monster.id==2):
                                            direction = 2
                    if(monster.id==2):
                        if(random.random()<0.9):
                            healMonster = random.randint(0,len(game.map.monsters)-1)
                            if(not monster==game.map.monsters[healMonster] and game.map.monsters[healMonster].alive):
                                if(game.map.monsters[healMonster].attributes.hp<game.map.monsters[healMonster].attributes.hpMax):
                                    game.map.monsters[healMonster].attributes.hp+=game.map.floor
                                    if(game.map.monsters[healMonster].attributes.hp>game.map.monsters[healMonster].attributes.hpMax):
                                        game.map.monsters[healMonster].attributes.hp = game.map.monsters[healMonster].attributes.hpMax
                                    pygame.draw.circle(screen,"#00FF15",[X+game.map.monsters[healMonster].camPos.x+random.randint(-1,1),Y+game.map.monsters[healMonster].camPos.y+random.randint(-1,1)],20)
                                    pygame.draw.line(screen,"#00FF15",[X+game.map.monsters[healMonster].camPos.x+random.randint(-2,2),Y+game.map.monsters[healMonster].camPos.y+random.randint(-2,2)],[X+monster.camPos.x+random.randint(-2,2),Y+monster.camPos.y+random.randint(-2,2)],30)
                                    direction = -1
                        else:
                            if(random.random()<0.1):
                                damage = random.randint(1,game.map.floor)
                                if(game.map.player.inventory[0][1].id==13):
                                    damage = 0
                                    if(game.map.player.inventory[0][1].goBreak):
                                        clear_slot(game,0,1)
                                    else:
                                        if(random.random()<game.map.player.inventory[0][1].breakChance/100):
                                            game.map.player.inventory[0][1].goBreak = True
                                        game.map.player.inventory[0][1].breakChance+=1
                                        
                                if(damage<game.map.player.attributes.hp):
                                    pygame.draw.circle(screen,"#8400FF",[game.map.player.camPos.x+random.randint(-1,1),game.map.player.camPos.y+random.randint(-1,1)],20)
                                    pygame.draw.line(screen,"#8400FF",[game.map.player.camPos.x+random.randint(-2,2),game.map.player.camPos.y+random.randint(-2,2)],[X+monster.camPos.x+random.randint(-2,2),Y+monster.camPos.y+random.randint(-2,2)],30)
                                    game.map.player.attributes.hp-=damage
                                    objectView = random.randint(0,49)
                                    game.map.damagesView[objectView].value = (0-damage)
                                    game.map.damagesView[objectView].id = 1
                                    game.map.damagesView[objectView].pos.y = random.randint(250,750)
                                    game.map.damagesView[objectView].pos.x = random.randint(250,750)
                                    game.map.damagesView[objectView].size = 50
                                    direction = -1
                                    game.map.player.dice = random.randint(1,100)
                                    if(game.map.player.inventory[0][2].id==10):
                                        if(game.map.player.inventory[0][2].goBreak):
                                            game.map.player.attributes.hp = game.map.player.attributes.hpMax
                                            clear_slot(game,0,2)
                                        else:
                                            if(random.random()<game.map.player.inventory[0][2].breakChance/100):
                                                game.map.player.inventory[0][2].goBreak = True
                                            game.map.player.inventory[0][2].breakChance+=1
                if(direction==0):
                    target.y-=1
                if(direction==1):
                    target.y+=1
                if(direction==2):
                    target.x-=1
                if(direction==3):
                    target.x+=1
                monster.pos.y+=target.y
                monster.pos.x+=target.x
                success = True
                if(monster.id==1):
                    if(random.random()<0.25):
                        if(random.random()<0.1):
                            attribute = random.randint(0,4)
                            if(attribute==0):
                                monster.attributes.hpMax = game.map.floor
                                monster.attributes.hp = game.map.floor
                            if(attribute==1):
                                monster.attributes.defense = game.map.floor
                            if(attribute==2):
                                monster.attributes.strength = game.map.floor
                            if(attribute==3):
                                monster.attributes.intelligence = 1
                            if(attribute==4):
                                monster.attributes.dexterity = 1
                        attribute = random.randint(0,4)
                        if(attribute==0):
                            monster.attributes.hpMax+=1
                            monster.attributes.hp+=1
                        if(attribute==1):
                            monster.attributes.defense+=1
                        if(attribute==2):
                            monster.attributes.strength+=1
                        if(attribute==3):
                            monster.attributes.intelligence+=1
                        if(attribute==4):
                            monster.attributes.dexterity+=0.1
                if(game.map.tiles[monster.pos.y][monster.pos.x] in forbiddenBlcoks):
                    if(game.map.tiles[monster.pos.y][monster.pos.x]==3):
                        if(random.random()<0.1):
                            game.map.tiles[monster.pos.y][monster.pos.x] = 1
                    success = False
                if(game.map.player.pos.y==monster.pos.y and game.map.player.pos.x==monster.pos.x):
                    success = False
                    if(game.map.player.attributes.hp>=1):
                        damage = random.randint(1,monster.attributes.strength)
                        if(random.random()<0.5):
                            damage+=monster.attributes.intelligence
                        defense = int(game.map.player.attributes.defense*(game.map.player.dice/100))

                        if(game.map.player.inventory[0][1].id==7):
                            defense+=random.randint(1,defense+1)
                            if(game.map.player.inventory[0][1].goBreak):
                                clear_slot(game,0,1)
                            else:
                                if(random.random()<game.map.player.inventory[0][1].breakChance/100):
                                    game.map.player.inventory[0][1].goBreak = True
                                game.map.player.inventory[0][1].breakChance+=1

                        if(game.map.player.inventory[0][2].id==10):
                            if(game.map.player.inventory[0][2].goBreak):
                                game.map.player.attributes.hp = game.map.player.attributes.hpMax
                                clear_slot(game,0,2)
                            else:
                                if(random.random()<game.map.player.inventory[0][2].breakChance/100):
                                    game.map.player.inventory[0][2].goBreak = True
                                game.map.player.inventory[0][2].breakChance+=1
                            

                        if(random.random()<0.5):
                            defense+=monster.attributes.intelligence

                        if(game.map.player.inventory[0][1].id==12):
                            damage = int(damage/2)
                            monster.attributes.hp-=damage
                            defense+=1
                            if(game.map.player.inventory[0][1].goBreak):
                                clear_slot(game,0,1)
                            else:
                                if(random.random()<game.map.player.inventory[0][1].breakChance/100):
                                    game.map.player.inventory[0][1].goBreak = True
                                game.map.player.inventory[0][1].breakChance+=1

                        if(game.map.player.inventory[0][2].id==8):
                            if(game.map.player.inventory[0][2].goBreak):
                                game.map.player.attributes.hpMax-=game.map.player.inventory[0][game.map.player.inventorySelection.x].hp
                                game.map.player.attributes.defense-=game.map.player.inventory[0][game.map.player.inventorySelection.x].defense
                                game.map.player.attributes.strength-=game.map.player.inventory[0][game.map.player.inventorySelection.x].strength
                                game.map.player.attributes.intelligence-=game.map.player.inventory[0][game.map.player.inventorySelection.x].intelligence
                                game.map.player.attributes.dexterity-=game.map.player.inventory[0][game.map.player.inventorySelection.x].dexterity
                                clear_slot(game,0,2)
                            else:
                                if(random.random()<game.map.player.inventory[0][2].breakChance/100):
                                    game.map.player.inventory[0][2].goBreak = True
                                if(random.random()<0.1):
                                    game.map.player.inventory[0][2].breakChance+=1

                        if(game.map.player.inventory[0][2].id==9):
                            if(game.map.player.inventory[0][2].goBreak):
                                clear_slot(game,0,2)
                            else:
                                if(random.random()<game.map.player.inventory[0][2].breakChance/100):
                                    game.map.player.inventory[0][2].goBreak = True
                                if(random.random()<0.1):
                                    game.map.player.inventory[0][2].breakChance+=1

                        if(defense>=damage):
                            defense = damage
                            if(random.random()<0.5):
                                defense = damage-1
                        else:
                            game.map.player.inventoryOpened = False
                        
                        pygame.draw.circle(screen,"#ff0000",[525+random.randint(-1,1),525+random.randint(-1,1)],20)
                        game.map.player.attributes.hp-=(damage-defense)
                        if(defense<damage):
                            game.map.player.dice = random.randint(1,100)
                        if(monster.id==4):
                            if(random.random()<0.75):
                                debuff = random.randint(0,2)
                                if(random.random()<0.25):
                                    debuff = random.randint(0,4)
                                if(debuff==0):
                                    game.map.player.attributes.hpMax-=1
                                if(debuff==1):
                                    game.map.player.attributes.defense-=1
                                if(debuff==2):
                                    game.map.player.attributes.strength-=1
                                if(debuff==3):
                                    game.map.player.attributes.intelligence-=1
                                if(debuff==4):
                                    game.map.player.attributes.dexterity-=0.1
                        objectView = random.randint(0,49)
                        game.map.damagesView[objectView].value = (0-(damage-defense))
                        game.map.damagesView[objectView].id = 1
                        game.map.damagesView[objectView].pos.y = random.randint(250,750)
                        game.map.damagesView[objectView].pos.x = random.randint(250,750)
                        game.map.damagesView[objectView].size = 50
                        monster.dice = random.randint(1,100)
                for otherMonster in game.map.monsters:
                    if(otherMonster==monster):
                        continue
                    else:
                        if(otherMonster.pos.y==monster.pos.y and otherMonster.pos.x==monster.pos.x):
                            success = False
                            break
                for item in game.map.items:
                    if(monster.pos.y==item.y and monster.pos.x==item.x):
                        item.y = -1
                        item.x = -1
                        success = False
                        break
                if(not success):
                    monster.pos.y-=target.y
                    monster.pos.x-=target.x
                    if(direction==0):
                        monster.camPos.y-=15
                    if(direction==1):
                        monster.camPos.y+=15
                    if(direction==2):
                        monster.camPos.x-=15
                    if(direction==3):
                        monster.camPos.x+=15
                else:
                    if(direction!=-1):
                        monster.dice = random.randint(1,100)
    game.map.player.keyInput = 0
#----------------------------------------------------------------------------------------------------------------------------------------
def render_dark(game = GAME()):
    for y in range(-10,10,1):
        for x in range(-10,10,1):
            Y = y*50+500
            X = x*50+500
            if(game.map.memory[game.map.player.pos.y+y][game.map.player.pos.x+x]==0):
                size = 45
                if(random.random()<0.1):
                    size = random.randint(40,50)
                pygame.draw.circle(screen,"#000000",[X+random.randint(20,30),Y+random.randint(20,30)],size)
                chance = ((game.map.player.attributes.hpMax-game.map.player.attributes.hp)/(game.map.player.attributes.hpMax))/100
                if(random.random()<chance):
                    pygame.draw.circle(screen,"#161616",[X+random.randint(10,40),Y+random.randint(10,40)],random.randint(1,10))
                    j = random.randint(-25,25)
                    i = random.randint(-25,25)
                    for j1 in range(-1,2):
                        for i1 in range(-1,2):
                            if(j1==0 or i1==0):
                                if(game.map.memory[game.map.player.pos.y+j+j1][game.map.player.pos.x+i+i1]==0):
                                    game.map.memory[game.map.player.pos.y+j][game.map.player.pos.x+i] = 0
                
#----------------------------------------------------------------------------------------------------------------------------------------
def render_interface(game = GAME()):
    for damageObject in game.map.damagesView:
        if(damageObject.size>0):
            font = pygame.font.SysFont('Comic Sans MS', damageObject.size)
            damage_text = font.render(f"{damageObject.value}", True, "#e2e2e2")
            if(damageObject.id==1):
                damage_text = font.render(f"{damageObject.value}", True, "#ff0000")
            screen.blit(damage_text, (damageObject.pos.x+random.randint(-1,1),damageObject.pos.y+random.randint(-1,1)))
            if(random.random()<0.25):
                damageObject.size-=1
                damageObject.pos.y+=random.randint(-1,1)
                damageObject.pos.x+=random.randint(-1,1)

    font = pygame.font.SysFont('Comic Sans MS', 20)

    if(game.map.player.attributes.hp>=1):
        floor_text = font.render(f'Floor {game.map.floor}',True,"#ffffff")
        screen.blit(floor_text, (900,950))

        dice_text = font.render(f'{game.map.player.dice}',True,"#000000")
        screen.blit(dice_text, (game.map.player.camPos.x+random.randint(-1,1)-dice_text.get_size()[0]/2,game.map.player.camPos.y+random.randint(-1,1)-dice_text.get_size()[1]/2))

        hpBar = (game.map.player.attributes.hp/game.map.player.attributes.hpMax)*200
        pygame.draw.rect(screen,"#364935",(790,10,200,20))
        pygame.draw.rect(screen,"#08fe00",(790,10,hpBar,20))

        expBar = (game.map.player.exp/game.map.player.nextExp)*200
        pygame.draw.rect(screen,"#464935",(790,35,200,20))
        pygame.draw.rect(screen,"#e0fe00",(790,35,expBar,20))
        if(game.map.player.key):
            X = 950
            Y = 55
            pygame.draw.lines(screen,"#fbff00",False,[[X+25,Y+20],[X+20,Y+25],[X+25,Y+30],[X+30,Y+25],[X+25,Y+20]],4)
            pygame.draw.lines(screen,"#fbff00",False,[[X+25,Y+20],[X+25,Y+10]],3)

        if(game.map.player.attributes.hp>game.map.player.attributes.hpMax):
            game.map.player.attributes.hp = game.map.player.attributes.hpMax
        hpValue_text = font.render(f'{game.map.player.attributes.hp} / {game.map.player.attributes.hpMax}',True,"#000000")
        if(game.map.player.exp>game.map.player.nextExp):
            game.map.player.exp = game.map.player.nextExp
        expValue_text = font.render(f'{game.map.player.exp} / {game.map.player.nextExp}',True,"#000000")
        screen.blit(hpValue_text, (890-hpValue_text.get_size()[0]/2,19-hpValue_text.get_size()[1]/2))
        screen.blit(expValue_text, (890-expValue_text.get_size()[0]/2,44-expValue_text.get_size()[1]/2))
        if(game.map.player.inventoryOpened):
            render_inventory(game)
        else:
            y = 20
            x = 20
            for i in range(3):
                if(game.map.player.inventory[0][i].id==6):
                    pygame.draw.rect(screen, "#D8D8D8", (x+22, y+5, 6, 25)) # Lâmina
                    pygame.draw.rect(screen, "#D8D8D8", (x+23, y+3, 4, 2)) # Ponta
                    pygame.draw.rect(screen, "#D8D8D8", (x+24, y+1, 2, 2)) # Ponta
                    pygame.draw.rect(screen, "#C9A227", (x+15, y+30, 20, 4)) # Guarda
                    pygame.draw.rect(screen, "#8B5A2B", (x+22, y+34, 6, 10)) # Cabo
                    pygame.draw.rect(screen, "#C9A227", (x+21, y+44, 8, 3)) # Pomo
                if(game.map.player.inventory[0][i].id==7):
                    pygame.draw.circle(screen, "#707070", (x+25, y+25), 18)
                    pygame.draw.circle(screen, "#C8C8C8", (x+25, y+25), 15)
                    pygame.draw.rect(screen, "#E8E8E8", (x+23, y+12, 4, 26))
                    pygame.draw.rect(screen, "#E8E8E8", (x+12, y+23, 26, 4))
                    pygame.draw.circle(screen, "#AAAAAA", (x+25, y+25), 4)
                if(game.map.player.inventory[0][i].id==8):
                    pygame.draw.circle(screen, "#FFD700", (x+25, y+25), 12)
                    pygame.draw.circle(screen, "#000000", (x+25, y+25), 8)
                    pygame.draw.circle(screen, "#FF4040", (x+25, y+11), 4)
                    pygame.draw.circle(screen, "#FFFFFF", (x+24, y+10), 1)
                if(game.map.player.inventory[0][i].id==9):
                    pygame.draw.rect(screen, "#FFD700", (x+22, y+8, 6, 28)) # Haste vertical
                    pygame.draw.rect(screen, "#FFD700", (x+12, y+16, 26, 6)) # Braços
                    pygame.draw.rect(screen, "#FFD700", (x+18, y+36, 14, 5)) # Base
                    pygame.draw.rect(screen, "#FFFFFF", (x+20, y+15, 10, 6)) # Joia central
                    pygame.draw.rect(screen, "#FFF3A0", (x+20, y+5, 10, 3)) # Topo
                if(game.map.player.inventory[0][i].id==10):
                    pygame.draw.rect(screen, "#43FF52", (x+22, y+8, 6, 28)) # Haste vertical
                    pygame.draw.rect(screen, "#43FF52", (x+12, y+16, 26, 6)) # Braços
                    pygame.draw.rect(screen, "#43FF52", (x+18, y+36, 14, 5)) # Base
                    pygame.draw.rect(screen, "#FFFFFF", (x+20, y+15, 10, 6)) # Joia central
                    pygame.draw.rect(screen, "#BEFFA0", (x+20, y+5, 10, 3)) # Topo
                if(game.map.player.inventory[0][i].id==11):
                    pygame.draw.line(screen, "#8B5A2B", (x+18, y+42), (x+30, y+12), 5)
                    pygame.draw.circle(screen, "#66CCFF", (x+32, y+10), 7)
                    pygame.draw.circle(screen, "#AADDFF", (x+30, y+8), 2)
                if(game.map.player.inventory[0][i].id==12):
                    pygame.draw.polygon(screen, "#707070", [(x+25, y+5),(x+38, y+12),(x+40, y+25),(x+35, y+36),(x+25, y+45),(x+15, y+36),(x+10, y+25),(x+12, y+12)])
                    pygame.draw.polygon(screen, "#C8C8C8", [(x+25, y+9),(x+35, y+15),(x+36, y+24),(x+32, y+33),(x+25, y+40),(x+18, y+33),(x+14, y+24),(x+15, y+15)])
                    pygame.draw.rect(screen, "#E8E8E8", (x+23, y+12, 4, 24))
                    pygame.draw.rect(screen, "#E8E8E8", (x+17, y+20, 16, 4))
                if(game.map.player.inventory[0][i].id==13): # ESCUDO ANTI-MALDIÇÃO
                    pygame.draw.polygon(screen, "#707070", [(x+25, y+5),(x+39, y+15),(x+36, y+32),(x+25, y+45),(x+14, y+32),(x+11, y+15)])
                    pygame.draw.polygon(screen, "#D0D0D0", [(x+25, y+9),(x+35, y+16),(x+33, y+30),(x+25, y+39),(x+17, y+30),(x+15, y+16)])
                    pygame.draw.line(screen, "#FFFFFF", (x+18, y+12), (x+25, y+38), 2)
                if(game.map.player.inventory[0][i].id!=0):
                    breakChance_text = font.render(f'{game.map.player.inventory[0][i].breakChance}%',True,"#FFFFFF")
                    if(game.map.player.inventory[0][i].goBreak):
                        breakChance_text = font.render(f'{game.map.player.inventory[0][i].breakChance}%',True,"#FF0000")
                    screen.blit(breakChance_text, (x+25-breakChance_text.get_size()[0]/2+random.randint(-1,1), y+60-breakChance_text.get_size()[1]/2+random.randint(-1,1)))
                if(game.map.player.inventory[0][i].cursed and game.map.player.inventory[0][i].reveled):
                    pygame.draw.circle(screen,"#FF0000",[x+random.randint(10,40),y+random.randint(10,40)],random.randint(1,10))
                x+=60
    else:
        floor_text = font.render(f'{game.map.floor}',True,"#000000")
        screen.blit(floor_text, (game.map.player.camPos.x+random.randint(-1,1)-floor_text.get_size()[0]/2,game.map.player.camPos.y+random.randint(-1,1)-floor_text.get_size()[1]/2))
        font = pygame.font.SysFont('Comic Sans MS', 50)
        continue_text = font.render("'ESC' to continue", True, "#FF0000")
        screen.blit(continue_text, (500-continue_text.get_size()[0]/2+random.randint(-1,1),850-continue_text.get_size()[1]/2+random.randint(-1,1)))
#----------------------------------------------------------------------------------------------------------------------------------------
def move_player(game = GAME()):

    if(game.map.player.attributes.hpMax<1):
        game.map.player.attributes.hpMax = 1
    if(game.map.player.attributes.defense<1):
        game.map.player.attributes.defense = 1
    if(game.map.player.attributes.strength<1):
        game.map.player.attributes.strength = 1
    if(game.map.player.attributes.intelligence<1):
        game.map.player.attributes.intelligence = 1
    if(game.map.player.attributes.dexterity<1):
        game.map.player.attributes.dexterity = 1

    speed = int(game.map.player.attributes.dexterity)
    if(speed>50):
        speed = 50
    if(speed<5):
        speed = 5
    if(game.map.player.camPos.y>525):
        game.map.player.camPos.y-=random.randint(2,speed)
    if(game.map.player.camPos.y<525):
        game.map.player.camPos.y+=random.randint(2,speed)
    if(game.map.player.camPos.x>525):
        game.map.player.camPos.x-=random.randint(2,speed)
    if(game.map.player.camPos.x<525):
        game.map.player.camPos.x+=random.randint(2,speed)

    if(game.map.player.attributes.hp<1):
        game.map.player.attributes.hp = 0
        if(game.map.player.inventory[0][2].id==9):
            if(random.random()<0.005):
                while(True):
                    y = random.randint(0,999)
                    x = random.randint(0,999)
                    if(game.map.tiles[y][x]==1):
                        game.map.player.pos.y = y
                        game.map.player.pos.x = x
                        break
                game.map.player.attributes.hp = 1
                for y in range(4):
                    for x in range(3):
                        if(random.random()<0.5):
                            clear_slot(game,y,x)
                game.map.player.keyInput = 5
                return
        else:
            if(keyboard.is_pressed('esc')):
                game.play = False
            game.map.player.attributes.intelligence = 1
    else:
        timeWait = 1/game.map.player.attributes.dexterity
        if(game.map.player.inventoryOpened):
            timeWait = 0.25
        if(time.perf_counter()-game.map.player.clockSpeed>timeWait):
            clock = False
            target = POS()
            target.y = 0
            target.x = 0
            forbiddenBlcoks = [0,3]
            if(game.map.player.exp>=game.map.player.nextExp):
                game.map.player.attPoints+=1
                game.map.player.level+=1
                game.map.player.exp = 0
                if(game.map.player.attributes.hp>=game.map.player.attributes.hpMax):
                    game.map.player.exp+=game.map.floor
                else:
                    game.map.player.attributes.hp+=game.map.floor
                game.map.player.nextExp+=random.randint(1,game.map.floor*2)
            if(keyboard.is_pressed('w')):
                clock = True
                if(not game.map.player.inventoryOpened):
                    game.map.player.keyInput = 1
                    target.y-=1
                else:
                    game.map.player.inventorySelection.y-=1
            if(keyboard.is_pressed('s')):
                clock = True
                if(not game.map.player.inventoryOpened):
                    game.map.player.keyInput = 2
                    target.y+=1
                else:
                    game.map.player.inventorySelection.y+=1
            if(keyboard.is_pressed('a')):
                clock = True
                if(not game.map.player.inventoryOpened):
                    game.map.player.keyInput = 3
                    target.x-=1
                else:
                    game.map.player.inventorySelection.x-=1
            if(keyboard.is_pressed('d')):
                clock = True
                if(not game.map.player.inventoryOpened):
                    game.map.player.keyInput = 4
                    target.x+=1
                else:
                    game.map.player.inventorySelection.x+=1
            if(keyboard.is_pressed('q')):
                clock = True
                if(game.map.player.inventoryOpened):
                    if(game.map.player.inventorySelection.y!=0):
                        if(game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].id!=0):
                            clear_slot(game,game.map.player.inventorySelection.y,game.map.player.inventorySelection.x)
                            game.map.player.exp+=random.randint(1,game.map.floor*game.map.player.attributes.intelligence)
            if(keyboard.is_pressed('enter')):
                clock = True
                if(not game.map.player.inventoryOpened):
                    if(game.map.player.key):
                        if(game.map.tiles[game.map.player.pos.y][game.map.player.pos.x]==2):
                            game.next = True
                else:
                    if(game.map.player.inventoryOpened):
                        if(game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].id==1):
                            game.map.player.attributes.hp+=game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].heal
                            clear_slot(game,game.map.player.inventorySelection.y,game.map.player.inventorySelection.x)
                        if(game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].id==2):
                            while(True):
                                y = random.randint(0,999)
                                x = random.randint(0,999)
                                if(game.map.tiles[y][x]==1):
                                    game.map.player.pos.y = y
                                    game.map.player.pos.x = x
                                    break
                            game.map.player.keyInput = 5
                            clear_slot(game,game.map.player.inventorySelection.y,game.map.player.inventorySelection.x)
                        if(game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].id==3):
                            buff = random.randint(0,4)
                            debuff = random.randint(0,4)
                            while(buff==debuff):
                                buff = random.randint(0,4)
                                debuff = random.randint(0,4)
                            if(buff==0):
                                hp = random.randint(1,10)
                                game.map.player.attributes.hpMax+=hp
                                game.map.player.attributes.hp+=hp
                            if(debuff==0):
                                game.map.player.attributes.hpMax-=random.randint(1,10)
                            if(buff==1):
                                game.map.player.attributes.defense+=random.randint(1,10)
                            if(debuff==1):
                                game.map.player.attributes.defense-=random.randint(1,10)
                            if(buff==2):
                                game.map.player.attributes.strength+=random.randint(1,10)
                            if(debuff==2):
                                game.map.player.attributes.strength-=random.randint(1,10)
                            if(buff==3):
                                game.map.player.attributes.intelligence+=1
                            if(debuff==3):
                                game.map.player.attributes.intelligence-=1
                            if(buff==4):
                                game.map.player.attributes.dexterity+=0.1
                            if(debuff==4):
                                game.map.player.attributes.dexterity-=0.1
                            clear_slot(game,game.map.player.inventorySelection.y,game.map.player.inventorySelection.x)
                        if(game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].id==4):
                            if(game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].cursed):
                                for y in range(-50,50):
                                    for x in range(-50,50):
                                        game.map.memory[game.map.player.pos.y+y][game.map.player.pos.x+x] = 0
                            else:
                                for y in range(-50,50):
                                    for x in range(-50,50):
                                        if(game.map.tiles[game.map.player.pos.y+y][game.map.player.pos.x+x]!=0):
                                            for j in range(-1,2):
                                                for i in range(-1,2):
                                                    game.map.memory[game.map.player.pos.y+y+j][game.map.player.pos.x+x+i] = 1
                            clear_slot(game,game.map.player.inventorySelection.y,game.map.player.inventorySelection.x)
                        if(game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].id==5):
                            game.map.player.exp = game.map.player.nextExp
                            clear_slot(game,game.map.player.inventorySelection.y,game.map.player.inventorySelection.x)
                        x = game.map.player.inventorySelection.x
                        equip = False
                        if(game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].id in [6,11]):
                            x = 0
                            equip = True
                        if(game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].id in [7,12,13]):
                            x = 1
                            equip = True
                        if(game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].id in [8,9,10]):
                            x = 2
                            equip = True
                        if(equip):
                            if(game.map.player.inventory[0][x].id==0):
                                game.map.player.inventory[0][x].id = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].id
                                game.map.player.inventory[0][x].defense = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].defense
                                game.map.player.inventory[0][x].dexterity = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].dexterity
                                game.map.player.inventory[0][x].heal = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].heal
                                game.map.player.inventory[0][x].hp = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].hp
                                game.map.player.inventory[0][x].intelligence = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].intelligence
                                game.map.player.inventory[0][x].strength = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].strength
                                game.map.player.inventory[0][x].cursed = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].cursed
                                game.map.player.inventory[0][x].reveled = True
                                game.map.player.inventory[0][x].breakChance = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].breakChance
                                game.map.player.inventory[0][x].goBreak = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].goBreak
                                game.map.player.attributes.hpMax+=game.map.player.inventory[0][x].hp
                                game.map.player.attributes.defense+=game.map.player.inventory[0][x].defense
                                game.map.player.attributes.strength+=game.map.player.inventory[0][x].strength
                                game.map.player.attributes.intelligence+=game.map.player.inventory[0][x].intelligence
                                game.map.player.attributes.dexterity+=game.map.player.inventory[0][x].dexterity
                                clear_slot(game,game.map.player.inventorySelection.y,game.map.player.inventorySelection.x)
                        if(game.map.player.inventorySelection.y==0):
                            if(not game.map.player.inventory[0][game.map.player.inventorySelection.x].cursed):
                                success = False
                                for y in range(1,4):
                                    for x in range(3):
                                        if(not success):
                                            if(game.map.player.inventory[y][x].id==0):
                                                game.map.player.attributes.hpMax-=game.map.player.inventory[0][game.map.player.inventorySelection.x].hp
                                                game.map.player.attributes.defense-=game.map.player.inventory[0][game.map.player.inventorySelection.x].defense
                                                game.map.player.attributes.strength-=game.map.player.inventory[0][game.map.player.inventorySelection.x].strength
                                                game.map.player.attributes.intelligence-=game.map.player.inventory[0][game.map.player.inventorySelection.x].intelligence
                                                game.map.player.attributes.dexterity-=game.map.player.inventory[0][game.map.player.inventorySelection.x].dexterity
                                                game.map.player.inventory[y][x].id = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].id
                                                game.map.player.inventory[y][x].defense = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].defense
                                                game.map.player.inventory[y][x].dexterity = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].dexterity
                                                game.map.player.inventory[y][x].heal = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].heal
                                                game.map.player.inventory[y][x].hp = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].hp
                                                game.map.player.inventory[y][x].intelligence = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].intelligence
                                                game.map.player.inventory[y][x].strength = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].strength
                                                game.map.player.inventory[y][x].cursed = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].cursed
                                                game.map.player.inventory[y][x].reveled = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].reveled
                                                game.map.player.inventory[y][x].breakChance = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].breakChance
                                                game.map.player.inventory[y][x].goBreak = game.map.player.inventory[game.map.player.inventorySelection.y][game.map.player.inventorySelection.x].goBreak
                                                success = True
                                clear_slot(game,0,game.map.player.inventorySelection.x)
            if(keyboard.is_pressed('i')):
                clock = True
                if(game.map.player.inventoryOpened==False):
                    game.map.player.inventoryOpened = True
                else:
                    game.map.player.inventoryOpened = False
            if(clock):
                game.map.player.clockSpeed = time.perf_counter()
            if((target.y!=0 and target.x==0) or (target.y==0 and target.x!=0)):
                game.map.player.pos.y+=target.y
                game.map.player.pos.x+=target.x
                success = True
                if(game.map.tiles[game.map.player.pos.y][game.map.player.pos.x] in forbiddenBlcoks):
                    if(game.map.tiles[game.map.player.pos.y][game.map.player.pos.x]==3):
                        if(random.random()<0.1):
                            game.map.tiles[game.map.player.pos.y][game.map.player.pos.x] = 1
                        objectView = random.randint(0,49)
                        game.map.damagesView[objectView].value = "..."
                        game.map.damagesView[objectView].id = 0
                        game.map.damagesView[objectView].pos.y = random.randint(250,750)
                        game.map.damagesView[objectView].pos.x = random.randint(250,750)
                        game.map.damagesView[objectView].size = 50
                    success = False
                for monster in game.map.monsters:
                    if(game.map.player.pos.y == monster.pos.y and game.map.player.pos.x == monster.pos.x):
                        success = False
                        damage = int(game.map.player.attributes.strength*(game.map.player.dice/100))

                        if(game.map.player.inventory[0][0].id==6):
                            damage+=random.randint(0,damage)
                            if(game.map.player.inventory[0][0].goBreak):
                                clear_slot(game,0,0)
                            else:
                                if(random.random()<game.map.player.inventory[0][0].breakChance/100):
                                    game.map.player.inventory[0][0].goBreak = True
                                if(random.random()<0.5):
                                    game.map.player.inventory[0][0].breakChance+=1
                                
                        if(game.map.player.inventory[0][0].id==11):
                            damage+=game.map.player.attributes.intelligence
                            if(game.map.player.inventory[0][0].goBreak):
                                clear_slot(game,0,0)
                            else:
                                if(random.random()<game.map.player.inventory[0][0].breakChance/100):
                                    game.map.player.inventory[0][0].goBreak = True
                                game.map.player.inventory[0][0].breakChance+=1

                        if(random.random()<0.5):
                            damage+=game.map.player.attributes.intelligence
                        defense = int(monster.attributes.defense*(monster.dice/100))
                        if(random.random()<0.5):
                            defense+=game.map.player.attributes.intelligence
                        if(defense>damage):
                            defense = damage
                            if(random.random()<0.5):
                                defense = damage-1
                        monster.attributes.hp-=(damage-defense)
                        if(defense<damage):
                            monster.dice = random.randint(1,100)
                        monster.attacked = True
                        objectView = random.randint(0,49)

                        game.map.damagesView[objectView].value = (damage-defense)
                        game.map.damagesView[objectView].id = 0
                        game.map.damagesView[objectView].pos.y = random.randint(250,750)
                        game.map.damagesView[objectView].pos.x = random.randint(250,750)
                        game.map.damagesView[objectView].size = 50
                        game.map.player.dice = random.randint(1,100)
                for item in game.map.items:
                    if(game.map.player.pos.y==item.y and game.map.player.pos.x==item.x):
                        successInv = False
                        for y in range(1,4):
                            for x in range(3):
                                if(not successInv):
                                    if(game.map.player.inventory[y][x].id==0):
                                        clear_slot(game,y,x)
                                        if(game.map.floor>=10):
                                            game.map.player.inventory[y][x].breakChance = random.randint(1,100)
                                        if(random.random()<0.05):
                                            game.map.player.inventory[y][x].cursed = True
                                        game.map.player.inventory[y][x].id = random.randint(1,13)
                                        if(random.random()<0.5):
                                            game.map.player.inventory[y][x].id = random.randint(1,5)
                                        if(game.map.player.inventory[y][x].id==1):
                                            game.map.player.inventory[y][x].heal = 1+game.map.floor+random.randint(0-game.map.floor,game.map.floor)
                                        if(game.map.player.inventory[y][x].id==8):
                                            attribute = random.randint(0,2)
                                            if(attribute==0):
                                                game.map.player.inventory[y][x].hp = random.randint(1,game.map.floor+1)
                                            if(attribute==1):
                                                game.map.player.inventory[y][x].strength = random.randint(1,game.map.floor+1)
                                            if(attribute==2):
                                                game.map.player.inventory[y][x].defense = random.randint(1,game.map.floor+1)
                                        successInv = True
                                        item.y = -1
                                        item.x = -1
                        if(successInv):
                            success = False
                            break
                if(success):
                    if(game.map.player.keyInput==1):
                        game.map.player.camPos.y+=50
                    if(game.map.player.keyInput==2):
                        game.map.player.camPos.y-=50
                    if(game.map.player.keyInput==3):
                        game.map.player.camPos.x+=50
                    if(game.map.player.keyInput==4):
                        game.map.player.camPos.x-=50
                    game.map.player.dice = random.randint(1,100)
                else:
                    game.map.player.pos.y-=target.y
                    game.map.player.pos.x-=target.x
                    if(game.map.player.keyInput==1):
                        game.map.player.camPos.y-=15
                    if(game.map.player.keyInput==2):
                        game.map.player.camPos.y+=15
                    if(game.map.player.keyInput==3):
                        game.map.player.camPos.x-=15
                    if(game.map.player.keyInput==4):
                        game.map.player.camPos.x+=15
                    game.map.player.keyInput = 0
            if(game.map.tiles[game.map.player.pos.y][game.map.player.pos.x]==4):
                game.map.player.attributes.hp-=random.randint(1,game.map.floor)
                game.map.tiles[game.map.player.pos.y][game.map.player.pos.x] = 1
            if(game.map.player.pos.y == game.map.key.y and game.map.player.pos.x == game.map.key.x):
                game.map.player.key = True
                game.map.key.y = -1
                game.map.key.x = -1
#----------------------------------------------------------------------------------------------------------------------------------------
def simulate_vision(game = GAME(),y=0,x=0,i=0):
    if(i>=1):
        if(random.random()<0.5):
            if(y<0):
                y-=1
            else:
                y+=1
        if(random.random()<0.5):
            if(x<0):
                x-=1
            else:
                x+=1
    if(game.map.tiles[game.map.player.pos.y+y][game.map.player.pos.x+x]!=0 and game.map.tiles[game.map.player.pos.y+y][game.map.player.pos.x+x]!=3):
        i+=1
        game.map.memory[game.map.player.pos.y+y][game.map.player.pos.x+x] = 1
        if(i<game.map.player.attributes.intelligence):
            simulate_vision(game,y,x,i)
    game.map.memory[game.map.player.pos.y+y][game.map.player.pos.x+x] = 1
    return 0
#----------------------------------------------------------------------------------------------------------------------------------------
def render_game(game = GAME()):
    if(game.map.player.attributes.hp<0):
        game.map.player.attributes.hp = 0
    y = random.randint(-50,50)
    x = random.randint(-50,50)
    for y in range(-1,2,1):
        for x in range(-1,2,1):
            simulate_vision(game,y,x)
    for y in range(-10,10,1):
        for x in range(-10,10,1):
            Y = y*50+500
            X = x*50+500
            if(game.map.tiles[game.map.player.pos.y+y][game.map.player.pos.x+x]==0):
                pygame.draw.rect(screen,"#545454",(X,Y,50,50))
            if(game.map.tiles[game.map.player.pos.y+y][game.map.player.pos.x+x]==1):
                pygame.draw.rect(screen,"#a2a2a2",(X,Y,50,50))
            if(game.map.tiles[game.map.player.pos.y+y][game.map.player.pos.x+x]==2):
                if(game.map.player.key):
                    pygame.draw.rect(screen,"#ffffff",(X,Y,50,50))
                pygame.draw.rect(screen,"#363636",(X+5+random.randint(-1,1),Y+5+random.randint(-1,1),40,40))
            if(game.map.tiles[game.map.player.pos.y+y][game.map.player.pos.x+x]==3):
                pygame.draw.rect(screen,"#545454",(X,Y,50,50))
            if(game.map.tiles[game.map.player.pos.y+y][game.map.player.pos.x+x]==4):
                pygame.draw.rect(screen,"#a2a2a2",(X,Y,50,50))
                pygame.draw.circle(screen,"#999999",[X+12.5,Y+12.5],12)
                pygame.draw.circle(screen,"#999999",[X+37.5,Y+12.5],12)
                pygame.draw.circle(screen,"#999999",[X+37.5,Y+37.5],12)
                pygame.draw.circle(screen,"#999999",[X+12.5,Y+37.5],12)
            if(game.map.key.y==game.map.player.pos.y+y and game.map.key.x==game.map.player.pos.x+x):
                pygame.draw.lines(screen,"#fbff00",False,[[X+25,Y+20],[X+20,Y+25],[X+25,Y+30],[X+30,Y+25],[X+25,Y+20]],4)
                pygame.draw.lines(screen,"#fbff00",False,[[X+25,Y+20],[X+25,Y+10]],3)
            for item in game.map.items:
                if(item.y==game.map.player.pos.y+y and item.x==game.map.player.pos.x+x):
                    pygame.draw.rect(screen, "#A66A2C", (X+8, Y+10, 34, 10))
                    pygame.draw.rect(screen, "#8B4513", (X+8, Y+20, 34, 18))
                    pygame.draw.rect(screen, "#808080", (X+14, Y+10, 4, 28))
                    pygame.draw.rect(screen, "#808080", (X+32, Y+10, 4, 28))
                    pygame.draw.rect(screen, "#FFD700", (X+22, Y+22, 6, 8))
                    pygame.draw.rect(screen, "#5A2E0C", (X+10, Y+38, 6, 4))
                    pygame.draw.rect(screen, "#5A2E0C", (X+34, Y+38, 6, 4))

    if(game.map.player.attributes.hp<1):
        pygame.draw.lines(screen,"#5e5e5e",False,[[game.map.player.camPos.x-20,game.map.player.camPos.y+15],[game.map.player.camPos.x+20,game.map.player.camPos.y+15]],10)
        pygame.draw.rect(screen,"#5e5e5e",(game.map.player.camPos.x-15,game.map.player.camPos.y-20,30,35))
    else:
        pygame.draw.circle(screen,"#ffffff",[game.map.player.camPos.x+random.randint(-1,1),game.map.player.camPos.y+random.randint(-1,1)],20)
#----------------------------------------------------------------------------------------------------------------------------------------
def put_attributes(game = GAME()):
    global running
    game.map.player.clockSpeed = time.perf_counter()
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        screen.fill("black")
        for y in range(-10,10,1):
            for x in range(-10,10,1):
                Y = y*50+500
                X = x*50+500
                if(random.random()<0.1):
                    pygame.draw.circle(screen,"#161616",[X+random.randint(10,40),Y+random.randint(10,40)],random.randint(1,10))
        font = pygame.font.SysFont('Comic Sans MS', 50)
        points_text = font.render(f'ATTRIBUTES POINTS: {game.map.player.attPoints}', True, (0, 255, 0))
        if(game.map.player.attPoints<=0):
            points_text = font.render(f'ATTRIBUTES POINTS: {game.map.player.attPoints}', True, (255, 0, 0))
        screen.blit(points_text, (500-points_text.get_size()[0]/2+random.randint(-1,1),100-points_text.get_size()[1]/2+random.randint(-1,1)))
        if(game.attSelection==0):
            hp_text = font.render(f'> HP: {game.map.player.attributes.hp} / {game.map.player.attributes.hpMax}', True, (255, 245, 150))
            screen.blit(hp_text, (500-hp_text.get_size()[0]/2+random.randint(-1,1),250-hp_text.get_size()[1]/2+random.randint(-1,1)))
        else:
            hp_text = font.render(f'HP: {game.map.player.attributes.hp} / {game.map.player.attributes.hpMax}', True, (255, 255, 255))
            screen.blit(hp_text, (500-hp_text.get_size()[0]/2,250-hp_text.get_size()[1]/2))
        if(game.attSelection==1):
            defense_text = font.render(f'> DEFENSE: {game.map.player.attributes.defense}', True, (255, 245, 150))
            screen.blit(defense_text, (500-defense_text.get_size()[0]/2+random.randint(-1,1),350-defense_text.get_size()[1]/2+random.randint(-1,1)))
        else:
            defense_text = font.render(f'DEFENSE: {game.map.player.attributes.defense}', True, (255, 255, 255))
            screen.blit(defense_text, (500-defense_text.get_size()[0]/2,350-defense_text.get_size()[1]/2))
        if(game.attSelection==2):
            strength_text = font.render(f'> STRENGTH: {game.map.player.attributes.strength}', True, (255, 245, 150))
            screen.blit(strength_text, (500-strength_text.get_size()[0]/2+random.randint(-1,1),450-strength_text.get_size()[1]/2+random.randint(-1,1)))
        else:
            strength_text = font.render(f'STRENGTH: {game.map.player.attributes.strength}', True, (255, 255, 255))
            screen.blit(strength_text, (500-strength_text.get_size()[0]/2,450-strength_text.get_size()[1]/2))
        if(game.attSelection==3):
            intelligence_text = font.render(f'> INTELLIGENCE: {game.map.player.attributes.intelligence}', True, (255, 245, 150))
            screen.blit(intelligence_text, (500-intelligence_text.get_size()[0]/2+random.randint(-1,1),550-intelligence_text.get_size()[1]/2+random.randint(-1,1)))
        else:
            intelligence_text = font.render(f'INTELLIGENCE: {game.map.player.attributes.intelligence}', True, (255, 255, 255))
            screen.blit(intelligence_text, (500-intelligence_text.get_size()[0]/2,550-intelligence_text.get_size()[1]/2))
        if(game.attSelection==4):
            dexterity_text = font.render(f'> DEXTERITY: {game.map.player.attributes.dexterity:.1f}', True, (255, 245, 150))
            screen.blit(dexterity_text, (500-dexterity_text.get_size()[0]/2+random.randint(-1,1),650-dexterity_text.get_size()[1]/2+random.randint(-1,1)))
        else:
            dexterity_text = font.render(f'DEXTERITY: {game.map.player.attributes.dexterity:.1f}', True, (255, 255, 255))
            screen.blit(dexterity_text, (500-dexterity_text.get_size()[0]/2,650-dexterity_text.get_size()[1]/2))
        if(game.attSelection==5):
            continue_text = font.render(f'> CONTINUE', True, (255, 245, 150))
            screen.blit(continue_text, (500-continue_text.get_size()[0]/2+random.randint(-1,1),900-continue_text.get_size()[1]/2+random.randint(-1,1)))
        else:
            continue_text = font.render(f'CONTINUE', True, (255, 255, 255))
            screen.blit(continue_text, (500-continue_text.get_size()[0]/2,900-continue_text.get_size()[1]/2))
        if(time.perf_counter()-game.map.player.clockSpeed>0.2):
            if(keyboard.is_pressed('w')):
                game.map.player.clockSpeed = time.perf_counter()
                if(game.attSelection>0):
                    game.attSelection-=1
            if(keyboard.is_pressed('s')):
                game.map.player.clockSpeed = time.perf_counter()
                if(game.attSelection<5):
                    game.attSelection+=1
            if(keyboard.is_pressed('enter')):
                game.map.player.clockSpeed = time.perf_counter()
                if(game.map.player.attPoints>0):
                    if(game.attSelection==0):
                        game.map.player.attPoints-=1
                        hp = random.randint(1,10)
                        game.map.player.attributes.hp+=hp
                        if(game.map.player.attributes.hp>game.map.player.attributes.hpMax):
                            game.map.player.attributes.hpMax = game.map.player.attributes.hp
                    if(game.attSelection==1):
                        game.map.player.attPoints-=1
                        game.map.player.attributes.defense+=random.randint(1,10)
                    if(game.attSelection==2):
                        game.map.player.attPoints-=1
                        game.map.player.attributes.strength+=random.randint(1,10)
                    if(game.attSelection==3):
                        if(game.map.player.attPoints>=game.map.player.attributes.intelligence):
                            game.map.player.attPoints-=(game.map.player.attributes.intelligence)
                            game.map.player.attributes.intelligence+=1
                    if(game.attSelection==4):
                        if(game.map.player.attPoints>=int(game.map.player.attributes.dexterity)):
                            game.map.player.attPoints-=int(game.map.player.attributes.dexterity)
                            game.map.player.attributes.dexterity+=0.1
                if(game.attSelection==5):
                    break
        pygame.display.flip()
        clock.tick(60)
#----------------------------------------------------------------------------------------------------------------------------------------
def create_map(game = GAME()):
    screen.fill("black")
    font = pygame.font.SysFont('Comic Sans MS', 50)
    loading_text = font.render('Loading...', True, (255, 255, 255))
    screen.blit(loading_text, (500-loading_text.get_size()[0]/2,500-loading_text.get_size()[1]/2))
    pygame.display.flip()

    game.map.player.key = False
    mapY = 500
    mapX = 500
    i = 0
    floor = game.map.floor
    if(floor>250):
        floor = 250
    for y in range(1000):
        for x in range(1000):
            game.map.tiles[y][x] = 0
            game.map.memory[y][x] = 0
    while(True):
        floorMap = floor
        if(floorMap>50):
            floorMap = 50
        tamY = random.randint(1,5)
        tamX = random.randint(1,5)
        for y in range(0-tamY,tamY,1):
            for x in range(0-tamX,tamX,1):
                if(mapY+tamY>50 and mapY+tamY<950 and mapX+tamX>50 and mapX+tamX<950):
                    game.map.tiles[mapY+y][mapX+x] = 1 # FREEBLOCK
        direction = random.randint(0,3)
        while(True):
            if(direction==0):
                mapY-=1
            if(direction==1):
                mapY+=1
            if(direction==2):
                mapX-=1
            if(direction==3):
                mapX+=1
            if(mapY>100 and mapY<900 and mapX>100 and mapX<900):
                game.map.tiles[mapY][mapX] = 1
            else:
                direction = random.randint(0,3)
            if(random.random()<0.25):
                direction = random.randint(0,3)
            if(random.randint(0,floor+1)==0):
                break
        if(i>=floorMap+1):
            if(random.random()<0.5):
                game.map.tiles[mapY][mapX] = 2
                break
        i+=1
    for it in range(game.map.floor):
        for i in range(10000):
            y = random.randint(0,999)
            x = random.randint(0,999)
            if(game.map.tiles[y][x]==1):
                game.map.tiles[y][x] = 3
                break
    while(True):
        if(random.random()<0.5):
            break
        while(True):
            y = random.randint(0,999)
            x = random.randint(0,999)
            if(game.map.tiles[y][x]==1):
                game.map.tiles[y][x] = 4
                break
    while(True):
        game.map.player.pos.y = random.randint(0,999)
        game.map.player.pos.x = random.randint(0,999)
        game.map.player.camPos.y = 525
        game.map.player.camPos.x = 525
        if(game.map.tiles[game.map.player.pos.y][game.map.player.pos.x]==1):
            break
    game.map.monsters = numpy.array([MONSTER() for _ in range(floor)])
    for monster in game.map.monsters:
        monster.pos.y = -1
        monster.pos.x = -1
    key = False
    for monster in game.map.monsters:
        for i in range(1000000):
            monster.pos.y = random.randint(0,999)
            monster.pos.x = random.randint(0,999)
            monster.camPos.y = (monster.pos.y*50-game.map.player.pos.y*50)
            monster.camPos.x = (monster.pos.x*50-game.map.player.pos.x*50)
            fail = False
            y = monster.pos.y
            x = monster.pos.x
            for i in range(100):
                if(random.random()<0.5):
                    if(random.random()<0.5):
                        y+=1
                    else:
                        y-=1
                else:
                    if(random.random()<0.5):
                        x+=1
                    else:
                        x-=1
                if(game.map.player.pos.y==y and game.map.player.pos.x==x):
                    fail = True
                    break
            if(fail):
                continue
            monster.id = random.randint(0,4)
            monster.attributes.hpMax = random.randint(1,10)
            monster.attributes.defense = random.randint(1,10)
            monster.attributes.strength = random.randint(1,10)
            monster.attributes.intelligence = 1
            monster.attributes.dexterity = 1
            if(game.map.tiles[monster.pos.y][monster.pos.x]==1):
                if(game.map.player.pos.y!=monster.pos.y and game.map.player.pos.x!=monster.pos.x):
                    attPoints = game.map.floor
                    while(attPoints>0):
                        attribute = random.randint(0,4)
                        if(monster.id==2):
                            if(random.random()<0.75):
                                attribute = 3
                        if(monster.id==3):
                            if(random.random()<0.75):
                                attribute = 4
                        if(attribute==0):
                            attPoints-=1
                            monster.attributes.hpMax+=random.randint(1,10)
                        if(attribute==1):
                            attPoints-=1
                            monster.attributes.defense+=random.randint(1,10)
                        if(attribute==2):
                            attPoints-=1
                            monster.attributes.strength+=random.randint(1,10)
                        if(attribute==3):
                            if(attPoints>=monster.attributes.intelligence):
                                attPoints-=monster.attributes.intelligence
                                monster.attributes.intelligence+=1
                        if(attribute==4):
                            if(attPoints>=int(monster.attributes.dexterity)):
                                attPoints-=int(monster.attributes.dexterity)
                                monster.attributes.dexterity+=0.1
                    if(monster.id==1):
                        monster.attributes.hpMax = game.map.floor
                        monster.attributes.defense = game.map.floor
                        monster.attributes.strength = game.map.floor
                        monster.attributes.intelligence = 1
                        monster.attributes.dexterity = 1
                    if(monster.id==5):
                        monster.attributes.hpMax = game.map.floor
                        monster.attributes.defense = game.map.floor
                        monster.attributes.strength = game.map.floor
                        monster.attributes.intelligence *= 2
                    if(random.random()<0.01):
                        monster.key = True
                        key = True
                    monster.attributes.hp = monster.attributes.hpMax
                    monster.alive = True
                    break
    if(not key):
        while(True):
            game.map.key.y = random.randint(0,999)
            game.map.key.x = random.randint(0,999)
            if(game.map.tiles[game.map.key.y][game.map.key.x]==1):
                key = True
                break
    itensQ = game.map.floor
    if(itensQ>9):
        itensQ = 9
    game.map.items = numpy.array([POS() for _ in range(itensQ)])
    for item in game.map.items:
        item.y = -1
        item.x = -1
    for item in game.map.items:
        for i in range(1000000):
            success = True
            item.y = random.randint(0,999)
            item.x = random.randint(0,999)
            for otherItem in game.map.items:
                if(item==otherItem):
                    continue
                if(item.y==otherItem.y and item.x==otherItem.x):
                    success = False
                    break
            if(success):
                if(game.map.tiles[item.y][item.x]==1):
                    break
#----------------------------------------------------------------------------------------------------------------------------------------
def menu(game = GAME()):
    global running
    screen.fill("black")
    for y in range(-10,10,1):
        for x in range(-10,10,1):
            Y = y*50+500
            X = x*50+500
            if(random.random()<0.1):
                pygame.draw.circle(screen,"#161616",[X+random.randint(10,40),Y+random.randint(10,40)],random.randint(1,10))
    font = pygame.font.SysFont('Comic Sans MS', 50)
    font_title = pygame.font.SysFont('Comic Sans MS', 80)
    title_text = font_title.render('DUNGEONS OF SIN',True,(255, 255, 255))
    screen.blit(title_text, ((500-title_text.get_size()[0]/2)+random.randint(-1,1),(250-title_text.get_size()[1]/2)+random.randint(-1,1)))
    if game.menu.selection==0:
        play_text = font.render('> PLAY', True, (255, 245, 150))
        screen.blit(play_text, ((500-play_text.get_size()[0]/2)+random.randint(-2,2),(450-play_text.get_size()[1]/2)+random.randint(-2,2)))
    else:
        play_text = font.render('  PLAY', True, (255, 255, 255))
        screen.blit(play_text, ((500-play_text.get_size()[0]/2),(450-play_text.get_size()[1]/2)))
    if game.menu.selection==1:
        exit_text = font.render('> EXIT', True, (255, 245, 150))
        screen.blit(exit_text, ((500-exit_text.get_size()[0]/2)+random.randint(-2,2),(550-exit_text.get_size()[1]/2)+random.randint(-2,2)))
    else:
        exit_text = font.render('  EXIT', True, (255, 255, 255))
        screen.blit(exit_text, ((500-exit_text.get_size()[0]/2),(550-exit_text.get_size()[1]/2)))
    
    if(keyboard.is_pressed('w')):
        game.menu.selection = 0
    if(keyboard.is_pressed('s')):
        game.menu.selection = 1
    if(keyboard.is_pressed('enter')):
        if game.menu.selection == 1:
            running = False
        if game.menu.selection == 0:
            game.play = True
#----------------------------------------------------------------------------------------------------------------------------------------
def play(game = GAME()):
    screen.fill("black")
    if(game.next):
        game.map.floor+=1
        game.map.player.key = False
        game.map.player.firstAtt = True
        put_attributes(game)
        if(running==False):
            return 0
        create_map(game)
        game.next = False
    render_game(game)
    move_player(game)
    move_monsters(game)
    render_dark(game)
    render_interface(game)
#----------------------------------------------------------------------------------------------------------------------------------------

game = GAME()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if game.play == False:
        game.map = MAP()
        game.next = True
        menu(game)
    else:
        play(game)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()