import pygame
import pygame.math as pymath
import math



class Planet(pygame.sprite.Sprite):

    planetGroup = pygame.sprite.Group() # group with all planets in it
    GRAVITYMULTIPLIER = 10000 # Gravitational constant

    def __init__(self, name, x, y, radius, density, color, WIN : pygame.surface.Surface, velocity = pymath.Vector2(0,0)):
        """
        :param name: Name of the planet
        :param x: x coordinate of the center of the planet
        :param y: y coordinate of the center of the planet
        :param radius: Radius of the planet
        :param density: Density of the planet
        :param color: Color of the planet for display
        :param WIN: Window the planet is in
        :param velocity: The initial velocity of the planet
        """
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.radius = radius
        self.surface = pygame.Surface([2*radius, 2*radius])
        self.rect = pygame.Rect(x - self.radius, y - self.radius, 2*self.radius, 2*self.radius)
        self.WIN = WIN
        self.density = density
        self.color = color
        self.velocity = velocity
        self.mass : float
        self.getMass()
        self.add(Planet.planetGroup)



    # ---------- PARAMETERS --------
    def getMass(self) -> None:
        """
        Calculates the mass of the planet and sets self.mass to it
            Assumes uniferm density
        :return: None
        """
        volume = ((math.pi * (self.radius*10000000)**3)*4)/3
        self.mass = volume*self.density

    def getX(self) -> float:
        """
        Returns x coordinate of the center of the planet
        :return: float
        """
        return self.rect.x + self.radius

    def getY(self) -> float:
        """
        Returts y coordinate of the center of the planet
        :return: float
        """
        return self.rect.y + self.radius

    # ---------- MOVEMENT ---------
    # Note: in PyGame, the positive Y direction is down, and the negative is up
    def move(self) -> None:
        """
        Moves the planet based on its velocity and draws it on the Window
        :return: None
        """

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        #d raws the planet
        pygame.draw.circle(self.WIN, self.color, (self.getX(), self.getY()), self.radius)


    # ---------- PHYSISCS ---------

    def applyForce(self, magnitude : float, angle : float, name) -> None:
        """
        Takes magnitude of the force and angle at which to apply it (in radians)
            and applies it
        :param magnitude: Magnitude of the force
        :param angle: Angle between source and object of the force (radians)
        :param name: Name of the planet applying the force
        :return: None
        """

        force = pymath.Vector2(magnitude, 0)#creates force vector
        if force.length() >= 0.00000001:
            force.rotate_ip_rad(angle)
            force.scale_to_length(force.length())

        self.velocity.x += force.x
        self.velocity.y -= force.y


    def gravity(self):
        """
        Exerts gravity upon the object from all other planets
        :return: None
        """
        planet: Planet  # planet applying the force
        planetlist = Planet.planetGroup.sprites()  # list of all planets, including itself
        planetlist.remove(self)

        for planet in planetlist:
            #calculates the distance between the centers of the 2 planets
            distance = math.sqrt((planet.getX() + self.getX()) ** 2 + ((planet.getY() + self.getY()) ** 2))

            #calculates the magnitude of the force using a modified Universal Gravitation equation
            force = (Planet.GRAVITYMULTIPLIER * planet.mass/self.mass) / distance**2

            #calculates angle between the 2 planets in radians
            angle = math.atan2(-(planet.getY() - self.getY()), planet.getX() - self.getX())
            self.applyForce(force, angle, planet.name)


    #---------- DISPLAY --------
    def update(self) -> None:
        """
        Updates the planet each frame
        :return: None
        """
        self.gravity()
        self.move()
