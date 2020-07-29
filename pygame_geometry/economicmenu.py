from . import colors
from pygame.locals import *

import pygame

class Button(Rect):
    """Button using pygame and colors.
    No properties are used for the surface,
    the background nor the font in this class."""
    def __init__(self,
                text="button",
                position=(0,0),
                size=(300,50),

                police="monospace",
                text_size=50,
                bold=False,
                italic=False,

                default_background=colors.WHITE,
                hovered_background=colors.GREEN,
                focused_background=colors.BLUE,
                clicked_background=colors.RED,

                default_color=colors.BLACK,
                hovered_color=None,
                focused_color=None,
                clicked_color=None,

                action=None):
        """Create a button."""
        self.text = text

        self.police = police
        self.text_size = text_size
        self.bold = bold
        self.italic = italic

        self.default_background = default_background
        self.hovered_background = hovered_background
        self.focused_background = focused_background
        self.clicked_background = clicked_background

        self.default_color = default_color
        self.hovered_color = hovered_color
        self.focused_color = focused_color
        self.clicked_color = clicked_color

        self.hovered = False
        self.focused = False
        self.clicked = False

        super().__init__(position,size)

        self.refresh()

    def __contains__(self,position):
        """Determine if a point is within the button."""
        return self.collidepoint(position)

    def getFont(self):
        """Return a font."""
        return pygame.font.SysFont(self.police,self.text_size,self.bold,self.italic)

    def getColor(self):
        """Return the color."""
        if self.clicked and (self.clicked_color is not None):
            return self.clicked_color
        elif self.focused and (self.focused_color is not None):
            return self.focused_color
        elif self.hovered and (self.hovered_color is not None):
            return self.hovered_color
        else:
            return self.default_color

    def getBackground(self):
        """Return the background."""
        if self.clicked and (self.clicked_background is not None):
            return self.clicked_background
        elif self.focused and (self.focused_background is not None):
            return self.focused_background
        elif self.hovered and (self.hovered_background is not None):
            return self.hovered_background
        else:
            return self.default_background

    def getSurface(self):
        """Return a surface."""
        fsurface=self.font.render(self.text,True,self.color)
        surface=pygame.Surface(self.size)
        sx,sy=surface.get_size()
        sfx,sfy=fsurface.get_size()
        background=self.getBackground()
        if background is not None:
            if self.isColor(background):
                surface.fill(background)
            else:
                background=pygame.transform.scale(background,surface.get_size())
                surface.blit(background)
        surface.blit(fsurface,((sx-sfx)//2,(sy-sfy)//2))
        return surface

    def getPosition(self):
        """Return the position of the button."""
        return (self.left,self.top)

    def setPosition(self,position):
        """Set the position of the button."""
        x,y=position
        sx,sy=self.size
        self.center=x+sx//2
        self.center=y+sy//2

    def onClick(self):
        """Execute an action."""
        if self.action is not None:
            self.action()

    def reset(self):
        """Reset the button."""
        self.hovered=False
        self.focused=False
        self.clicked=False

    def refresh(self):
        """Recreate the main components of the button:
        font, color, background, surface."""
        self.font=self.getFont()
        self.color=self.getColor()
        self.surface=self.getSurface()

    def update(self,position,click,focus,select):
        """Update a button."""
        self.focused=focus
        if position in self:
            self.hovered=True
            if click:
                self.focused=True
                self.clicked=True
            else:
                self.clicked=False
        else:
            self.hovered=False
        if select:
            if focus:
                self.clicked=True

    def isColor(self,object):
        """Determine if an object is a color."""
        if type(object)==tuple:
            if len(object)==3:
                for i in range(3):
                    if not (0<=object[i]<256):
                        return False
                return True
            else:
                return False
        else:
            return False


    position=property(getPosition,setPosition)


class Page(Rect):
    """Page using pygame, colors and window."""
    def __init__(self,size,buttons=[],position=(0,0),background=None):
        """Create a page."""
        self.buttons=buttons
        self.focus=None
        self.select=False
        self.background=background
        super().__init__(position,size)
        self.refresh()
        self.spreadVerticalButtons()

    def isColor(self,object):
        """Determine if an object is a color."""
        if type(object) == tuple:
            if len(object) == 3 or len(object) == 4:
                for i in range(len(object)):
                    if not (0 <= object[i] < 256):
                        return False
                return True
            else:
                return False
        else:
            return False

    def spreadVerticalButtons(self):
        """Spread the buttons on the vertical evenly."""
        l=len(self.buttons)
        sx,sy=self.surface.get_size()
        uy=sy//l
        mx=sx//2
        for i in range(l):
            self.buttons[i].center=(mx,uy*(i+1/2))

    def spreadHorizontalButtons(self):
        """Spread the buttons on the horizontal evenly."""
        l=len(self.buttons)
        sx,sy=self.surface.get_size()
        ux=sx//l
        my=sy//2
        for i in range(l):
            self.buttons[i].center=(ux*(i+1/2),my)

    def showButtons(self):
        """Show the buttons on the surface."""
        for button in self.buttons:
            self.surface.blit(button.surface,button.position)

    def __call__(self,window):
        """Execute the main loop with the window."""
        while window.open:
            self.events(window)
            self.update(window)
            self.refresh()
            self.show(window)
            window.flip()

    def events(self,window):
        """Deal with the events."""
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                window.open = False
                return

            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    window.open = False
                    return

                if event.key == K_DOWN or event.key == K_RIGHT:
                    if self.focus is not None:
                        self.focus = (self.focus+1) % len(self.buttons)
                    else:
                        self.focus=0
                if event.key == K_UP or event.key == K_LEFT:
                    if self.focus is not None:
                        self.focus = (self.focus-1) % len(self.buttons)
                    else:
                        self.focus=0

            if event.type == MOUSEMOTION:
                self.motion = True
            else:
                self.motion = False


    def update(self,window):
        """Update the page."""
        self.cursor = window.point()
        self.click = window.click()
        keys = window.press()
        self.select = bool(keys[K_RETURN]) or bool(keys[K_SPACE])
        self.setFocus()
        self.resetButtons()
        self.updateButtons()

    def refresh(self):
        """Refresh the page and the buttons."""
        self.refreshPage()
        self.refreshButtons()

    def refreshPage(self):
        """Refresh the surface and the background of the page."""
        self.surface=self.getSurface()

    def refreshButtons(self):
        """Refresh the buttons."""
        for button in self.buttons:
            button.refresh()

    def setFocus(self):
        """Set the focus using the motion."""
        if self.motion or self.click:
            for i in range(len(self.buttons)):
                if self.cursor in self.buttons[i]:
                    self.focus = i

    def resetButtons(self):
        """Reset all the buttons."""
        for i in range(len(self.buttons)):
            self.buttons[i].reset()

    def updateButtons(self):
        """Update a button."""
        for i in range(len(self.buttons)):
            focus = bool(self.focus == i)
            self.buttons[i].update(self.cursor,self.click,focus,self.select)

    def show(self,window):
        """Show the page by showing its components."""
        self.showSurface(window)
        self.showButtons(window)
        window.flip()

    def showSurface(self,window):
        """Show the surface."""
        window.screen.blit(self.surface,self.position)

    def showButtons(self,window):
        """Show the buttons of the page."""
        for i in range(len(self.buttons)):
            window.screen.blit(self.buttons[i].surface,self.buttons[i].position)

    def getSurface(self):
        """Return the surface of the page."""
        surface = pygame.Surface(self.size)
        if self.background is not None:
            if self.isColor(self.background):
                surface.fill(self.background)
            else:
                background = pygame.transform.scale(self.background,self.size)
                surface.blit(background)
        return surface

    def getPosition(self):
        """Return the position of the button."""
        return (self.left,self.top)

    def setPosition(self,position):
        """Set the position of the button."""
        x, y = position
        sx, sy = self.size
        self.center = x + sx//2
        self.center = y + sy//2

    position = property(getPosition)



"""

def action1():
    pass

def action2():
    pass

def action3():
    pass

actions={
    "key_action1":action1,
    "key_action2":action2,
    "key_action3":action3
}



tree={
    "key_page1":{
        "key1" : "action1",
        "key2" : "action2",
        "key3" : ""
    }
    "key_page2":{
        "key1": "key_action3",
        "key2": ""
    }
}


def action1():
    othello.plateau.grille=[]

buttons =  {   1 : "Start",
                11 : "Lancer",
                12 : "Joueur blanc",
                    121 : "Humain",
                    122 : "Cyrano",
                    123 : "Retour vers joueur blanc",
                13 : "Joueur noir",
                    131 : "Humain",
                    132 : "Cyrano",
                    133 : "Retour vers joueur noir",
                14 : "Retour vers start",
            2 : "Option",
                21 : "Activer l'aide au mouvement", # cliquer sur ce bouton fait alterner un bouléen
                22 : "Retour vers option",
            3 : "Quitter" # cliquer ferme la fenetre
        }
}


interactions_buttons={
    "Humain" : choisirJoueurBlancHumain,
    "Cyrano" :
}




pages={
    "page1":Page
    "page2":Page()
}

interactions = {
    "page1":{
        "Start" : clé page 2;
        "Option" : clé page ;
        "Quitter" : fermer la fenetre };

    "page2":{

    }

}







"""

class Menu:

    def createFromButtonsHierarchy(buttons):
        """Create a page from a buttons dictionary."""

        return Menu(pages,interactions)

    def __init__(self,pages,tree,actions):
        """Create a menu."""
        self.pages=pages #Dictionary
        self.tree=tree
        self.key=key

    def __call__(self,window):
        """Load the page of key 'key'."""
        while window.open:
            self.page.events(window)
            self.page.update(window)
            self.update()
            self.refresh()
            self.page.show(window)
            window.screen.blit(self.page.surface,(0,0))
            window.flip()


    def update(self):
        """Update the menu after updating the page and its buttons in order to
        take an action."""
        button_key=self.checkButtons()
        if button_key is not None:
            self.tree[self.key]



    def checkButtons(self):
        """Check if the buttons are being clicked."""
        for i in range(len(self.page.buttons)):
            if self.page.buttons[i].clicked:
                return i

        key_action=self.tree[self.key]
        action=self.actions[key_action]
        action()

    def getPage(self):
        """Return the current page."""
        return self.pages[self.key]


    page=property(getPage)


if __name__=="__main__":
    from .window import Window
    window=Window("Page")
    buttons=[Button(t) for t in ["oui","non","peut etre","pourquoi pas"]]
    page=Page(window.size,buttons)
    page(window)
