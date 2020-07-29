from .manager import Manager
from .entity import Entity
from .motion import Motion
from .group import Group
import numpy as np

import random


class EntityGroup(Group):
    """An entity group is a group of entities. Entity specific features are added."""

    @staticmethod
    def getCollided(group1, group2):
        """Determine the collisions between 2 groups."""
        collisions = []
        for e1 in group1:
            for e2 in group2:
                if (e1.position - e2.position).norm < e1.born + e2.born:
                    if e1.cross(e2):
                        collisions.append((e1, e2))
        return collisions

    @staticmethod
    def killOnCollision(group1, group2):
        """We suppose the entities of group1 and group2 alives."""
        for e1 in group1:
            for e2 in group2:
                if (e1.position - e2.position).norm < e1.born + e2.born:
                    if e1.cross(e2):
                        e1.die()
                        e2.die()

    @classmethod
    def randomOfType(cls, etype, n=0, **kwargs):
        """Create a group of n random entities of type 'etype'."""
        entities = [etype.random() for i in range(n)]
        return cls(*entities, **kwargs)

    @classmethod
    def randomOfTypes(cls, *types, n=0, **kwargs):
        """Create a group of n random entities of type a all of the given types."""
        class etype(*types):
            pass
        return cls.randomOfType(etype, **kwargs)

    @classmethod
    def random(cls, n=10, **kwargs):
        """Create n random entities."""
        entities = [Entity.random() for i in range(n)]
        return cls(*entities, **kwargs)

    @classmethod
    def randomWithSizeSparse(self, n, size, sparse, **kwargs):
        """Create a random group using the size and sparse parameters."""
        g = super().random(n, **kwargs)
        g.enlarge(size)
        g.spread(sparse)
        return g

    def __init__(self, *entities, alive=False, active=False, activate=False):
        """Create a entity group."""
        super().__init__(*entities)
        self.active = active
        self.alive = alive
        if activate:
            self.activate()

    # Binding the entities to the elements
    entities = property(Group.getElements, Group.setElements, Group.delElements)

    def randomEntity(self):
        """Return a random entity of the group."""
        chosen = []
        for entity in self.entities:
            if isinstance(entity, EntityGroup):
                chosen.append(entity.randomEntity())
            else:
                chosen.append(entity)
        return random.choice(chosen)

    def spawn(self):
        """Spawn each entity."""
        self.alive = True
        for entity in self:
            entity.spawn()

    def updateActivation(self):
        """Determine if the group is active if any of the entities is active."""
        self.active = False
        for entity in self:
            if entity.active:
                self.active = True

    def activate(self):
        """Reactivate all entities."""
        self.active = True
        for entity in self:
            entity.activate()

    def deactivate(self):
        """Deactivate all entities."""
        self.active = False
        for entity in self:
            entity.deactivate()

    def reactKeyDown(self, key):
        """Make each entity react to the key down event."""
        for entity in self:
            if entity.active:
                entity.reactKeyDown(key)

    def reactMouseMotion(self, position):
        """Make each entity react to a mouse motion event."""
        for entity in self:
            if entity.active:
                entity.reactMouseMotion(position)

    def reactMouseButtonDown(self, button, position):
        """Make all entities react to a mouse button down event."""
        for entity in self:
            if entity.active:
                entity.reactMouseButtonDown(button, position)

    def respawn(self):
        """Respawn all dead entities."""
        for entity in self:
            entity.respawn()

    def clean(self):
        """Delete all dead entities."""
        i = 0
        while i < len(self):
            if self[i].alive:
                if isinstance(self[i], EntityGroup):
                    self[i].clean()
                i += 1
            else:
                del self[i]

    def show(self, context):
        """Show all entities."""
        for entity in self:
            entity.show(context)

    def showBorn(self, context):
        for entity in self:
            entity.showBorn(context)

    def __str__(self, name=None):
        """Return the str of the types of the entities."""
        if name is None:
            name = type(self).__name__
        return super().__str__(name)

    def update(self, dt):
        """Update all entities."""
        for entity in self:
            entity.update(dt)

    def setFriction(self, friction):
        """Set the friction of the entities to a given friction."""
        for entity in self:
            entity.setFriction(friction)

    def enlarge(self, n):
        """Enlarge the anatomies of the entities."""
        for entity in self:
            entity.enlarge(n)

    def spread(self, n):
        """Spread the bodies of the entities."""
        for entity in self:
            entity.spread(n)

    def control(self, controller):
        """Return the controlled entity using the controller."""
        # print(self[:])
        if len(controller) > 1:
            return self[controller[0]].control(controller[1:])
        else:
            return self[controller[0]]


