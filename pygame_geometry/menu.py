from pygame.locals import *
from .rect import Rect
from . import colors

import pygame

class Button(Rect):
    """Button using pygame and colors."""
    def __init__(self,
                text="button",
                position=[0,0],
                size=[300,50],

                police="monospace",
                text_size=50,
                bold=False,
                italic=False,

                default_background_style=colors.WHITE,
                hovered_background_style=colors.GREEN,
                focused_background_style=colors.BLUE,
                clicked_background_style=colors.RED,

                default_text_style=colors.BLACK,
                hovered_text_style=colors.BLACK,
                focused_text_style=colors.BLACK,
                clicked_text_style=colors.BLACK,

                build=True):
        """Create a button."""
        super().__init__(position,size)

        self.text = text

        self.police = police
        self.text_size = text_size
        self.bold = bold
        self.italic = italic

        self.default_background_style = default_background_style
        self.hovered_background_style = hovered_background_style
        self.focused_background_style = focused_background_style
        self.clicked_background_style = clicked_background_style

        self.default_text_style = default_text_style
        self.hovered_text_style = hovered_text_style
        self.focused_text_style = focused_text_style
        self.clicked_text_style = clicked_text_style

        self.hovered = False
        self.focused = False
        self.clicked = False

        self.updateBackgroundSizes()
        if build: self.build()

    def build(self):
        """Buid a new surface."""
        self.surface=pygame.Surface(self.size)
        self.updateSurface()

    def getFont(self):
        """Return a font."""
        return pygame.font.SysFont(self.police,self.text_size,self.bold,self.italic)

    def getTextStyle(self):
        """Return the style of the text."""
        if self.clicked:
            return self.clicked_text_style
        elif self.focused:
            return self.focused_text_style
        elif self.hovered:
            return self.hovered_text_style
        else:
            return self.default_text_style

    def getBackgroundStyle(self):
        """Return the style of the background."""
        if self.clicked:
            return self.clicked_background_style
        elif self.focused:
            return self.focused_background_style
        elif self.hovered:
            return self.hovered_background_style
        else:
            return self.default_background_style

    def updateBackgroundSizes(self):
        """Set the sizes of the background surfaces if they exist."""
        if isinstance(self.clicked_background_style,pygame.Surface):
            pygame.transform.scale(self.clicked_background_style,self.size)
        if isinstance(self.focused_background_style,pygame.Surface):
            pygame.transform.scale(self.focused_background_style,self.size)
        if isinstance(self.hovered_background_style,pygame.Surface):
            pygame.transform.scale(self.hovered_background_style,self.size)
        if isinstance(self.default_background_style,pygame.Surface):
            pygame.transform.scale(self.default_background_style,self.size)

    def updateSurface(self):
        """Return the surface of the button."""
        sx,sy=self.size
        font_surface=self.font.render(self.text,True,self.text_style)
        sfx,sfy=font_surface.get_size()
        background_style=self.getBackgroundStyle()
        if isinstance(background_style,pygame.Surface):
            self.surface.blit(background_style)
        else:
            self.surface.fill(background_style)
        self.surface.blit(font_surface,((sx-sfx)//2,(sy-sfy)//2))

    def reset(self):
        """Reset the button."""
        self.hovered=False
        self.focused=False
        self.clicked=False

    def update(self,*args):
        """Update the button."""
        self.updateStates(*args)
        self.updateSurface()

    def updateStates(self,position,click,focus,select):
        """Update the states of the button."""
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

    def isColorStyle(self,object):
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


    font=property(getFont)
    text_style=property(getTextStyle)
    background_style=property(getBackgroundStyle)

class Page(Rect):
    """Page using pygame, colors and window."""
    def __init__(self,rect,buttons=[],background=None):
        """Create a page."""
        self.buttons=buttons
        self.focus=None
        self.select=False
        self.background=background
        cdn=Rect.getCoordinatesFromRect(rect)
        super().__init__(cdn[:2],cdn[2:])
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
        while window:
            self.events(window)
            self.update(window)
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
        self.updateStates(window)
        self.updateSurface()

    def updateStates(self,window):
        """Update the state of the page."""
        self.cursor = window.point()
        self.click = window.click()
        keys = window.press()
        self.select = bool(keys[K_RETURN]) or bool(keys[K_SPACE])
        self.setFocus()
        self.resetButtons()
        self.updateButtons()

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

    def showSurface(self,window):
        """Show the surface."""
        window.screen.blit(self.surface,(self.xmin,self.ymin))

    def showButtons(self,context):
        """Show the buttons of the page."""
        for i in range(len(self.buttons)):
            context.screen.blit(self.buttons[i].surface,self.buttons[i].position)

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


    surface=property(getSurface)



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
