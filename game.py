import pygame
import numpy
import random
import keyboard
import time

#----------------------------------------------------------------------------------------------------------------------------------------
class POS:
    def __init__(self):
        self.x = -1
        self.y = -1
class ATTRIBUTES:
    hp = 1
    hpMax = 1
    defense = 1
    strenght = 1
    dexterity = 1
    intelligence = 1
class ITEM:
    id = 0
    heal = 0
    hp = 0
    strength = 0
    defense = 0
    dexterity = 0
    intelligence = 0
    cursed = False
class PLAYER:
    attPoints = 0
    level = 1
    gold = 0
    exp = 0
    nextExp = 1
    keyInput = 0
    clockSpeed = time.perf_counter()
    alive = True
    inventoryOpened = False
    fallen = False
    key = False
    firstAtt = True
    inventory = numpy.array([[ITEM() for _ in range(4)] for _ in range(3)])
    pos = POS()
    inventorySelection = POS()
    attributes = ATTRIBUTES()
class MONSTER:
    def __init__(self):
        self.id = 0
        self.alive = False
        self.key = False
        self.clockSpeed = time.perf_counter()
        self.pos = POS()
        self.attributes = ATTRIBUTES()
class DAMAGESVIEW:
    def __init__(self):
        self.value = 0
        self.pos = POS()
        self.size = 0
class MAP:
    tiles = numpy.zeros((1000,1000))
    memory = numpy.zeros((1000,1000))
    floor = 0
    player = PLAYER()
    items = numpy.array([POS() for _ in range(floor)])
    monsters = numpy.array([MONSTER() for _ in range(floor)])
    damagesView = numpy.array([DAMAGESVIEW() for _ in range(50)])
class MENU:
    selection = 0
class GAME:
    attSelection = 0
    map = MAP
    menu = MENU
    play = False
    next = True
#----------------------------------------------------------------------------------------------------------------------------------------
def move_monsters(game = GAME()):
    for monster in game.map.monsters:
        if(monster.attributes.hp<1):
            monster.pos.y = -1
            monster.pos.x = -1
            monster.alive = False
        if(monster.alive):
            if(time.perf_counter()-monster.clockSpeed>1/monster.attributes.dexterity):
                monster.clockSpeed = time.perf_counter()
                target = POS()
                target.y = 0
                target.x = 0
                forbiddenBlcoks = [0]
                direction = random.randint(0,3)
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
                if(game.map.tiles[monster.pos.y][monster.pos.x] in forbiddenBlcoks):
                    monster.pos.y-=target.y
                    monster.pos.x-=target.x
                if(game.map.player.pos.y==monster.pos.y and game.map.player.pos.x==monster.pos.x):
                    monster.pos.y-=target.y
                    monster.pos.x-=target.x
                for otherMonster in game.map.monsters:
                    if(otherMonster==monster):
                        continue
                    else:
                        if(otherMonster.pos.y==monster.pos.y and otherMonster.pos.x==monster.pos.x):
                            monster.pos.y-=target.y
                            monster.pos.x-=target.x
                            break
