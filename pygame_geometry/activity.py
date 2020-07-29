from .group import Group
from .widgets import Button, Slider


class Component:
    made = 0

    def __init__(self, tag=None):
        if tag is None:
            tag = type(self).__name__ + str(type(self).made)
        self.tag = tag
        type(self).made += 1

    def show(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def onKeyDown(self, key):
        pass

    def onKeyUp(self, key):
        pass

    def onMouseMotion(self, position):
        pass

    def onMouseButtonDown(self, button, position):
        pass


class ComponentGroup(Component, Group):
    def __init__(self, *components, tag=None):
        Component.__init__(self, tag)
        Group.__init__(self, *components)

    def show(self, context):
        for element in self:
            element.show(context)

    def update(self, dt):
        for element in self:
            element.update(dt)

    def onKeyDown(self, key):
        for element in self:
            element.onKeyDown(key)

    def onKeyUp(self, key):
        for element in self:
            element.onKeyDown(key)

    def onMouseMotion(self, position):
        for element in self:
            element.onMouseMotion(position)

    def onMouseButtonDown(self, button, position):
        for element in self:
            element.onMouseButtonDown(button, position)


class Activity(ComponentGroup):
    """Base class Activity inspired from android studio."""
    pass


class WidgetActivity(Activity):
    def __init__(self, widget_group, *args):
        super().__init__(widget_group, *args)

    def getWidgets(self):
        return self[0]

    def setWidgets(self, widgets):
        self[0] = widgets

    widgets = property(getWidgets, setWidgets)


class WidgetGroup(ComponentGroup):
    def __init__(self, widgets):
        super().__init__()
        self.widgets = widgets


if __name__ == "__main__":
    # c1 = Component()
    # c2 = Component()
    # print(c1.tag, c2.tag)

    wg = WidgetGroup(Button.random("test"))
    a = Activity([wg])