#!/usr/bin/env python
"""The goal of this program is to ease up the use of events while doing functions.
This can be done by using decorators above functions. Each decorator could indicate
the event being detected."""

from . import context
import pygame


class Controller:
    """Controller which functions can be used as decorators
    to add controls to the manager."""

    def __init__(self):
        """Create an controller."""
        pass

    def press(self, type, key):
        """Decorator for pressing a key."""
        def decorator(action):
            return Control(Event(type, key=key), action)
        return decorator

class Event:
    """Representation of a pygame event."""
    def __init__(self, type, **value):
        """Create an event using its type and value."""
        self.type = type
        self.__dict__.update(value)

class Manager:
    """Base class of any simulation or game."""
    on:bool = True
    controls:list = []

    def __init__(self, context:Context):
        """Create a manager class."""
        self.context = context
        self.controls = Manager.controls
        self.on = Manager.on

    def add_controls(self):
        """Add the controls to the manager."""
        for function_name in dir(self):
            function = getattr(self, function_name)
            if isinstance(function, Control):
                self.controls.append(function)

    def loop_events(self):
        """Loop through all the events and controls."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            for control in self.controls:
                if control.event.type == event.type:
                    if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                        if control.event.key == event.key:
                            control.action(self)

    def main(self, *args, **kwargs):
        """Main function of the manager."""
        self.start()
        while self.on:
            self.loop()

    def start(self):
        """Start of the game."""
        self.add_controls()

    def loop(self):
        """Main loop of the game."""
        self.loop_events()
        self.show()
        self.update()

    def show(self):
        """Show the manager window."""
        self.context.flip()
        self.context.clear()

    def update(self):
        """Update the manager state."""

    def __call__(self, *args, **kwargs):
        """Call the main loop and start the manager."""
        self.main(*args, **kwargs)

    def quit(self):
        """Quit the game."""
        self.on = False

class Control:
    def __init__(self, event, action):
        """Create a control using the event and the action function."""
        self.event = event
        self.action = action

    def __call__(self, *args, **kwargs):
        """Call the action function."""
        return self.action(*args, **kwargs)

on = Controller()

if __name__ == "__main__":
    # The following part is the demo part.
    # It shows users how to use the environment.

    from . import abstract
    from . import colors

    class Game(Manager):
        """Demo class."""

        def __init__(self, context):
            """Create a game which only state is a one dimensional position x."""
            super().__init__(context)
            self.circle = abstract.Circle(0, 0, radius=1, area_color=colors.GREEN, fill=True)

        def show(self):
            """Show a circle."""
            super().show()
            self.circle.show(self.context)

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

        @on.press(pygame.KEYDOWN, pygame.K_ESCAPE)
        def escape(self):
            """Escape the game."""
            self.quit()

    context = context.Context(name='Test Controller')
    game = Game(context)
    game()