#----------------------------------------------------------------------------------------------------------------------------------------
def move_player(game = GAME()):
    if(time.perf_counter()-game.map.player.clockSpeed>1/game.map.player.attributes.dexterity):
        clock = False
        target = POS()
        target.y = 0
        target.x = 0
        forbiddenBlcoks = [0]
        if(keyboard.is_pressed('w')):
            target.y-=1
            clock = True
        if(keyboard.is_pressed('s')):
            target.y+=1
            clock = True
        if(keyboard.is_pressed('a')):
            target.x-=1
            clock = True
        if(keyboard.is_pressed('d')):
            target.x+=1
            clock = True
        if(keyboard.is_pressed('enter')):
            if(game.map.tiles[game.map.player.pos.y][game.map.player.pos.x]==2):
                game.next = True
        if(keyboard.is_pressed('esc')):
            game.play = False
            game.next = True
        if(clock):
            game.map.player.clockSpeed = time.perf_counter()
        if((target.y!=0 and target.x==0) or (target.y==0 and target.x!=0)):
            game.map.player.pos.y+=target.y
            game.map.player.pos.x+=target.x
            if(game.map.tiles[game.map.player.pos.y][game.map.player.pos.x] in forbiddenBlcoks):
                game.map.player.pos.y-=target.y
                game.map.player.pos.x-=target.x
            for monster in game.map.monsters:
                if(game.map.player.pos.y==monster.pos.y and game.map.player.pos.x==monster.pos.x):
                    game.map.player.pos.y-=target.y
                    game.map.player.pos.x-=target.x

                    damage = random.randint(1,game.map.player.attributes.strenght)
                    defense = random.randint(0,monster.attributes.defense)
                    if(defense>damage):
                        defense = damage
                    monster.attributes.hp-=(damage-defense)
                    objectView = random.randint(0,49)

                    game.map.damagesView[objectView].value = (damage-defense)
                    game.map.damagesView[objectView].pos.y = random.randint(250,750)
                    game.map.damagesView[objectView].pos.x = random.randint(250,750)
                    game.map.damagesView[objectView].size = 50
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
    if(game.map.tiles[game.map.player.pos.y+y][game.map.player.pos.x+x]!=0):
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
    for y in range(-1,2,1):
        for x in range(-1,2,1):
            simulate_vision(game,y,x)
    for y in range(-10,10,1):
        for x in range(-10,10,1):
            Y = y*50+500
            X = x*50+500
            if(game.map.memory[game.map.player.pos.y+y][game.map.player.pos.x+x]==1):
                if(game.map.tiles[game.map.player.pos.y+y][game.map.player.pos.x+x]==0):
                    pygame.draw.rect(screen,"#545454",(X,Y,50,50))
                if(game.map.tiles[game.map.player.pos.y+y][game.map.player.pos.x+x]==1):
                    pygame.draw.rect(screen,"#a2a2a2",(X,Y,50,50))
                if(game.map.tiles[game.map.player.pos.y+y][game.map.player.pos.x+x]==2):
                    if(game.map.player.key):
                        pygame.draw.rect(screen,"#ffffff",(X,Y,50,50))
                    pygame.draw.rect(screen,"#363636",(X+5,Y+5,40,40))
                for monster in game.map.monsters:
                    if(monster.pos.y==game.map.player.pos.y+y and monster.pos.x==game.map.player.pos.x+x):
                        pygame.draw.circle(screen,"#ff0000",[X+25,Y+25],20)
                if(y==0 and x==0):
                    pygame.draw.circle(screen,"#ffffff",[X+25,Y+25],20)

    for damageObject in game.map.damagesView:
        if(damageObject.size>0):
            font = pygame.font.SysFont('Comic Sans MS', damageObject.size)
            damage_text = font.render(f"{damageObject.value}", True, "#ff0000")
            screen.blit(damage_text, (damageObject.pos.x+random.randint(-1,1),damageObject.pos.y+random.randint(-1,1)))
            if(random.random()<0.25):
                damageObject.size-=1
                damageObject.pos.y+=random.randint(-1,1)
                damageObject.pos.x+=random.randint(-1,1)

    font = pygame.font.SysFont('Comic Sans MS', 20)
    floor_text = font.render(f'Floor {game.map.floor}', True, (255, 255, 255))
    screen.blit(floor_text, (10+random.randint(-1,1),10+random.randint(-1,1)))
    level_text = font.render(f'level {game.map.player.level}', True, (255, 255, 255))
    screen.blit(level_text, (10+random.randint(-1,1),35+random.randint(-1,1)))

    hpBar = (game.map.player.attributes.hp/game.map.player.attributes.hpMax)*200
    pygame.draw.rect(screen,"#364935",(790,10,200,20))
    pygame.draw.rect(screen,"#08fe00",(790,10,hpBar,20))

    hpValue_text = font.render(f'{game.map.player.attributes.hp} / {game.map.player.attributes.hpMax}', True, "#000000")
    screen.blit(hpValue_text, (890-hpValue_text.get_size()[0]/2,19-hpValue_text.get_size()[1]/2))
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

        font = pygame.font.SysFont('Comic Sans MS', 50)
        points_text = font.render(f'ATTRIBUTES POINTS: {game.map.player.attPoints}', True, (255, 255, 255))
        if(game.attSelection==0):
            hp_text = font.render(f'> HP: {game.map.player.attributes.hp} / {game.map.player.attributes.hpMax}', True, (255, 245, 150))
        else:
            hp_text = font.render(f'HP: {game.map.player.attributes.hp} / {game.map.player.attributes.hpMax}', True, (255, 255, 255))
        if(game.attSelection==1):
            defense_text = font.render(f'> DEFENSE: {game.map.player.attributes.defense}', True, (255, 245, 150))
        else:
            defense_text = font.render(f'DEFENSE: {game.map.player.attributes.defense}', True, (255, 255, 255))
        if(game.attSelection==2):
            strenght_text = font.render(f'> STRENGHT: {game.map.player.attributes.strenght}', True, (255, 245, 150))
        else:
            strenght_text = font.render(f'STRENGHT: {game.map.player.attributes.strenght}', True, (255, 255, 255))
        if(game.attSelection==3):
            intelligence_text = font.render(f'> INTELLIGENCE: {game.map.player.attributes.intelligence}', True, (255, 245, 150))
        else:
            intelligence_text = font.render(f'INTELLIGENCE: {game.map.player.attributes.intelligence}', True, (255, 255, 255))
        if(game.attSelection==4):
            dexterity_text = font.render(f'> DEXTERY: {game.map.player.attributes.dexterity}', True, (255, 245, 150))
        else:
            dexterity_text = font.render(f'DEXTERY: {game.map.player.attributes.dexterity}', True, (255, 255, 255))
        if(game.attSelection==5):
            continue_text = font.render(f'> CONTINUE', True, (255, 245, 150))
        else:
            continue_text = font.render(f'CONTINUE', True, (255, 255, 255))

        screen.blit(points_text, (500-points_text.get_size()[0]/2+random.randint(-1,1),100-points_text.get_size()[1]/2+random.randint(-1,1)))
        screen.blit(hp_text, (500-hp_text.get_size()[0]/2+random.randint(-1,1),250-hp_text.get_size()[1]/2+random.randint(-1,1)))
        screen.blit(defense_text, (500-defense_text.get_size()[0]/2+random.randint(-1,1),350-defense_text.get_size()[1]/2+random.randint(-1,1)))
        screen.blit(strenght_text, (500-strenght_text.get_size()[0]/2+random.randint(-1,1),450-strenght_text.get_size()[1]/2+random.randint(-1,1)))
        screen.blit(intelligence_text, (500-intelligence_text.get_size()[0]/2+random.randint(-1,1),550-intelligence_text.get_size()[1]/2+random.randint(-1,1)))
        screen.blit(dexterity_text, (500-dexterity_text.get_size()[0]/2+random.randint(-1,1),650-dexterity_text.get_size()[1]/2+random.randint(-1,1)))
        screen.blit(continue_text, (500-continue_text.get_size()[0]/2+random.randint(-1,1),900-continue_text.get_size()[1]/2+random.randint(-1,1)))

        if(time.perf_counter()-game.map.player.clockSpeed>0.3):
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
                        game.map.player.attributes.hpMax+=1
                        game.map.player.attributes.hp+=1
                    if(game.attSelection==1):
                        game.map.player.attributes.defense+=1
                    if(game.attSelection==2):
                        game.map.player.attributes.strenght+=1
                    if(game.attSelection==3):
                        game.map.player.attributes.intelligence+=1
                    if(game.attSelection==4):
                        game.map.player.attributes.dexterity+=1
                    game.map.player.attPoints-=1
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
        tamY = random.randint(1,floorMap+1)
        tamX = random.randint(1,floorMap+1)
        if(tamY>10):
            tamY = random.randint(1,10)
        if(tamX>10):
            tamX = random.randint(1,10)
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
            if(random.random()<=0.25):
                direction = random.randint(0,3)
            if(random.randint(0,floor+1)==0):
                break
        if(i>=floorMap+1):
            if(random.random()<=0.5):
                game.map.tiles[mapY][mapX] = 2
                break
        i+=1
    while(True):
        game.map.player.pos.y = random.randint(0,999)
        game.map.player.pos.x = random.randint(0,999)
        if(game.map.tiles[game.map.player.pos.y][game.map.player.pos.x]==1):
            break
    game.map.monsters = numpy.array([MONSTER() for _ in range(floor)])
    for monster in game.map.monsters:
        monster.pos.y = -1
        monster.pos.x = -1
    key = False
    for monster in game.map.monsters:
        while(True):
            monster.pos.y = random.randint(0,999)
            monster.pos.x = random.randint(0,999)
            monster.alive = True
            if(key==False):
                monster.key = True
                key = True
            if(game.map.tiles[monster.pos.y][monster.pos.x]==1):
                if(game.map.player.pos.y!=monster.pos.y and game.map.player.pos.x!=monster.pos.x):
                    break
    for item in game.map.items:
        item.y = -1
        item.x = -1
    for monster in game.map.items:
        item.y = random.randint(0,999)
        item.x = random.randint(0,999)
        if(game.map.tiles[item.y][item.x]!=1):
            item.y = -1
            item.x = -1
#----------------------------------------------------------------------------------------------------------------------------------------
def menu(game = GAME()):
    screen.fill("black")
    font = pygame.font.SysFont('Comic Sans MS', 50)
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
        game.map.player.firstAtt = True
        game.map.player.attPoints += 1
        put_attributes(game)
        if(running==False):
            return 0
        create_map(game)
        game.next = False
    render_game(game)
    move_player(game)
    move_monsters(game)
#----------------------------------------------------------------------------------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
running = True

game = GAME()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if game.play == False:
        game.map = MAP()
        menu(game)
    else:
        play(game)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()