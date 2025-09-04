#entity

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from physics_object import PhysicsObject, Vector3


# Player Entity
class Player(PhysicsObject):
    """The player character represented as a blue cube."""
    def __init__(self, position, velocity, width=1.0, height=2.0, depth=1.0):
        super().__init__(position, velocity, width, height, depth)
        self.color = (0.0, 0.0, 1.0)  # Blue

    def render(self):
        glPushMatrix()
        glScalef(self.width, self.height, self.depth)
        glutSolidCube(1)
        glPopMatrix()


# Floor Entity
class Floor(PhysicsObject):
    """Large green ground for the farm."""
    def __init__(self, position, width=50.0, height=1.0, depth=50.0):
        super().__init__(position, Vector3(0, 0, 0), width, height, depth)
        self.color = (0.2, 0.8, 0.2)  # Green ground

    def render(self):
        glPushMatrix()
        glScalef(self.width, self.height, self.depth)
        glutSolidCube(1)
        glPopMatrix()


# Building (Farmhouse)
class Building(PhysicsObject):
    """A simple farmhouse with cube base and triangular roof."""
    def __init__(self, position, width=5, height=5, depth=5):
        super().__init__(position, Vector3(0, 0, 0), width, height, depth)
        self.wall_color = (0.6, 0.3, 0.0)  # Brown walls
        self.roof_color = (0.8, 0.0, 0.0)  # Red roof

    def render(self):
        # Base walls
        glPushMatrix()
        glScalef(self.width, self.height, self.depth)
        glColor3f(*self.wall_color)
        glutSolidCube(1)
        glPopMatrix()

        # Roof (triangular prism, front + back)
        glPushMatrix()
        glTranslatef(0, self.height / 2, 0)
        glColor3f(*self.roof_color)
        glBegin(GL_TRIANGLES)

        # Front face
        glVertex3f(-self.width / 2, 0, self.depth / 2)
        glVertex3f(self.width / 2, 0, self.depth / 2)
        glVertex3f(0, self.height / 2, self.depth / 2)

        # Back face
        glVertex3f(-self.width / 2, 0, -self.depth / 2)
        glVertex3f(self.width / 2, 0, -self.depth / 2)
        glVertex3f(0, self.height / 2, -self.depth / 2)

        glEnd()
        glPopMatrix()


# Crop Entity
class Crop(PhysicsObject):
    """Crop with 3 growth stages (seed → sprout → harvest)."""
    def __init__(self, position, width=0.5, height=1.0, depth=0.5):
        super().__init__(position, Vector3(0, 0, 0), width, height, depth)
        self.stage = 0  # 0=seed, 1=sprout, 2=harvest

    def grow(self):
        if self.stage < 2:
            self.stage += 1

    def render(self):
        if self.stage == 0:  # Seed (sphere)
            glColor3f(0.5, 0.25, 0.0)  # Brown seed
            glutSolidSphere(0.2, 10, 10)

        elif self.stage == 1:  # Sprout (small green cylinder)
            glColor3f(0.0, 0.8, 0.0)
            glPushMatrix()
            glRotatef(-90, 1, 0, 0)  # Rotate to stand upright
            gluCylinder(gluNewQuadric(), 0.1, 0.1, self.height, 10, 10)
            glPopMatrix()

        elif self.stage == 2:  # Harvestable crop (yellow cylinder)
            glColor3f(1.0, 1.0, 0.0)
            glPushMatrix()
            glRotatef(-90, 1, 0, 0)
            gluCylinder(gluNewQuadric(), 0.15, 0.15, self.height, 10, 10)
            glPopMatrix()


