#using pygame as main canvas
import pygame

#init pygame
pygame.init()

#create a window(could be full screen)

screen = pygame.display.set_mode(pygame.display.FULLSCREEN)


#Create a Master grid for simulating the results
gird = []

#Start defining the initial lines and transversal

class line:
    def __init__(self):
        pass

    def line(self,A=0,B=0):
        global grid
        grid.append([])
#Start defining the angles

class postulates:
    class converse:
        def __init__(self):
            pass

    def corresponding(self,A,B):





#Init the running bool
running = True


#Start the program

while True:
    #Get the event keys
    for event in pygame.event.get():
        #Mouse clicks


        #if quitting application
        if event == pygame.QUIT or running == False:
            exit(1)


    #Main Program

