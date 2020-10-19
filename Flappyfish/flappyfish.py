#importando propriedades usadas no codigo------------------

import pygame, random
from pygame.locals import *

#Definindo tamanho da janela de jogo----------------------

SCREEN_WIDTH = 800 #Definindo largura
SCREEN_HEIGHT = 800 #Definindo comprimento

#Definindo propriedades dos elementos---------------------
SPEED = 10  #Propriedade Velocidade dos elementos
GRAVITY = 1  #Propriedade gravidade do jogo
GAME_SPEED = 10  #Propriedade Velocidade do jogo

GROUND_WIDTH = 2 * SCREEN_WIDTH #Propriedade de largura do chão
GROUND_HEIGHT = 100 #Propriedade de comprimento do chão

TUBO_WIDTH = 80 #Propriedade de largura do tubo
TUBO_HEIGHT = 500 #Propriedade de comprimento do tubo

TUBO_GAP = 200 #Propriedade de espaçamento entre os tubos

#Definindo uma classe para os tubos----------------------

class Tubo(pygame.sprite.Sprite):# classe criada para os tubos

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)#iniciando o pygame para usar os sprites

        self.image = pygame.image.load('tubo.png').convert_alpha()# carregando o sprite e removendo o espaço transparente
        self.image = pygame.transform.scale(self.image, (TUBO_WIDTH,TUBO_HEIGHT))  # reorganizando a resolução dos tubos
        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)#usa-se o flip para inverter a imagem do tubo 
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

#Definindo uma classe para o chão----------------------
        
class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('base.png').convert_alpha() #carregando a imagem do chão 
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT)) # ajustando a imagem a tela

        self.mask = pygame.mask.from_surface(self.image) #criando a mascara para criar as colisões

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
    
    def update(self): #atualizando o chao pixel a pixel
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite): #checando se esta fora da tela
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_tubos(xpos):
    size = random.randint(100, 300)
    tubo = Tubo(False, xpos, size)
    tubo_inverted = Tubo(True, xpos, SCREEN_HEIGHT - size - TUBO_GAP)
    return (tubo, tubo_inverted)


#Definindo uma classe para o peixe----------------------

class Fish(pygame.sprite.Sprite):#classe para modelar o peixe

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  #iniciando o pygame

        self.images = pygame.image.load('bluefish1.png').convert_alpha(), #carregando as imagens             

        self.speed = SPEED  # adicionando velocidade para o peixe

        self.current_image = 0

        self.image = pygame.image.load('bluefish1.png').convert_alpha()  # carregando a imagem do peixe
        self.mask = pygame.mask.from_surface(self.image) #criando uma mascara para o peixe

        self.rect = self.image.get_rect()  #posicionando o peixe na tela
        self.rect[0] = SCREEN_WIDTH / 2  #colocando as informaçoes no rect para deixar o peixe no meio da tela
        self.rect[1] = SCREEN_HEIGHT / 2  #colocando as informaçoes no rect para deixar o peixe no meio da tela

    def update(self):
        self.speed += GRAVITY #adicionando gravidade em todos os momentos
        self.rect[1] += self.speed
    
    def bump(self): 
        self.speed = -SPEED #bump para o peixe subir

#Depois de todas as classes definidas, começa o jogo-----

pygame.init() #iniciando o pygame 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #criando a tela de jogo

BACKGROUND = pygame.image.load('background-day.jpg') #carregando a imagem que sera o background
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT)) #convertendo a imagem para o tamanho da tela

fish_group = pygame.sprite.Group() #grupo para adicionar o passaro
fish = Fish() #criado um peixe do tipo peixe
fish_group.add(fish) #foi adicionado no proprio grupo

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground) #colocando o chão no seu proprio grupo

tubo_group = pygame.sprite.Group()
for i in range(2):
    tubos = get_random_tubos(SCREEN_WIDTH * i + 800)
    tubo_group.add(tubos[0]) #adicionando tubos ao proprio grupo 
    tubo_group.add(tubos[1]) #adicionando tubos ao proprio grupo 


clock = pygame.time.Clock() #criando o clock para determinar o fps

while True: #repetição principal do jogo 
    clock.tick(30)
    for event in pygame.event.get(): #evento para fechar o jogo
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:# caso aperte espaço, o peixe sobe
            if event.key == K_SPACE:
                fish.bump()

        if event.type == KEYDOWN:# caso aperte seta para cima, o jogo fecha
            if event.key == K_UP:
                pygame.quit()
                

    screen.blit(BACKGROUND, (0, 0))#fazendo a imagem aparecer em todos os frames, e na posição na tela

    if is_off_screen(ground_group.sprites()[0]): #definindo que se o chão sair da tela, pode ser deletado 
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)#colocando o chão no seu proprio grupo

    if is_off_screen(tubo_group.sprites()[0]) :#definindo que se os tubos sairem da tela, podem ser deletados
        tubo_group.remove(tubo_group.sprites()[0]) #removendo os tubos
        tubo_group.remove(tubo_group.sprites()[0])#removendo os tubos

        tubos = get_random_tubos(SCREEN_WIDTH * 2) #criando novos tubos em locais aleatorios

        tubo_group.add(tubos[0]) #adicionando os tubos
        tubo_group.add(tubos[1])#adicionando os tubos

    fish_group.update() #atualizando as informaçoes do peixe
    ground_group.update() #atualizando as informações do chão
    tubo_group.update() #atualizando as informações dos tubos

    fish_group.draw(screen) #desenhando o peixe
    tubo_group.draw(screen) #desenhando o s tubos
    ground_group.draw(screen) #desenhando o chao

    pygame.display.update() #a tela fica atualizando para que o jogo funcione
    
# Criando condição para acabar o jogo

    if(pygame.sprite.groupcollide(fish_group, ground_group, False, False, pygame.sprite.collide_mask) or #condições para que se o peixe colida 
       pygame.sprite.groupcollide(fish_group, tubo_group, False, False, pygame.sprite.collide_mask)): #com a mascara do tubo ou do chao    
        input()
        break
        
       
    
