import pygame
import random
import numpy as np
import matplotlib.pyplot as plt
import os

gamemode = 2
max_x = 480
max_y = 480 

GREEN1 = (34, 139, 34)   # Forest Green
GREEN2 = (50, 205, 50)   # Lime Green
RED = (200, 0, 0)
DARK_RED = (150, 0, 0)
WHITE = (255, 255, 255)
BG_COLOR = (20, 20, 20)  # Dark theme
GRID_COLOR = (30, 30, 30)

RIGHT = (1, 0)
LEFT  = (-1, 0)
DOWN  = (0, 1)
UP    = (0, -1)

square_size = 30
start_pos = [60, 150]
number_of_squares = int(max_x / square_size * max_y / square_size)
top_scores = []
data = []
neural_size = [5, 90, 3] # input, inside layers, output SIZE


def random_pos() : 
    return [random.randint(0, (max_x // square_size) - 1) * square_size, random.randint(0, (max_y // square_size) - 1) * square_size]

def distance(pos1, pos2):
    return (pos1[0] - pos2 [0])**2 + (pos1[1] - pos2[1])**2

class AI:
    def __init__(self, weights = None):
        if weights is None:
            self.weights = []
            for i in range(len(neural_size)-1):
                self.weights.append(np.random.randn(neural_size[i], neural_size[i+1]) * np.sqrt(2 / neural_size[i]))
        else:
            self.weights = weights
        self.apple_pos = random_pos()
        self.value = 0
        self.length = 3
        self.body =  [[60, 150], [60, 150], [60, 150]]
        self.body_set = {(start_pos[0], start_pos[1])}
        self.pos = start_pos.copy()
        self.direction = RIGHT
        self.alive = True
        self.steps_left = 200

    def reset(self):
        self.apple_pos = random_pos()
        self.value = 0
        self.length = 1
        self.body =  [[60, 150]]
        self.body_set = {(start_pos[0], start_pos[1])}
        self.pos = start_pos.copy()
        self.direction = RIGHT
        self.alive = True
        self.steps_left = 200

    def move(self):
        dist_before = distance(self.pos, self.apple_pos)

        new_pos = [self.pos[0] + self.direction[0] * square_size, self.pos[1] + self.direction[1] * square_size]
        new_pos_tuple = tuple(new_pos)

        if not (0 <= new_pos[0] < max_x and 0 <= new_pos[1] < max_y): # Bordures
            self.value -= 25
            self.game_over()
            return

        if new_pos_tuple in self.body_set:  # Corps
            self.value -= 50
            self.game_over()
            return

        ate_apple = (new_pos == self.apple_pos)
        

        self.body.append(new_pos)
        self.body_set.add(new_pos_tuple)
        self.pos = new_pos

        if ate_apple:
            self.value += 200
            self.steps_left = 200
            self.length += 1 
            self.apple_pos = random_pos()
            while tuple(self.apple_pos) in self.body_set:
                self.apple_pos = random_pos()
        else:
            self.steps_left -= 1
            dist_after = distance(self.pos, self.apple_pos)
            if dist_after < dist_before:
                self.value += 1
            else:
                self.value -= 2
            if len(self.body) > self.length:
                old_tail = self.body.pop(0) 
                self.body_set.discard(tuple(old_tail))

        if self.steps_left <= 0:
            self.game_over()
            
    def draw(self, screen):
        screen.fill(BG_COLOR)
        for x in range(0, max_x, square_size):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, max_y))
        for y in range(0, max_y, square_size):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (max_x, y))

        for i, pos in enumerate(self.body):
                pygame.draw.rect(screen, GREEN1, (*pos, square_size - 1, square_size - 1))
                pygame.draw.rect(screen, GREEN2, (pos[0] + 4, pos[1] + 4, square_size - 9, square_size - 9))

        apple_rect = (*self.apple_pos, square_size - 2, square_size - 2)
        pygame.draw.ellipse(screen, RED, apple_rect)
        pygame.draw.ellipse(screen, DARK_RED, (self.apple_pos[0]+4, self.apple_pos[1]+2, 8, 8))

        font = pygame.font.SysFont("Arial", 24, bold=True)
        score_text = font.render(f"Apples: {self.length - 3 }", True, WHITE)
        screen.blit(score_text, (10, 10))
        
    def score(self):
        return [self.value, self.weights]
    
    def game_over(self):
        #print(f"Game Over! Final Score: {self.value}")
        global data
        data.append(self.score())
        self.alive = False

def wall_distance(pos, direction):
        up = pos[1] / max_y
        down = (max_y - pos[1]) / max_y
        left = pos [0] / max_x
        right = (max_x - pos[0]) / max_x
        if direction == UP : 
            return up, left, right
        elif direction == DOWN : 
            return down, right, left
        elif direction == LEFT:
            return left, down, up
        else :
            return right, up, down
        
def is_wall(pos):
    return True if (pos[0] < 0 or pos[0] >= max_x or pos[1] < 0 or pos[1] >= max_y) else False

