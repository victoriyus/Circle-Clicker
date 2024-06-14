"""
Date: 06/14/2024
Name: Button Class
Description Button classes used in Circle Clicker
"""
# Imports pygame (Needs to be imported to work properly)
import pygame


class Button:
    def __init__(self, x, y, image, scale, surface):
        '''
        initializing the button
        '''
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale)))
        self.imageDimensions = [width * scale, height * scale]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False
        self.selected = False
        self.oldimage = False
        self.oldrectcenter = False
        self.surface = surface
        self.x = x
        self.y = y
        self.scale = scale

    def draw(self):
        '''
        Draws the button onto the screen
        '''

        # Draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, x, y):
        '''
        Moves the button
        '''

        self.rect.center = (x, y)

    def click(self):
        '''
        Detects if the button gets clicked
        '''
        action = False
        # hover = False

        # Getting the mouse position
        pos = pygame.mouse.get_pos()

        # Check if the mouse is hovering over or clicking the button
        if self.rect.collidepoint(pos):
            # hover = True

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        return action


class clickableButton(Button):

    def hover(self):
        '''
        Detects when the cursor is hovering over a button
        '''
        hover = False

        # Getting the mouse position
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):

            hover = True

        return hover


class gameButton(Button):

    def __init__(self, index, x, y, image, scale, surface):

        super().__init__(x, y, image, scale, surface)

        self.index = index
        self.broke_combo = False

    def has_broken_combo(self):
        '''
        Checks if the button has broken combo yet
        '''

        if not self.broke_combo:

            self.broke_combo = True

            return False

        return True
