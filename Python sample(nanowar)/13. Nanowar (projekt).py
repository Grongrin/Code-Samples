import pygame
import random
import math


pygame.init()
width = 600
height = 600
screen = pygame.display.set_mode((width, height))
done = 2
ON = True
end = False
clock = pygame.time.Clock()
bckg_alpha=70
background = pygame.image.load(str(random.randrange(1,10))+".png")
background.set_alpha(bckg_alpha)

sizes = [18, 22, 28, 34]
growth_speed = 0.01
squad_speed = 0.7
squad_small = 6
AIpop = 0
commit = 0
color1 = (0, 0, 0)
color2 = (0, 0, 0)
a = 0 

target_node = None

node_list = []
AI_nodes = []
selected_nodes = []
squad_list = []

counter = 0

mouse_start_pos = (0, 0)


class Node:
    
    def __init__(self):
        
        self.coords = [0, 0]
        self.player = 'Neutral'
        self.size = 0
        self.pop = 0
        self.growth = 0
        
class Squad:
    
    def __init__(self):
        
        self.coords = [0, 0]
        self.player = 'Neutral'
        self.strenght = 0
        self.target = None
        self.dir = [0.0, 0.0]
        
        
def node_isnear(node1, node2):
    d = distance(node1.coords, node2.coords)
    if d > node1.size + node2.size + 10:
        return False
    else:
        return True
        
        
        
def mouse_on_node():
    global node_list
    for node in (node_list):
        if distance(node.coords, pygame.mouse.get_pos()) < node.size:
            return node
    return None
    
    
    
    
def attack(attacker, target, commit):
    if(attacker != target and attacker.pop*commit >= 1):
        new_squad = Squad()
        new_squad.player = attacker.player
        new_squad.strenght = math.floor(attacker.pop*commit)
        attacker.pop -= new_squad.strenght
        new_squad.target = target
        d = distance(attacker.coords, target.coords)
        new_squad.dir = [(target.coords[0]-attacker.coords[0])/d, (target.coords[1]-attacker.coords[1])/d]
            
        new_squad.coords = [attacker.coords[0]+attacker.size*new_squad.dir[0], attacker.coords[1]+attacker.size*new_squad.dir[1]]
        squad_list.append(new_squad)



def squad_on_destination(squad):
	if distance(squad.coords, squad.target.coords) < squad.target.size:
		return True
		
	else:
		return False
  
  
def distance(coords1, coords2):
    return math.hypot(coords1[0]-coords2[0], coords1[1]-coords2[1])

    
    
    
def select_rect(rect):
    for node in (node_list):
        if node.player == 'Me' and ((node.coords[0] > rect[0]-node.size and node.coords[0] < rect[0]+rect[2]+node.size and node.coords[1]>rect[1] and node.coords[1]<rect[1]+rect[3]) or (node.coords[0] > rect[0] and node.coords[0] < rect[0]+rect[2] and node.coords[1]>rect[1]-node.size and node.coords[1]<rect[1]+rect[3]+node.size) or distance(node.coords, (rect[0], rect[1])) < node.size or distance(node.coords, (rect[0]+rect[2], rect[1])) < node.size or distance(node.coords, (rect[0], rect[1]+rect[3])) < node.size or distance(node.coords, (rect[0]+rect[2], rect[1]+rect[3])) < node.size):
            selected_nodes.append(node)
            
            
def two_point_rect(p1, p2):
    if p1[0] < p2[0]:
        x = p1[0]       
    else:
        x = p2[0]
    
    if p1[1] < p2[1]:
        y = p1[1]       
    else:
        y = p2[1]
    
    xlen = math.fabs(p1[0] - p2[0])
    ylen = math.fabs(p1[1] - p2[1])
    return (x, y, xlen, ylen)
    
    
def node_str_balance(node, player):
    balance = 0
    if node.player == player:
        balance += math.floor(node.pop)
    else:
        balance -= math.floor(node.pop)
    for squad in (squad_list):
        if squad.target == node and squad.player == player:
            balance += squad.strenght
        elif squad.target == node:
            balance -= squad.strenght
    return balance
    
    
def Sort_range(lista, node):
    less=[]
    equal=[]
    greater=[]

    if len(lista) > 1:
        pivot = distance(lista[0].coords, node.coords)-(lista[0].size+node.size)
        for AInode in lista:
            if distance(AInode.coords, node.coords)-(AInode.size+node.size)<pivot:
                less.append(AInode)
            if distance(AInode.coords, node.coords)-(AInode.size+node.size)==pivot:
                equal.append(AInode)
            if distance(AInode.coords, node.coords)-(AInode.size+node.size)>pivot:
                greater.append(AInode)

        return Sort_range(less, node)+equal+Sort_range(greater, node)

    else:
        return lista
    
