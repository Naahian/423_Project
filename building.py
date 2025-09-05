import time
from physics_object import PhysicsObject, Vector3, load_texture
from physics_object import PhysicsObject, Vector3
from OpenGL.GL import *
from OpenGL.GLUT import *
from physics_object import PhysicsObject, Vector3
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *





class Building(PhysicsObject):
    """A simple farmhouse with cube base and triangular roof."""
    def __init__(self, position, width=5, height=5, depth=5, wall_texture=None, roof_texture=None):
        super().__init__(position, Vector3(0, 0, 0), width, height, depth)
        self.wall_color = (0.6, 0.3, 0.0)  # Brown walls
        self.roof_color = (0.8, 0.0, 0.0)  # Red roof
        
        self.wall_texture_id = None
        self.roof_texture_id = None
        
        if wall_texture:
            self.wall_texture_id = load_texture(wall_texture)
        if roof_texture:
            self.roof_texture_id = load_texture(roof_texture)

    def render_cube_with_texture(self, width, height, depth):
        """Draw a cube with proper texture coordinates"""
        w, h, d = width/2, height/2, depth/2
        
        glBegin(GL_QUADS)
        
        # Front face
        glTexCoord2f(0.0, 0.0); glVertex3f(-w, -h, d)
        glTexCoord2f(1.0, 0.0); glVertex3f(w, -h, d)
        glTexCoord2f(1.0, 1.0); glVertex3f(w, h, d)
        glTexCoord2f(0.0, 1.0); glVertex3f(-w, h, d)
        
        # Back face
        glTexCoord2f(1.0, 0.0); glVertex3f(-w, -h, -d)
        glTexCoord2f(1.0, 1.0); glVertex3f(-w, h, -d)
        glTexCoord2f(0.0, 1.0); glVertex3f(w, h, -d)
        glTexCoord2f(0.0, 0.0); glVertex3f(w, -h, -d)
        
        # Top face
        glTexCoord2f(0.0, 1.0); glVertex3f(-w, h, -d)
        glTexCoord2f(0.0, 0.0); glVertex3f(-w, h, d)
        glTexCoord2f(1.0, 0.0); glVertex3f(w, h, d)
        glTexCoord2f(1.0, 1.0); glVertex3f(w, h, -d)
        
        # Bottom face
        glTexCoord2f(1.0, 1.0); glVertex3f(-w, -h, -d)
        glTexCoord2f(0.0, 1.0); glVertex3f(w, -h, -d)
        glTexCoord2f(0.0, 0.0); glVertex3f(w, -h, d)
        glTexCoord2f(1.0, 0.0); glVertex3f(-w, -h, d)
        
        # Right face
        glTexCoord2f(1.0, 0.0); glVertex3f(w, -h, -d)
        glTexCoord2f(1.0, 1.0); glVertex3f(w, h, -d)
        glTexCoord2f(0.0, 1.0); glVertex3f(w, h, d)
        glTexCoord2f(0.0, 0.0); glVertex3f(w, -h, d)
        
        # Left face
        glTexCoord2f(0.0, 0.0); glVertex3f(-w, -h, -d)
        glTexCoord2f(1.0, 0.0); glVertex3f(-w, -h, d)
        glTexCoord2f(1.0, 1.0); glVertex3f(-w, h, d)
        glTexCoord2f(0.0, 1.0); glVertex3f(-w, h, -d)
        
        glEnd()

    def render(self):
        # Base walls
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        
        if self.wall_texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.wall_texture_id)
            glColor3f(1.0, 1.0, 1.0)  # Use white to preserve texture colors
        else:
            glColor3f(*self.wall_color)
        
        # Draw cube with proper texture coordinates
        self.render_cube_with_texture(self.width, self.height, self.depth)
        
        if self.wall_texture_id:
            glDisable(GL_TEXTURE_2D)
        
        glPopMatrix()

        # Roof (triangular prism, front + back + sides)
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y + self.height / 2, self.position.z)

        if self.roof_texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.roof_texture_id)
            glColor3f(1.0, 1.0, 1.0)
        else:
            glColor3f(*self.roof_color)

        # Front triangle
        glBegin(GL_TRIANGLES)
        glTexCoord2f(0.0, 0.0); glVertex3f(-self.width / 2, 0, self.depth / 2)
        glTexCoord2f(1.0, 0.0); glVertex3f(self.width / 2, 0, self.depth / 2)
        glTexCoord2f(0.5, 1.0); glVertex3f(0, self.height / 2, self.depth / 2)
        glEnd()

        # Back triangle
        glBegin(GL_TRIANGLES)
        glTexCoord2f(0.0, 0.0); glVertex3f(-self.width / 2, 0, -self.depth / 2)
        glTexCoord2f(1.0, 0.0); glVertex3f(self.width / 2, 0, -self.depth / 2)
        glTexCoord2f(0.5, 1.0); glVertex3f(0, self.height / 2, -self.depth / 2)
        glEnd()

        # Left side (rectangle)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f(-self.width / 2, 0, -self.depth / 2)
        glTexCoord2f(1.0, 0.0); glVertex3f(-self.width / 2, 0, self.depth / 2)
        glTexCoord2f(1.0, 1.0); glVertex3f(0, self.height / 2, self.depth / 2)
        glTexCoord2f(0.0, 1.0); glVertex3f(0, self.height / 2, -self.depth / 2)
        glEnd()

        # Right side (rectangle)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f(self.width / 2, 0, -self.depth / 2)
        glTexCoord2f(1.0, 0.0); glVertex3f(self.width / 2, 0, self.depth / 2)
        glTexCoord2f(1.0, 1.0); glVertex3f(0, self.height / 2, self.depth / 2)
        glTexCoord2f(0.0, 1.0); glVertex3f(0, self.height / 2, -self.depth / 2)
        glEnd()

        # Bottom side (rectangle - optional, might be hidden by walls)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f(-self.width / 2, 0, -self.depth / 2)
        glTexCoord2f(1.0, 0.0); glVertex3f(-self.width / 2, 0, self.depth / 2)
        glTexCoord2f(1.0, 1.0); glVertex3f(self.width / 2, 0, self.depth / 2)
        glTexCoord2f(0.0, 1.0); glVertex3f(self.width / 2, 0, -self.depth / 2)
        glEnd()

        if self.roof_texture_id:
            glDisable(GL_TEXTURE_2D)

        glPopMatrix()
