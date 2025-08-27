from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

# Vector3 Class
class Vector3:
    """A 3D vector class to represent positions, velocities, etc."""
    
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        length = self.length()
        if length == 0:
            return Vector3()
        return self * (1.0 / length)

# PhysicsObject Class
class PhysicsObject:
    """Base class for any object in the game world that has physics (3D)."""
    
    def __init__(self, position, velocity, width, height, depth):
        self.position = position  # 3D position (x, y, z)
        self.velocity = velocity  # 3D velocity (vx, vy, vz)
        self.width = width
        self.height = height
        self.depth = depth
        self.collidable = True
        self.rotation = Vector3(0, 0, 0)  # Rotation around x, y, z
        self.color = (0.5, 0.5, 0.5)  # Default color (gray)

    def update(self, delta_time):
        self.position += self.velocity * delta_time
        self.handle_collision()

    def handle_collision(self):
        """Logic to handle collision, currently no resolution."""
        pass

    def check_collision(self, other):
        """Check if this object collides with another object (in 3D)."""
        return (self.position.x < other.position.x + other.width and
                self.position.x + self.width > other.position.x and
                self.position.y < other.position.y + other.height and
                self.position.y + self.height > other.position.y and
                self.position.z < other.position.z + other.depth and
                self.position.z + self.depth > other.position.z)

    def draw(self):
        """Draw the 3D object."""
        glPushMatrix()  # Save the current transformation matrix
        
        glTranslatef(self.position.x, self.position.y, self.position.z)  # Move the object to its position
        glRotatef(self.rotation.x, 1, 0, 0)  # Rotate around X-axis
        glRotatef(self.rotation.y, 0, 1, 0)  # Rotate around Y-axis
        glRotatef(self.rotation.z, 0, 0, 1)  # Rotate around Z-axis

        # Apply color
        glColor3f(*self.color)  # Apply the object's color
        
        self.render()  # Render the object
        
        glPopMatrix()  # Restore the transformation matrix

    def render(self):
        """Render the object. This can be a cube for simplicity."""
        glutSolidCube(1)  # Draw a unit cube
