from physics_object import PhysicsObject, Vector3
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


# Player Class
class Player(PhysicsObject):
    def __init__(self, position=Vector3(0, 0, 0), velocity=Vector3(0, 0, 0), width=1, height=1, depth=1):
        super().__init__(position, velocity, width, height, depth)
        self.color = (0.8, 0.8, 0.8)  # Color the player green

    def draw(self):
        glPushMatrix()
        
        # Translate the player to its position and apply rotation
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation.x, 1, 0, 0)  # Rotation on X axis
        glRotatef(self.rotation.y, 0, 1, 0)  # Rotation on Y axis
        glRotatef(self.rotation.z, 0, 0, 1)  # Rotation on Z axis

        # Apply color to the player
        glColor3f(*self.color)
        
        # Draw the player as a solid cube
        glutSolidCube(self.width)  # The player's size is based on its width
        
        glPopMatrix()


# Floor Class
class Floor(PhysicsObject):
    def __init__(self, position=Vector3(0, 0, 0), width=300, height=300, depth=1):
        # Set the floor to be a large flat surface
        super().__init__(position, Vector3(0, 0, 0), width, height, depth)
        self.color = (0.4, 0.4, 0.4)  # Color the floor gray

    def draw(self):
        glPushMatrix()

        # Translate the floor to its position (usually on the bottom of the scene)
        glTranslatef(self.position.x, self.position.y, self.position.z)
        
        # Draw the floor as a large cube (which is flat in this case)
        glColor3f(*self.color)  # Set the floor color
        glScalef(self.width, self.depth, self.height)  # Scale to create a flat surface

        glutSolidCube(1)  # The cube is scaled to create a floor surface

        glPopMatrix()