def is_body(p, pos):
    return True if tuple(pos) in p.body_set else False

def collision(player, pos):
    return 0 if is_wall(pos)  else 1 # or is_body(player, pos)

def move_neural(player):

    vx, vy = player.direction

    dx = (player.apple_pos[0] - player.pos[0]) / max_x
    dy = (player.apple_pos[1] - player.pos[1]) / max_y

    if player.direction == LEFT: dxp, dyp = -dx, -dy
    elif player.direction == UP: dxp, dyp = dy, -dx
    elif player.direction == DOWN: dxp, dyp = -dy, dx
    else: dxp, dyp = dx, dy
    
    b_front = collision(player, [player.pos[0] + vx * square_size, player.pos[1] + vy * square_size])
    b_left  = collision(player, [player.pos[0] - vy * square_size, player.pos[1] + vx * square_size])
    b_right = collision(player, [player.pos[0] + vy * square_size, player.pos[1] - vx * square_size])
        
    # wall_front, wall_left, wall_right = wall_distance(player.pos, player.direction)

    layer_input = np.array([b_front, b_left, b_right, dxp, dyp])
    active_layer = layer_input

    for i in range(len(player.weights) - 1):
        active_layer = np.maximum(0, np.dot(active_layer, player.weights[i]))

    final_output = np.dot(active_layer, player.weights[-1])
    action = np.argmax(final_output)

    if action == 0:      # STRAIGHT
        return (vx, vy)

    elif action == 1:    # LEFT
        return (-vy, vx)

    elif action == 2:    # RIGHT
        return (vy, -vx)
    
def mutate(weights, strength, mutation_rate):
    new_weights = []
    for w in weights:
        noise = np.random.normal(0, strength, w.shape)
        w_new = w + noise * (np.random.rand(*w.shape) < mutation_rate)
        new_weights.append(w_new)
    return new_weights

def next_gen(ai_pop_size, data, mutation = False, weights = []):
    global top_scores
    new_gen = []
    if not data :
        return [AI(weights) for i in range(ai_pop_size)]
    
    top10 = ai_pop_size // 10 
    best_ai = sorted(data, key=lambda x: x[0], reverse=True)[:top10]
    top_scores.append([score[0] for score in best_ai[:50]])

    for i in range(top10) :
        ai = best_ai[i]
        rate = i / (top10-1)

        for j in range(ai_pop_size//top10):
            if mutation : 
                weights = mutate(ai[1], 0.2*rate, 0.5*rate)
            else : 
                weights = ai[1]
            new_gen.append(AI(weights))

    data.clear()
    return new_gen

def play_game(ai_s, screen, clock):
    for ai in ai_s:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            new_direction = move_neural(ai)
            if (new_direction[0] != -ai.direction[0]) and (new_direction[1] != -ai.direction[1]):
                ai.direction = new_direction

            if (ai.score == number_of_squares):
                ai.game_over()
            ai.move()
            ai.value -= 1

            if not ai.alive:
                running = False

            ai.draw(screen)
            pygame.display.flip()
            clock.tick(10)

def ai_game(ai_s):
    any_snake_alive = True
    while any_snake_alive:
        any_snake_alive = False
        for ai in ai_s:

            if not ai.alive: 
                continue

            any_snake_alive = True

            new_direction = move_neural(ai)

            if (new_direction[0] != -ai.direction[0]) and (new_direction[1] != -ai.direction[1]):
                ai.direction = new_direction

            ai.move()
            ai.value -= 1

def train(ai_pop_size, gens, weights = []): # data = [score, weights] ; weights = [w1,w2] expandable ??
    if weights == []:
        for i in range(gens):
            print("gen :", i)         
            ai_game(next_gen(ai_pop_size, data, True))
    else :
        print("Training with old weights")
        ai_game(next_gen(ai_pop_size, data, False, weights))
        for i in range(gens):
            print("gen :", i)
            ai_game(next_gen(ai_pop_size, data, True))


    pygame.init()
    screen = pygame.display.set_mode((max_x, max_y))
    pygame.display.set_caption("SNAKKKKKKE")
    clock = pygame.time.Clock()

    max_history = [gen[0] for gen in top_scores]
    avg_history = [sum(gen)/len(gen) for gen in top_scores]

    plt.plot(max_history, label="Best Snake")
    plt.plot(avg_history, label="Top 50 Average")
    plt.xlabel("Generation")
    plt.ylabel("Score")
    plt.legend() 
    plt.savefig(f"training_logs/pop_size_{ai_pop_size}_number_of_gens_{gens}.png")
    plt.show()

    top_weights = sorted(data, key=lambda x: x[0], reverse=True)[0]
    best_ai = AI(top_weights[1])
    
    folder = 'training_logs'
    filename = 'best_ai.npz'

    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.join(folder, filename)

    np.savez(path, w1 = top_weights[1][0], w2 = top_weights[1][1])