def startup():
    symmetry = random.randrange(3)
    node_count = random.randrange(3, 6)
    print(node_count, '\n\n')
    while(node_count > 1):
        new_node = Node()
        new_node.size = random.choice(sizes)
        new_node.pop = new_node.size//3
        if(new_node.size == 34):
            new_node.growth = growth_speed*1.55
        elif(new_node.size == 28):
            new_node.growth = growth_speed*1.35
        elif(new_node.size == 22):
            new_node.growth = growth_speed*1.15
        else:
            new_node.growth = growth_speed
        
        if symmetry == 0:
            x = random.randrange(new_node.size, width/2-new_node.size)
            y = random.randrange(new_node.size, height-new_node.size)
        elif symmetry == 1:
            x = random.randrange(new_node.size, width-new_node.size)
            y = random.randrange(new_node.size, height/2-new_node.size)
        elif symmetry == 2:
            x = random.randrange(new_node.size, width-2.5*new_node.size)
            y = random.randrange(x+1.5*new_node.size, height-new_node.size+1)
        else:
            x = random.randrange(new_node.size, width-2.5*new_node.size)
            y = random.randrange(new_node.size, height-x-1.5*new_node.size)
        
        new_node.coords = [x, y]
        
        collide = False
        for node in (node_list):
            if node_isnear(node, new_node):
                collide = True
                break
            
            
        if(collide == True):
            continue
        else:
            
            node_count -= 1
                
            node_list.append(new_node)
            
            
    while(node_count == 1):
        new_node = Node()
        new_node.size = random.choice(sizes)
        new_node.pop = new_node.size//3
        if(new_node.size == 34):
            new_node.growth = growth_speed*1.55
        elif(new_node.size == 28):
            new_node.growth = growth_speed*1.35
        elif(new_node.size == 22):
            new_node.growth = growth_speed*1.15
        else:
            new_node.growth = growth_speed
        
        if symmetry == 0:
            x = random.randrange(new_node.size, width/2-new_node.size-100)
            y = random.randrange(new_node.size, height-new_node.size)
        elif symmetry == 1:
            x = random.randrange(new_node.size, width-new_node.size)
            y = random.randrange(new_node.size, height/2-new_node.size-100)
        elif symmetry == 2:
            x = random.randrange(new_node.size, width-2.5*new_node.size-100)
            y = random.randrange(x+1.5*new_node.size+100, height-new_node.size+1)
        else:
            x = random.randrange(new_node.size, width-2.5*new_node.size-100)
            y = random.randrange(new_node.size, height-x-1.5*new_node.size-100)
        
        new_node.coords = [x, y]
        
        collide = False
        for node in (node_list):
            if node_isnear(node, new_node):
                collide = True
                break
        if(collide == True):
            continue
        else:
            
            node_count -= 1
            if node_count == 0:
                new_node.player = 'Me'
                new_node.pop += new_node.pop
                
            node_list.append(new_node)

            
            
            
    x = len(node_list)
    for i in range(x):
        new_node = Node()
        new_node.coords = node_list[i].coords
        new_node.size = node_list[i].size
        new_node.pop = node_list[i].pop
        new_node.growth = node_list[i].growth
        if symmetry == 0:
            new_node.coords = [width-new_node.coords[0], new_node.coords[1]]
        elif symmetry == 1:
            new_node.coords = [new_node.coords[0], height-new_node.coords[1]]
        else:
            new_node.coords = [width-new_node.coords[0], height-new_node.coords[1]]
        node_list.append(new_node)
        
    node_list[-1].player = 'AI'
    AI_nodes.append(node_list[-1])
            
    print(node_list, '\n\n\n\n\nSymmetry=', symmetry, 'node count=', node_count)
    
def clear():
    del node_list[:]
    del AI_nodes[:]
    del squad_list[:]
    del selected_nodes[:]

#startup()
pygame.mixer.music.load('music2.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)
while ON:
    if not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ON = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_start_pos = pygame.mouse.get_pos()
                
                if not (pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]):
                    selected_nodes.clear()
                    
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                select_rect(two_point_rect(mouse_start_pos, pygame.mouse.get_pos()))
                
    
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if mouse_on_node() in (node_list):
                    commit = 0.5
                    counter = 0
                    target_node = mouse_on_node()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and mouse_on_node() == target_node:
                    for node in (selected_nodes):
                        attack(node, target_node, commit)
    
