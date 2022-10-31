import pygame
import random
import time
import sys

#===============================================================================
#                       funções                                         =
#===============================================================================
def check_neighbor_rooms(pos, item_list):
    """ Verifica cada célula ortogonal ao lado de pos para o item solicitado
    retorna True assim que o item for encontrado.
    """
    exits = cave[pos]
    return any(item in cave[pos] for item in item_list)
        
def draw_room( pos, screen):
    """ Desenha a sala no buffer
    """
    x=0
    y=1
    exits = cave[player_pos]
    screen.fill( (0,0,0) ) #rgb preto no background

 
    circle_radius = int ((SCREEN_WIDTH//2)*.75)
    pygame.draw.circle(screen, BROWN, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), circle_radius, 0)

    #desenho das saidas no mapa
    if exits[LEFT] > 0:
        left = 0
        top = SCREEN_HEIGHT//2-40
        pygame.draw.rect(screen, BROWN, ( (left,top), (SCREEN_WIDTH//4,80)), 0)
    if exits[RIGHT] > 0:
        #desenha saidas da direita
        left = SCREEN_WIDTH-(SCREEN_WIDTH//4)
        top = SCREEN_HEIGHT//2-40
        pygame.draw.rect(screen, BROWN, ((left,top), (SCREEN_WIDTH//4,80)), 0)
    if exits[UP] > 0:
        #dsaidas de cima no topo
        left = SCREEN_WIDTH//2-40
        top = 0
        pygame.draw.rect(screen, BROWN, ((left,top), (80,SCREEN_HEIGHT//4)), 0)
    if exits[DOWN] > 0 :
        #botao de saida
        left = SCREEN_WIDTH//2-40
        top = SCREEN_HEIGHT-(SCREEN_WIDTH//4)
        pygame.draw.rect(screen, BROWN, ((left,top), (80,SCREEN_HEIGHT//4)), 0)
        
    #verifica se tem inimigos por perto
    bats_near = check_neighbor_rooms(player_pos, bats_list)
    pit_near = check_neighbor_rooms(player_pos, pits_list)
    wumpus_near = check_neighbor_rooms(player_pos, [wumpus_pos, [-1,-1]])
    
    #círculo de sangue se o Wumpus estiver por perto
    if wumpus_near == True:
        circle_radius = int ((SCREEN_WIDTH//2)*.5)
        pygame.draw.circle(screen, RED, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), circle_radius, 0)

    #poço em preto se estiver presente
    if player_pos in pits_list:
        circle_radius = int ((SCREEN_WIDTH//2)*.5)
        pygame.draw.circle(screen, BLACK, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), circle_radius, 0)
     
    #constroi player
    screen.blit(player_img,(SCREEN_WIDTH//2-player_img.get_width()//2,SCREEN_HEIGHT//2-player_img.get_height()//2))

    #morcego
    if player_pos in bats_list:
        screen.blit(bat_img,(SCREEN_WIDTH//2-bat_img.get_width()//2,SCREEN_HEIGHT//2-bat_img.get_height()//2))

    #wumpus
    if player_pos == wumpus_pos:
        screen.blit(wumpus_img,(SCREEN_WIDTH//2-wumpus_img.get_width()//2,SCREEN_HEIGHT//2-wumpus_img.get_height()//2))

    #textos
    y_text_pos = 0
    pos_text = font.render("POS:"+str(player_pos), 1, (0, 255, 64))
    screen.blit(pos_text,(0, 0))
    arrow_text = font.render("flechas: "+str(num_arrows), 1, (0, 255, 64))
    y_text_pos = y_text_pos+pos_text.get_height()+10
    screen.blit(arrow_text,(0, y_text_pos))
    if bats_near == True:
        bat_text = font.render("existem morcegos por perto", 1, (0, 255, 64))
        y_text_pos = y_text_pos+bat_text.get_height()+10
        screen.blit(bat_text,(0, y_text_pos))
    if pit_near == True:
        pit_text = font.render("possui um buraco por perto", 1, (0, 255, 64))
        y_text_pos = y_text_pos+pit_text.get_height()+10
        screen.blit(pit_text,(0, y_text_pos))

    if player_pos in bats_list: #se os morcegos estão aqui, vá em frente e vire a tela e espere um pouco
        pygame.display.flip()
        time.sleep(2.0)
        
def populate_cave():
    global player_pos, wumpus_pos

    #inicio do jogador e seu lugar
    player_pos = random.randint(1, 20)

    # onde fica o monstro
    place_wumpus()
    
    #place the bats
    for bat in range(0,NUM_BATS):
        place_bat()

    #place the pits
    for pit in range (0,NUM_PITS):
        place_pit()

    #place the arrows
    for arrow in range (0,NUM_ARROWS):
        place_arrow()

    print ("jogador em: "+str(player_pos))
    print ("Wumpus em: "+str(wumpus_pos))
    print ("morcegos em:" + str(bats_list) )
    print ("poço em:" + str(pits_list))
    print ("flechas em:" +str(arrows_list))

def place_wumpus():
    global player_pos, wumpus_pos
    
    wumpus_pos = player_pos
    while (wumpus_pos == player_pos):
        wumpus_pos = random.randint(0,20)

def place_bat():
   #lugar dos morcegos
    bat_pos = player_pos
    while bat_pos == player_pos or (bat_pos in bats_list) or (bat_pos == wumpus_pos) or (bat_pos in pits_list):
        bat_pos = random.randint(1,20)
    bats_list.append(bat_pos)

def place_pit():
    pit_pos = player_pos
    while (pit_pos == player_pos) or (pit_pos in bats_list) or (pit_pos == wumpus_pos) or (pit_pos in pits_list):
        pit_pos = random.randint(1,20)
    pits_list.append(pit_pos)

def place_arrow():
    arrow_pos = player_pos
    while (arrow_pos == player_pos) or (arrow_pos in bats_list) or (arrow_pos == wumpus_pos) or (arrow_pos in pits_list):
        arrow_pos = random.randint(1,20)
    arrows_list.append(arrow_pos)
    
def check_room(pos):
    global player_pos, screen, num_arrows
    
    #é um wumpus?
    if player_pos == wumpus_pos:
        game_over("Você foi comido por um WUMPUS!!!")

    #é um poço?
    if player_pos in pits_list:
        game_over("Você caiu em um poço sem fundo!!")

    #sao morcegos? entao podem te jogar pra outro lugar
    if player_pos in bats_list:
        print("Os morcegos te pegam e te colocam em outro lugar na caverna!")
        screen.fill(BLACK)
        bat_text = font.render("Os morcegos te pegam e te colocam em outro lugar na caverna!", 1, (0, 255, 64))
        textrect = bat_text.get_rect()
        textrect.centerx = screen.get_rect().centerx
        textrect.centery = screen.get_rect().centery
        screen.blit(bat_text,textrect)
        pygame.display.flip()
        time.sleep(2.5)
        
        #move os morcegos
        new_pos = player_pos
        
        while (new_pos == player_pos) or (new_pos in bats_list) or (new_pos == wumpus_pos) or (new_pos in pits_list):
            new_pos = random.randint(1,20)
        bats_list.remove(player_pos)   
        bats_list.append(new_pos)
        print ("morcegos em: "+str(new_pos))
                
        #e assim move o jogador
        new_pos = player_pos # defina new_pos igual ao sistema operacional antigo para que o primeiro teste falhe
        # Agora coloque o jogador em um local aleatório
        while (new_pos == player_pos) or (new_pos in bats_list) or (new_pos == wumpus_pos) or (new_pos in pits_list):
            new_pos = random.randint(1,20)
        player_pos = new_pos
        print ("jogador em:"+str(player_pos))

    #item alguma flecha?
    if player_pos in arrows_list:
        screen.fill(BLACK)
        text = font.render("voce achou uma flecha", 1, (0, 255, 64))
        textrect = text.get_rect()
        textrect.centerx = screen.get_rect().centerx
        textrect.centery = screen.get_rect().centery
        screen.blit(text,textrect)
        pygame.display.flip()
        time.sleep(2.5)
        num_arrows +=1
        arrows_list.remove(player_pos)
            
def reset_game():
    global num_arrows
    populate_cave()
    num_arrows = 1

def game_over(message):
    global screen
    time.sleep(1.0)
    screen.fill(RED)
    text=font.render(message, 1, (0, 255, 64))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery
    screen.blit(text,textrect)
    pygame.display.flip()
    time.sleep(2.5)
    print (message)
    pygame.quit()
    sys.exit()

def move_wumpus():
    global wumpus_pos

    if mobile_wumpus == False or random.randint(1,100) > wumpus_move_chance:
        return
        
    exits = cave[wumpus_pos]
    
    for new_room in exits:
        if new_room == 0:
            continue
        elif new_room == player_pos:
            continue
        elif new_room in bats_list:
            continue
        elif new_room in pits_list:
            continue
        else:
            wumpus_pos = new_room
            break
            
    print ("Wumpus se moveu para:"+str(wumpus_pos))
                   
def shoot_arrow(direction):
    global num_arrows, player_pos

    hit = False
    
    if num_arrows == 0:
        return False
    num_arrows -= 1
    
    if wumpus_pos == cave[player_pos][direction]:
        hit = True

    if hit == True:
        game_over("Seu objetivo era certo e você matou o Wumpus!")
        pygame.quit()
        sys.exit()
    else:    
        print ("Sua flecha navega na escuridão, para nunca mais ser vista...")
        place_wumpus()
    if num_arrows == 0:
        game_over("Você está sem flechas. Você morreu!")
        pygame.quit()
        sys.exit()

def check_pygame_events():
    global player_pos
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.key ==pygame.K_LEFT:
             if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                shoot_arrow(LEFT)
             elif cave[player_pos][LEFT] > 0: 
                player_pos=cave[player_pos][LEFT]
                move_wumpus()
        elif event.key == pygame.K_RIGHT:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                shoot_arrow(RIGHT)
            elif cave[player_pos][RIGHT] >0:
                player_pos = cave[player_pos][RIGHT]
                move_wumpus()
        elif event.key == pygame.K_UP:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                shoot_arrow(UP)
            elif cave[player_pos][UP] > 0:
                player_pos = cave[player_pos][UP]
                move_wumpus()
        elif event.key ==pygame.K_DOWN:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                shoot_arrow(DOWN)
            elif cave[player_pos][DOWN] > 0:
                player_pos = cave[player_pos][DOWN]
                move_wumpus()

def print_instructions():
    print(
    '''
                             Cace o Wumpus!
Este é o jogo de "Caçar o Wumpus". Você foi lançado em um
caverna escura de 20 quartos com um temível Wumpus. A caverna tem a forma de um
dodachedron e a única saída é matar o Wumpus. Para esse fim
você tem um arco com uma flecha. Você pode encontrar mais flechas de azar
vítimas de Wumpus passadas na caverna. Há outros perigos na caverna,
especificamente morcegos e poços sem fundo.

    * Se você ficar sem flechas, você morre.
    * Se você acabar na mesma sala com o Wumpus, você morre.
    * Se você cair em um poço sem fundo, você morre.
    * Se você acabar em uma sala com morcegos, eles vão buscá-lo
      e depositá-lo em um local aleatório.

Se você estiver perto do Wumpus, verá as manchas de sangue nas paredes.
Se você estiver perto de morcegos, você os ouvirá e se estiver perto de um
pit você vai sentir o ar fluindo para baixo.

Use as setas para mover. Pressione a tecla <SHIFT> e uma tecla de seta para
dispare sua flecha.
    '''
    )
    
#===============================================================================
#                       contrução do jogo e suas areas                            =
#===============================================================================
#tamanho de tela
SCREEN_WIDTH = SCREEN_HEIGHT= 1000

bat_img = pygame.image.load('images/bat.png')
player_img = pygame.image.load('images/player.png')
wumpus_img = pygame.image.load('images/wumpus.png')
arrow_img = pygame.image.load('images/arrow.png')

NUM_BATS = 3
NUM_PITS = 3
NUM_ARROWS = 0

player_pos = 0
wumpus_pos = 0
num_arrows = 1 
mobile_wumpus = False 
wumpus_move_chance = 50

#constantes das direções
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

#definições das cores
BROWN = 193,154,107
BLACK = 0,0,0
RED = 138,7,7

cave = {1: [0,8,2,5], 
    2: [0,10,3,1],
    3: [0,12,4,2],
    4: [0,14,5,3], 
    5: [0,6,1,4],
    6: [5,0,7,15],
    7: [0,17,8,6],
    8: [1,0,9,7],
    9: [0,18,10,8],
    10: [2,0,11,9],
    11: [0,19,12,10], 
    12: [3,0,13,11], 
    13: [0,20,14,12], 
    14: [4,0,15,13], 
    15: [0,16,6,14], 
    16: [15,0,17,20],
    17: [7,0,18,16], 
    18: [9,0,19,17], 
    19: [11,0,20,18], 
    20: [13,0,16,19] }

bats_list = []
pits_list = []
arrows_list = []

#===============================================================================
#                       areas iniciais area                                   =
#===============================================================================

print_instructions()
input("Press <ENTER> to begin.")
pygame.init()
screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE )
pygame.display.set_caption("Hunt the Wumpus")

#carregam imgs
bat_img = pygame.image.load('images/bat.png')
player_img = pygame.image.load('images/player.png')
wumpus_img = pygame.image.load('images/wumpus.png')
arrow_img = pygame.image.load('images/arrow.png')

#setup
font = pygame.font.Font(None, 36)

#seta o inicio do jogo
reset_game()

#===============================================================================
#                       main game                                         =
#===============================================================================
while True:
    check_pygame_events()     
    draw_room(player_pos, screen)
    pygame.display.flip()   
    check_room(player_pos)
    

    
    
    
