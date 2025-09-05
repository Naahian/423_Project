from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import numpy as np
from PIL import Image



def load_texture(filename):
    """Load texture from image file."""
    try:
        image = Image.open(filename)
        image = image.convert('RGB')
        image_data = np.array(image, dtype=np.uint8)
        
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        height, width = image_data.shape[:2]
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, 
                    GL_RGB, GL_UNSIGNED_BYTE, image_data)
        
        return texture_id
    except:
        return None


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
        
        # Gravity settings
        self.gravity_enabled = True  # Whether gravity affects this object
        self.gravity_strength = -9.8  # Gravity acceleration (negative = downward)
        self.on_ground = False  # Whether the object is touching the ground
        self.ground_level = 0.0  # Ground level (floor Y position)
        self.bounce_factor = 0.3  # How bouncy the object is (0.0 = no bounce, 1.0 = perfect bounce)
        self.friction = 0.95  # Air resistance/friction (0.0 = stops immediately, 1.0 = no friction)

    def update(self, delta_time):
        """Update physics with gravity"""
        if self.gravity_enabled:
            self.apply_gravity(delta_time)
        
        # Apply movement
        self.position += self.velocity * delta_time
        
        # Handle ground collision
        self.handle_ground_collision()
        
        # Handle other collisions
        self.handle_collision()
        
        # Apply friction
        self.apply_friction()

    def apply_gravity(self, delta_time):
        """Apply gravity to the object"""
        if not self.on_ground:
            # Add gravity to Y velocity (downward acceleration)
            self.velocity.y += self.gravity_strength * delta_time

    def handle_ground_collision(self):
        """Handle collision with the ground"""
        # Calculate the bottom of the object
        object_bottom = self.position.y - (self.height / 2)
        
        # Check if object hits the ground
        if object_bottom <= self.ground_level:
            # Place object on ground
            self.position.y = self.ground_level + (self.height / 2)
            
            # Handle bouncing
            if self.velocity.y < 0:  # Only bounce if moving downward
                self.velocity.y = -self.velocity.y * self.bounce_factor
                
                # Stop tiny bounces
                if abs(self.velocity.y) < 0.1:
                    self.velocity.y = 0
                    self.on_ground = True
            else:
                self.on_ground = True
        else:
            self.on_ground = False

    def apply_friction(self):
        """Apply air resistance/friction to all movement"""
        self.velocity.x *= self.friction
        self.velocity.z *= self.friction
        
        # Only apply Y friction if object is moving very slowly
        if abs(self.velocity.y) < 0.1:
            self.velocity.y *= self.friction

    def jump(self, force=5.0):
        """Make the object jump (add upward velocity)"""
        if self.on_ground:  # Can only jump when on ground
            self.velocity.y = force
            self.on_ground = False

    def add_force(self, force_vector):
        """Add a force to the object (changes velocity)"""
        self.velocity += force_vector

    def set_gravity_enabled(self, enabled):
        """Enable or disable gravity for this object"""
        self.gravity_enabled = enabled

    def set_ground_level(self, y_level):
        """Set the ground level for this object"""
        self.ground_level = y_level

    def handle_collision(self):
        """Logic to handle collision, currently no resolution."""
        pass

    def check_collision(self, other):
        """Check if this object collides with another object (in 3D)."""
        return (self.position.x - self.width/2 < other.position.x + other.width/2 and
                self.position.x + self.width/2 > other.position.x - other.width/2 and
                self.position.y - self.height/2 < other.position.y + other.height/2 and
                self.position.y + self.height/2 > other.position.y - other.height/2 and
                self.position.z - self.depth/2 < other.position.z + other.depth/2 and
                self.position.z + self.depth/2 > other.position.z - other.depth/2)

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