#----------------------------------------Sztuczna inteligencja----------------------------------------
    
        if len(AI_nodes):
            AIstr = 0
            for AInode in (AI_nodes):
                AIstr += node_str_balance(AInode, 'AI')
            for node in (node_list):
                if node.player == 'Neutral' and -node_str_balance(node, 'AI')+1 < AIstr:
                    if -node_str_balance(node, 'Me') > node.pop:
                        node_garrison = -node_str_balance(node, 'Me')
                    else:
                        node_garrison = node.pop
                    AI_nodes = Sort_range(AI_nodes, node)
                    d1 = distance(AI_nodes[-1].coords, node.coords) - (AI_nodes[-1].size + node.size)
                    d2 = d1*10
                    for enemy in (node_list):
                        if(enemy.player == 'Me'):
                            AI_nodes = Sort_range(AI_nodes, enemy)
                            d2 = distance(AI_nodes[0].coords, enemy.coords) - (AI_nodes[0].size + enemy.size)
                            if ((d2 - d1) / squad_speed)*2.5*node.growth < node_garrison:
                                break
                   
                    if ((d2 - d1) / squad_speed)*2.5*node.growth > node_garrison:
                        AI_nodes = Sort_range(AI_nodes, node)
                        d=0
                        for squad in squad_list:
                            if squad.player == 'Me' and squad.target == node:
                                if distance(squad.coords, node.coords)-node.size > d:
                                    d=distance(squad.coords, node.coords)-node.size
                        if distance(node.coords, AI_nodes[0].coords)-(node.size+AI_nodes[0].size) > d:
                            i = 0
                            while node_str_balance(node, 'AI') <= 0 and i < len(AI_nodes):
                                AInode = AI_nodes[i]
                                attack(AInode, node, 1)
                                AIstr -= math.floor(AInode.pop)
                                i += 1
            for node in (node_list):
                AI_nodes = Sort_range(AI_nodes, node)
                if node.player == 'Me' and -node_str_balance(node, 'AI')+1+(distance(AI_nodes[-1].coords, node.coords)/squad_speed*growth_speed) < AIstr:     
                    i = 0
                    while node_str_balance(node, 'AI') <= 5 and i < len(AI_nodes):
                        AInode = AI_nodes[i]
                        attack(AInode, node, 1)
                        AIstr -= math.floor(AInode.pop)
                        i += 1
                if node.player == 'AI' and node_str_balance(node, 'AI') < 0:
                    i = 0
                    while node_str_balance(node, 'AI') <= 5 and i < len(AI_nodes):
                        AInode = AI_nodes[i]
                        if node_str_balance(AInode, 'AI') > math.floor(AInode.pop) // 2:
                            attack(AInode, node, 0.5)
                        i += 1


            
