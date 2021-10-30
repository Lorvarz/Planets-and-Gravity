import pygame
import pygame.math as pymath
from planet import Planet


#creates the window and names it
WIDTH, HEIGHT = 1000, 660
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planets and Gravity")

#initiates the font
pygame.font.init()
parameterFont = pygame.font.SysFont("comicsans", 30)


#creates a bunch of colors for later use
aquaGreen = (0,192,163)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
GREY = (169,169,169)
PINK = (255, 192, 203)

#sets the FPS
FPS = 60



def drawWindow(earth, moon) -> None:
    """
    Draws all items in the window and updates it
    :param earth: The Earth object
    :param moon: The moon object
    :return: None
    """
    WIN.fill(WHITE) #draws white background

    #prints the current gracity multiplier
    WIN.blit(parameterFont.render(f"Gravity multiplier: {Planet.GRAVITYMULTIPLIER / 10000}", True, (0,0,0)), (10,10))



    earth.move() # moves the earth without calling gravity on it
    moon.update() # updates the moon


    pygame.display.update() # draws all changes onto the window

def mainLoop() -> None:
    """
    Runs main simulation loop
    :return: None
    """

    Planet.planetGroup.empty() # empties the list of planets
    Planet.GRAVITYMULTIPLIER = 10000 #sets default Gravitational Constant

    earth = Planet("earth", WIDTH/2 , HEIGHT/2 , 66, 5.51, aquaGreen, WIN) #creates the earth object
    moon = Planet("moon", WIDTH/2, HEIGHT/2 +150 , 17, 3.34, GREY, WIN, pymath.Vector2(10, 0)) #creates the moon object

    clock = pygame.time.Clock() #creates FPS Clock

    WIN.fill(WHITE)

    run = True # determines whether to run the loop
    draw = True # determines whether to keep updating Frames
    while run: #simulation loop
        clock.tick(FPS) #regulates FPS

        # ------------------ EVENTS ----------------------
        for event in pygame.event.get():

            #Quits the game when closing the window
            if event.type == pygame.QUIT:
                run = False

            #       *KEY EVENTS*
            if event.type == pygame.KEYDOWN:

                #draws one frame (regardless of draw variable)
                #Note: can be used to go frame by frame if time is stopped
                if event.key == pygame.K_LSHIFT:
                    drawWindow(earth, moon)

                #Restarts the program
                if event.key == pygame.K_RSHIFT:
                    mainLoop()

                #Stops simulation time
                if event.key == pygame.K_SPACE:
                    draw = not draw


        keys = pygame.key.get_pressed()

        #Up and down arrows to increase or decreate gravitation constant
        if keys[pygame.K_UP]:
            Planet.GRAVITYMULTIPLIER += 100
        if keys[pygame.K_DOWN]:
            Planet.GRAVITYMULTIPLIER -= 100



        if draw: #decides whether to draw
            drawWindow(earth, moon)

    pygame.quit() #quits the game


if __name__ == '__main__':
    mainLoop()