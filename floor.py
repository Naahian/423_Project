from physics_object import PhysicsObject, Vector3, load_texture
from physics_object import PhysicsObject, Vector3
from OpenGL.GL import *
from OpenGL.GLUT import *
from physics_object import PhysicsObject, Vector3
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def draw_sun(game_state):
    glDisable(GL_LIGHTING)
    glPushMatrix()
    glTranslatef(game_state['light_pos'][0],game_state['light_pos'][1],game_state['light_pos'][2])
    glutSolidSphere(1,20,20)
    glPopMatrix()
    glEnable(GL_LIGHTING)



class Floor(PhysicsObject):
    def __init__(self, position=Vector3(0, 0, 0), width=500, height=500, depth=1, 
                 texture_file=None, texture_repeat=10.0):
        super().__init__(position, Vector3(0, 0, 0), width, height, depth)
        self.color = (0.3, 0.6, 0.1) 
        self.texture_id = None
        self.texture_repeat = texture_repeat  # How many times to repeat texture
        
        # Load texture if provided
        if texture_file:
            self.texture_id =  load_texture(texture_file)
    
    
    def draw_textured_quad(self):
        """Draw a textured quad for the floor."""
        half_width = self.width / 2
        half_height = self.height / 2
        
        # Calculate texture coordinates based on repeat factor
        tex_max = self.texture_repeat
        
        glBegin(GL_QUADS)
        
        # Bottom face (the floor surface)
        glNormal3f(0, 1, 0)  # Normal pointing up
        
        # Vertex 1: Front-left
        glTexCoord2f(0, 0)
        glVertex3f(-half_width, 0, half_height)
        
        # Vertex 2: Front-right  
        glTexCoord2f(tex_max, 0)
        glVertex3f(half_width, 0, half_height)
        
        # Vertex 3: Back-right
        glTexCoord2f(tex_max, tex_max)
        glVertex3f(half_width, 0, -half_height)
        
        # Vertex 4: Back-left
        glTexCoord2f(0, tex_max)
        glVertex3f(-half_width, 0, -half_height)
        
        glEnd()
    
    def draw_colored_cube(self):
        """Draw the floor as a colored cube (fallback)."""
        glColor3f(*self.color) 
        glScalef(self.width, self.depth, self.height) 
        glutSolidCube(1)
    
    def draw(self):
        """Main draw method with texture support."""
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        
        # Enable texturing if texture is available
        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            
            # Set color to white so texture shows properly
            glColor3f(1.0, 1.0, 1.0)
            
            # Draw textured floor
            self.draw_textured_quad()
            
            # Disable texturing
            glDisable(GL_TEXTURE_2D)
        else:
            # Fall back to colored cube
            self.draw_colored_cube()
        
        glPopMatrix()
    
    def set_texture_repeat(self, repeat_factor):
        """Change how many times the texture repeats across the floor."""
        self.texture_repeat = repeat_factor

