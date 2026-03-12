import pygame
import sys
import random

pygame.init()

max_x = 480
max_y = 480

screen = pygame.display.set_mode((max_x, max_y))
pygame.display.set_caption("SNAKKKKKKE")


GREEN1 = (170, 215, 81)
GREEN2 = (162, 209, 73)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
square_size = 30
number_of_squares = int(max_x / square_size * max_y / square_size)
start_pos = [60, 150]
clock = pygame.time.Clock()

def random_pos() : 
    return [random.randint(0, (max_x // square_size) - 1) * square_size, random.randint(0, (max_y // square_size) - 1) * square_size]
  
class Player:
    direction = (0, 0)
    pos = start_pos.copy()
    size = 14
    score = 0
    last_pos = [[0,0]]
    apple_pos = random_pos()

    def move(self):
        new_pos = [
            self.pos[0] + self.direction[0] * square_size,
            self.pos[1] - self.direction[1] * square_size
        ]

        ate_apple = (new_pos == self.apple_pos)

        if not (0 <= new_pos[0] < max_x and 0 <= new_pos[1] < max_y):
            self.game_over()
            return

        body = self.last_pos if ate_apple else self.last_pos[1:]

        if new_pos in body:
            self.game_over()
            return

        self.pos = new_pos
        self.last_pos.append(self.pos.copy())

        if ate_apple:
            self.score += 1
            self.apple_pos = random_pos()
            while self.apple_pos in self.last_pos:
                self.apple_pos = random_pos()
        else:
            if len(self.last_pos) > self.score:
                self.last_pos.pop(0)
    
    def draw(self):
        for pos in self.last_pos :
            if pos != [0,0] :
                pygame.draw.rect(screen, GREEN1, (*pos,square_size -1, square_size-1)) # Dessin du joueur 
        pygame.draw.rect(screen, RED, (*self.apple_pos, square_size - 1, square_size - 1)) # Dessin de la pomme
    
    def game_over(self):
        print(f"Game Over! Final Score: {self.score}")
        pygame.quit()
        sys.exit()
 
def get_direction(direction):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and direction != (1, 0):
        return (-1, 0)
    if keys[pygame.K_RIGHT] and direction != (-1, 0):
        return (1, 0)
    if keys[pygame.K_UP] and direction != (0, -1):
        return (0, 1)
    if keys[pygame.K_DOWN] and direction != (0, 1):
        return (0, -1)
    return direction


def simple_auto_move(player):
    head_x, head_y = player.pos
    apple_x, apple_y = player.apple_pos

    if apple_x > head_x : 
        return (1, 0) #aller a droite
    elif apple_x < head_x : 
        return (-1, 0) #aller a gauche
    elif apple_y < head_y : 
        return (0, 1) #aller en haut
    elif apple_y > head_y : 
        return (0, -1) #aller en bas
    else : 
        return player.direction
        
p1 = Player()

def ia_move(player):
    
    return

running = True

while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: 
            new_direction = get_direction(p1.direction)
            if (new_direction[0] != -p1.direction[0]) or (new_direction[1] != -p1.direction[1]):
                p1.direction = new_direction
            break
    
    if (p1.score == number_of_squares) :
        p1.game_over()

    p1.move()
    p1.draw()   
    pygame.display.flip()
    clock.tick(5)

# Quit pygame
p1.game_over()
