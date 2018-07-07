import pygame
import random
import time
import os
import shutil

WIDTH = 700
HEIGHT = 400
POINTS = 7
POINTS_PER_FRAME = 1
EXPORT_VIDEO = False
FPS = 60

colors = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255),(255,255,255)]
results = [0]*POINTS
totalTrials = 0.0

if __name__ == '__main__':
        pygame.init()
        screen = pygame.display.set_mode((int(WIDTH), int(HEIGHT)))

        done = False
        pointsPerFrame = 1
        i = 0

        if not os.path.exists("screenshots"):
                os.makedirs("screenshots")

        while not done:
                print "Frame " + str( int(i) )

                start_time = time.time()

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                done = True
                if done:
                                break

                for p in range(POINTS_PER_FRAME):
                    results[random.randint(0,POINTS-1)] += 1
                    totalTrials += 1.0

                pygame.draw.rect(screen, (0,0,0), (0,0,WIDTH,HEIGHT))
                for p in range(POINTS):
                    pygame.draw.rect(screen, colors[p], ((WIDTH/POINTS)*p,HEIGHT*(1-(results[p]/totalTrials)),(WIDTH/POINTS),HEIGHT))
                pygame.display.flip()

                time.sleep(1.0/FPS)

                time_elapsed = time.time() - start_time
                fps = 1.0 / time_elapsed
                print str( round(fps, 2) ) + " FPS"
                if EXPORT_VIDEO == True:
                        pygame.image.save(screen, "screenshots/screenshot_" + str("%06d" % int(i)) + ".bmp")

                i += 1

        if EXPORT_VIDEO == True:
                os.system("ffmpeg -r " + str(FPS) + " -i screenshots/screenshot_%06d.bmp -vcodec libx264 -y movie.mp4")
                shutil.rmtree("screenshots")

