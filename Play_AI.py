import V3
import numpy as np
import pygame

#V3.train(1000,200)

file = './training_logs/best_ai.npz'
data = np.load(file)

w1 = data['w1']
w2 = data['w2']

for key in data.files:
    print(f"Layer Name: {key} | Shape: {data[key].shape}")


pygame.init()
screen = pygame.display.set_mode((V3.max_x, V3.max_y))
pygame.display.set_caption("SNAKKKKKKE")
clock = pygame.time.Clock()
clock.tick(1000)
best_ai = V3.AI([w1,w2])
best_ai = [best_ai]

V3.play_game(best_ai, screen, clock)