#------------------------------------Koniec sztucznej inteligencji------------------------------------
        
        screen.fill((255, 255, 255))
        screen.blit(background,(width/2 - background.get_width() // 2, height/2 - background.get_height() // 2))
        
        
        
        me = False
        ai = False
        
        for node in (node_list):
            #node = node_list[i]
            if(node.player == 'Me'):
                color = (0, 0, 250) 
                if(node.pop < 100):
                    node.pop += node.growth
                me = True
            
            elif(node.player == 'AI'):
                color = (250, 0, 0)
                if(node.pop < 100):
                    node.pop += node.growth
                ai = True
                    
            else:
                color = (200, 200, 200)
            if node in (selected_nodes):
                outline = (0, 255, 0)
            else:
                outline = (0, 0, 0)
            coords = (node.coords[0], node.coords[1])
            pygame.draw.circle(screen, outline, coords, node.size+1)
            pygame.draw.circle(screen, color, coords, node.size)
            
            
            font = pygame.font.SysFont("Euphemia", node.size)
            text = font.render(str(math.floor(node.pop)), True, (255, 255, 255))
            screen.blit(text,(node.coords[0] - text.get_width() // 2, node.coords[1] - text.get_height() // 2))
     

        
        for squad in (squad_list):
            
            if squad_on_destination(squad):
                
                if(squad.target.player == squad.player):
                    squad.target.pop += squad.strenght
                    
                else:
                    if squad.strenght > squad.target.pop:
                        if squad.target.player == 'AI':
                            AI_nodes.remove(squad.target)
                        elif squad.player == 'AI':
                            AI_nodes.append(squad.target)
                        squad.target.player = squad.player
                        squad.target.pop = squad.strenght - math.floor(squad.target.pop)
                        if squad.target in (selected_nodes):
                            selected_nodes.remove(squad.target)
    
                    else:
                        squad.target.pop -= squad.strenght
                
                squad_list.remove(squad)
                
                    
                
            
            if(squad.player == 'Me'):
                me = True
                color = (0, 0, 250)
                me = True
    
            else:
                color = (250, 0, 0)
                ai = True
                
            squad.coords = [squad.coords[0]+squad.dir[0]*squad_speed, squad.coords[1]+squad.dir[1]*squad_speed]
            coords = (int(squad.coords[0]), int(squad.coords[1]))
            
            pygame.draw.circle(screen, (0, 0, 0), coords, squad_small + int(math.sqrt(squad.strenght))+1)
            pygame.draw.circle(screen, color, coords, squad_small + int(math.sqrt(squad.strenght)))
            
            
            font = pygame.font.SysFont("Euphemia", squad_small + int(math.sqrt(squad.strenght)))
            text = font.render(str(squad.strenght), True, (255, 255, 255))
            screen.blit(text,(squad.coords[0] - text.get_width() // 2, squad.coords[1] - text.get_height() // 2))
            
            
        if not me and not ai:
            done = True
            clear()
        elif not me and ai:
            done = -1
            clear()
        elif me and not ai:
            done = 1
            clear()
            
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(screen, (0, 0, 0),two_point_rect(mouse_start_pos, pygame.mouse.get_pos()) ,1)
        if pygame.mouse.get_pressed()[2] and len(selected_nodes) and target_node in (node_list):
            counter += 1
            if counter > 10 and commit < 1:
                commit += 0.015
            elif commit > 1:
                commit = 1
            font = pygame.font.SysFont("Euphemia", 16)
            text = font.render(str(int(commit*100))+'%', True, (255, 255, 255))
            screen.blit(text,(pygame.mouse.get_pos()[0] - text.get_width() // 2, pygame.mouse.get_pos()[1] - text.get_height()))
            font = pygame.font.SysFont("Euphemia", 15)
            text = font.render(str(int(commit*100))+'%', True, (0, 0, 0))
            screen.blit(text,(pygame.mouse.get_pos()[0] - text.get_width() // 2, pygame.mouse.get_pos()[1] - text.get_height()))
    
        
    
        #print("\n\n\n\n\n\n\n\n\n\n\n", selected_nodes, "\n\n\n", squad_list, "\n\n\n", AI_nodes)
        #print(node_list)    
        

            


    if done != False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ON = False
            if not end and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if (pygame.mouse.get_pos()[0] > 175 and pygame.mouse.get_pos()[0] < 275 and pygame.mouse.get_pos()[1]>275 and pygame.mouse.get_pos()[1]<325):
                    startup()
                    node_list = Sort_range(node_list, node_list[-1])
                    background = pygame.image.load(str(random.randrange(1,10))+".png")
                    background.set_alpha(bckg_alpha)
                    done = False
                elif (pygame.mouse.get_pos()[0] > 325 and pygame.mouse.get_pos()[0] < 425 and pygame.mouse.get_pos()[1]>275 and pygame.mouse.get_pos()[1]<325):
                    ON = False
        
        if done == 1:
            image = pygame.image.load("win-screen.png")
            a=0
            end = True
            done = 2
        elif done == -1:
            image = pygame.image.load("sorry-you-just-lost-the-game.png")
            a=0
            end = True
            done = 2
        
        
        #screen.fill((255, 255, 255))
        screen.blit(background,(width/2 - background.get_width() // 2, height/2 - background.get_height() // 2))
        if (pygame.mouse.get_pos()[0] > 175 and pygame.mouse.get_pos()[0] < 275 and pygame.mouse.get_pos()[1]>275 and pygame.mouse.get_pos()[1]<325):
            color1 = (200, 200, 200)
            color2 = (255, 255, 255)
        elif (pygame.mouse.get_pos()[0] > 325 and pygame.mouse.get_pos()[0] < 425 and pygame.mouse.get_pos()[1]>275 and pygame.mouse.get_pos()[1]<325):
            color1 = (255, 255, 255)
            color2 = (200, 200, 200)
        else:
            color1 = (255, 255, 255)
            color2 = (255, 255, 255)
        
        font = pygame.font.SysFont("Euphemia", 25)
        
        pygame.draw.rect(screen, (0, 0, 0), (174, 274, 102, 52))
        pygame.draw.rect(screen, color1, (175, 275, 100, 50))
        text = font.render('Play', True, (0, 0, 0))
        screen.blit(text,(225 - text.get_width() // 2, 300 - text.get_height()//2))
    
        pygame.draw.rect(screen, (0, 0, 0), (324, 274, 102, 52))
        pygame.draw.rect(screen, color2, (325, 275, 100, 50))
        text = font.render('Exit', True, (0, 0, 0))
        screen.blit(text,(375 - text.get_width() // 2, 300 - text.get_height()//2))
        
        
        if end:
            if a > 3:
                end = False
                background = pygame.image.load(str(random.randrange(1,10))+".png")
                background.set_alpha(bckg_alpha)
            screen.fill((0, 0, 0))
            screen.blit(image,(width/2 - image.get_width() // 2, height/2 - image.get_height() // 2))
            
        
        
    pygame.display.flip()
    counter += 1
    if counter > 59:
        counter = 0
        a += 1
    clock.tick(60)
    
pygame.mixer.music.stop()

