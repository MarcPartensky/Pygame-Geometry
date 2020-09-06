#!/usr/bin/env python
from pygame_geometry import abstract
from pygame_geometry import colors
from pygame_geometry import context
from pygame_geometry.events import Manager, on
import pygame

class Game(Manager):
    """Demo class."""

    def __init__(self, context):
        """Create a game which only state is a one dimensional position x."""
        super().__init__(context)
        self.circle = abstract.Circle(0, 0, radius=1, area_color=colors.GREEN, fill=True)

    def start(self):
        """Start message that tells what are the controls available."""
        super().start()
        self.help(self)

    def show(self):
        """Show a circle."""
        super().show()
        self.circle.show(self.context)
    
    @on.press(pygame.KEYDOWN, pygame.K_h)
    def help(self):
        """Show the controls."""
        self.context.console.clear()
        self.context.console(f"Available controls:")
        for control in self.controls:
            self.context.console(control)

    @on.press(pygame.KEYDOWN, pygame.K_LEFT)
    def left(self):
        """Go left when left key is pressed."""
        self.circle.x -= 1

    @on.press(pygame.KEYDOWN, pygame.K_RIGHT)
    def right(self):
        """Go right when right key is pressed."""
        self.circle.x += 1

    @on.press(pygame.KEYDOWN, pygame.K_SPACE)
    def color_circle(self):
        """Print the position in the console."""
        self.circle.area_color = colors.reverse(self.circle.area_color)
        print(self.circle.area_color)

    @on.press(pygame.KEYDOWN, pygame.K_f)
    def fill(self):
        """Print the position in the console."""
        self.circle.fill = not self.circle.fill

    @on.press(pygame.KEYDOWN, pygame.K_ESCAPE)
    def escape(self):
        """Escape the game."""
        self.quit()

context = context.Context(name='Test Controller')
game = Game(context)
game()