class AliveEntityGroup:
    """Group of entities that handle themselves."""

    @classmethod
    def random(cls, n=5, np=3, nm=2, nv=2, dv=2):
        """Create a random entity group using the optional number of entities 'n'."""
        entities = [Entity.random(n=np, nm=nm, nv=nv, d=dv) for i in range(n)]
        entities = dict(zip(range(len(entities)), entities))
        return cls(entities)

    def __init__(self, entities):
        """Create a body group using the dictionary of entities."""
        self.entities = entities
        self.updateAlives()
        self.updateMaxBorn()

    def updateAlives(self):
        """Update the ids of alive entities."""
        self.alives = dict([(id, entity) for (id, entity)
                            in self.entities.items() if entity.alive])
        # Recurrent data that must be updated.
        # It is better to proceed that way for efficiency

    @property
    def deads(self):
        """Return the ids of dead entities."""
        return {k: v for k, v in self.entities.items() if k not in self.alives}

    def spawnEach(self):
        """Spawn each entity."""
        for entity in self.entities.values():
            entity.spawn()
        self.alives = self.entities.keys()

    def update(self, dt):
        """Update the group."""
        self.updateEach(dt)
        collisions = self.getCollisionsWithCircles()
        if len(collisions) > 0:
            collided = self.getCollided(collisions)
            if len(collided) != 0:
                self.killEach(collided)
                self.updateAlives()

    def updateEach(self, dt):
        """Update each entity alive."""
        for entity in self.alives.values():
            entity.update(dt)

    def showEach(self, context):
        """Show each entity alive."""
        for entity in self.alives.values():
            entity.show(context)

    def respawnDeads(self):
        """Respawn each dead entity."""
        for entity in self.deads.values():
            entity.respawn()

    def getCollisions(self):
        """Return the list of couples of collisions detected between alive entities."""
        collisions = []
        keys = list(self.alives.keys())
        n = len(keys)
        for i in range(n):
            for j in range(i + 1, n):
                id1 = keys[i]
                id2 = keys[j]
                e1 = self.alives[id1]
                e2 = self.alives[id2]
                if e1.cross(e2):
                    collisions.append((id1, id2))
        return collisions

    def getCollided(self, collisions):
        """Return the ids of collided entities."""
        ids = list(set(np.reshape(collisions, 2 * len(collisions))))
        return dict([(id, self.entities[id]) for id in ids])

    def killEach(self, collided):
        """Kill entities with their ids."""
        for entity in collided.values():
            entity.die()

    def spread(self, n=10):
        """Spread randomly the entities."""
        for entity in self.entities.values():
            entity.motion = n * Motion.random()

    def followEach(self, point):
        """Make each entity follow the point."""
        for entity in self.alives.values():
            entity.follow(point)

    def getMaxBorn(self):
        """Return the borns of all entities."""
        return self._max_born

    def updateMaxBorn(self, ):
        """Set the max born of all the entities."""
        self._max_born = max([e.born for e in self.alives.values()])

    def getCollisionsWithCircles(self):
        """Return all circle collisions."""
        collisions = []
        keys = list(self.alives.keys())
        n = len(keys)
        for i in range(n):
            for j in range(i + 1, n):
                id1 = keys[i]
                id2 = keys[j]
                e1 = self.alives[id1]
                e2 = self.alives[id2]
                if (e1.position - e2.position).norm < e1.born + e2.born:
                    if e1.cross(e2):
                        collisions.append((id1, id2))
        return collisions

    @property
    def alive(self):
        """Return true if any of the entity is alive."""
        return len(self.alives) != 0

    @property
    def dead(self):
        """Return true if all entities are dead."""
        return len(self.alives) == 0


class GroupManager(Manager):
    @classmethod
    def random(cls, **kwargs):
        """Create a random entity group."""
        group = EntityGroup.random(**kwargs)
        return cls(group)

    def __init__(self, group, **kwargs):
        """Create a body group manager using the group and optional arguments."""
        super().__init__(**kwargs)
        self.group = group

    def update(self):
        """Update the group."""
        collisions = self.group.getCollisions()
        collided = self.group.getCollided(collisions)
        self.group.killEach(collided)
        self.group.updateAlives()
        self.group.updateEach(self.dt)

    def show(self):
        """Show the group."""
        self.group.showEach(self.context)


class GroupTester(GroupManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.group.spread(100)
        self.following = True

    def update(self):
        """Update without collisions checks."""
        # self.group.updateEach(self.dt)
        self.updateWithCollisions()

    def updateWithCollisions(self):
        """Update the group."""
        self.group.followEach(self.context.point())
        collisions = self.group.getCollisionsWithCircles()
        if len(collisions) > 0:
            self.context.console.append(collisions)
            collided = self.group.getCollided(collisions)
            if len(collided) != 0:
                self.group.killEach(collided)
                self.group.updateAlives()
        self.group.updateEach(self.dt)


if __name__ == "__main__":
    # bm = SpaceShipTester.random(following=True, dt=0.1)
    # bm()
    # gt = GroupTester.random(n=50)
    # print(gt.group.alives)
    # gt()
    b1 = EntityGroup.random()
    b2 = EntityGroup.random()
    b1.enlarge(100)
    print(b1 + b2)


