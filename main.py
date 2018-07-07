import pygame
import numpy as np
import random
import time
import os
import shutil
from sys import argv
from vector import *

WIDTH = 600
HEIGHT = 600
SCALE = 1
POINTS = 3
SCALER = 0.5
POINTS_PER_FRAME = 100 #(WIDTH*HEIGHT)/10
COLOUR_STEPS = 100
POINT_SIZE = 2
FANCY_COLOUR = False
TIME_SCALE = False
DEBUG = False
EXPORT_VIDEO = False
FPS = 60
FRAMES = 1000

def polygon (numSides):
        out = [Vector3(0,0,0)]*numSides
        ia = (2*np.pi)/numSides
        for n in range(numSides):
                y = 1.0-np.cos(ia*n)*((HEIGHT/2)-2)
                x = np.sin(ia*n)*((WIDTH/2)-2)
                out[n] = Vector3(x+(WIDTH/2),y+(HEIGHT/2),0)
        return out

def main ():
        pygame.init()
        screen = pygame.display.set_mode((int(WIDTH*SCALE), int(HEIGHT*SCALE)))
        foreground = pygame.surface.Surface((int(WIDTH*SCALE), int(HEIGHT*SCALE)), pygame.SRCALPHA, 32)
        background = pygame.surface.Surface((int(WIDTH*SCALE), int(HEIGHT*SCALE)), pygame.SRCALPHA, 32)
        foreground.fill((0,0,0,0))
        background.fill((0,0,0,0))

        global WIDTH
        global HEIGHT
        global SCALE
        global POINTS
        global SCALAR
        global POINTS_PER_FRAME
        global COLOUR_STEPS
        global POINT_SIZE
        global FANCY_COLOUR
        global TIME_SCALE
        global DEBUG
        global EXPORT_VIDEO
        global FPS
        global FRAMES

        points = polygon(POINTS)
        lineScaler = SCALER

        currentPosition = points[random.randint(0,len(points)-1)]
        numPlots = [[0 for x in range(WIDTH)] for y in range(HEIGHT)] 

        done = False
        pointsPerFrame = 1
        frame = 1
        i = 1

        if not os.path.exists("screenshots"):
                os.makedirs("screenshots")

        if DEBUG:
                for p in points:
                        x = p.x
                        y = p.y
                        for y2 in range(-POINT_SIZE/2,POINT_SIZE/2):
                                        for x2 in range(-POINT_SIZE/2,POINT_SIZE/2):
                                                foreground.set_at((int((x*SCALE)+x2), int((y*SCALE)+y2)), (255,255,255))
                        screen.blit(background, (0,0))
                        screen.blit(foreground, (0,0))
                        pygame.display.flip()
        else:
                POINT_SIZE = 1

        if TIME_SCALE:
                time.sleep(1)
                for f in range(FPS/2):
                        if EXPORT_VIDEO:
                                pygame.image.save(screen, "screenshots/screenshot_" + str("%06d" % int(frame)) + ".bmp")
                        frame += 1

        while not done:
                print "Frame " + str( int(frame) )
                start_time = time.time()

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                done = True
                if done:
                                break

                for f in range(pointsPerFrame):
                        line = scale(points[random.randint(0,len(points)-1)] - currentPosition, lineScaler)
                        newPosition = currentPosition + line
                        x = int(newPosition.x)
                        y = int(newPosition.y)
                        numPlots[y][x] += 1.0
                        if FANCY_COLOUR:
                                j = np.pi*(2.0*numPlots[y][x]/COLOUR_STEPS)
                                r = np.sin(j-(4.0*np.pi/4.0))
                                g = np.sin(j-(0.0*np.pi/4.0))
                                b = np.sin(j-(2.0*np.pi/4.0))
                                c = (r*255, g*255, b*255)
                        else:
                                #c = (numPlots[y][x],numPlots[y][x],numPlots[y][x])
                                c = (0,255,255)
                        c = (np.clip(c[0], 0, 255), np.clip(c[1], 0, 255), np.clip(c[2], 0, 255))

                        if DEBUG:
                                pygame.draw.line(background, (16,16,16), (int(currentPosition.x*SCALE), int(currentPosition.y*SCALE)), (x*SCALE, y*SCALE))

                        for y2 in range(SCALE):
                                        for x2 in range(SCALE):
                                                for y3 in range(-POINT_SIZE/2,POINT_SIZE/2):
                                                        for x3 in range(-POINT_SIZE/2,POINT_SIZE/2):
                                                                foreground.set_at((int((x*SCALE)+x2+x3), int((y*SCALE)+y2+y3)), c)
                        currentPosition = newPosition

                screen.blit(background, (0,0))
                screen.blit(foreground, (0,0))
                pygame.display.flip()

                if TIME_SCALE:
                        if i < 200:
                                if EXPORT_VIDEO == False:
                                        time.sleep(1.0/i)
                        else:
                                pointsPerFrame = int(POINTS_PER_FRAME*((1.0*i-200)/(1.0*FRAMES-200)))
                                print pointsPerFrame
                                if EXPORT_VIDEO == False:
                                        time.sleep(1.0/FPS)
                else:
                        pointsPerFrame = POINTS_PER_FRAME

                time_elapsed = time.time() - start_time
                fps = 1.0 / time_elapsed
                print str( round(fps, 2) ) + " FPS"
                if EXPORT_VIDEO:
                        if TIME_SCALE and i < 200:
                                for f in range(int(FPS*1.0/i)+1):
                                        pygame.image.save(screen, "screenshots/screenshot_" + str("%06d" % int(frame)) + ".bmp")
                                        frame += 1
                        else:
                                pygame.image.save(screen, "screenshots/screenshot_" + str("%06d" % int(frame)) + ".bmp")
                                frame += 1
                elif TIME_SCALE:
                        frame += int(FPS*1.0/i)+1
                else:
                        frame += 1
                
                if frame > FRAMES and EXPORT_VIDEO:
                        done = True

                i += 1
                                

        if EXPORT_VIDEO == True:
                os.system("ffmpeg -r " + str(FPS) + " -i screenshots/screenshot_%06d.bmp -vcodec libx264 -y movie.mp4")
                #shutil.rmtree("screenshots")

        
