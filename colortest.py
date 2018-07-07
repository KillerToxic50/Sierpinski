import pygame
import math
import time

WIDTH = 700
HEIGHT = 400

def clamp (x, maximum, minimum):
    return min(minimum, max(maximum, x))

if __name__ == '__main__':
        pygame.init()
        screen = pygame.display.set_mode((int(WIDTH), int(HEIGHT)))

        for x in range(WIDTH):
            i = math.pi*(2.0*x/WIDTH)
            r = clamp(math.sin(i-(4.0*math.pi/4.0)),0,1)
            g = clamp(math.sin(i-(0.0*math.pi/4.0)),0,1)
            b = clamp(math.sin(i-(2.0*math.pi/4.0)),0,1)
            c = (r*255, g*255, b*255)
            pygame.draw.line(screen, c, (x, 0), (x, HEIGHT))
        pygame.display.flip()

        time.sleep(2)