if __name__ == '__main__':
        # Create a dictionary for command line arguments
        opts = {}
        while argv:
                if argv[0][0] == '-':
                        try:
                                opts[argv[0]] = argv[1]
                        except:
                                opts[argv[0]] = 0
                argv = argv[1:]

        # Parse arguments
        if '-w' in opts:
                WIDTH =  int(opts['-w'])
        if '-q' in opts:
                HEIGHT =  int(opts['-q'])
        if '-s' in opts:
                SCALE =  int(opts['-s'])
        if '-n' in opts:
                POINTS =  int(opts['-n'])
        if '-l' in opts:
                SCALER =  float(opts['-l'])
        if '-c' in opts:
                FANCY_COLOUR = True
        if '-d' in opts:
                DEBUG = True
        if '-t' in opts:
                TIME_SCALE = True
        if '-r' in opts:
                POINT_SIZE = int(opts['-r'])
        if '-p' in opts:
                POINTS_PER_FRAME = int(opts['-p'])
        if '-v' in opts:
                EXPORT_VIDEO = True
                FRAMES = int(opts['-v'])
        if '-f' in opts:
                FPS =  float(opts['-f'])
        if '-h' in opts:
                print "\n --- Avaiable options: ---"
                print "-w - Set horizontal resolution of output"
                print "-h - Set vertical resoltion of output"
                print "-s - Set output resolution scale factor"
                print "-n - Set number of initial points"
                print "-l - Set line scalar used for calculating points"
                print "-p - Set number of points to plot per frame"
                print "-c - Enable frequency color gradient visualisation"
                print "-d - Enable drawing of initial points and show method lines, good for demos"
                print "-t - Enable increasing plot speed, good for demos"
                print "-r - Set size of points"
                print "-v - Enable video export and set length in frames"
                print "-f - Set FPS of exported video"
                exit()
        else:
                print "\n+---------------------------------------------+"
                print "| Run with -h for a list of available options |"
                print "+---------------------------------------------+\n"

        main()