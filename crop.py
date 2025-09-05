import time
from physics_object import PhysicsObject, Vector3
from OpenGL.GL import *
from OpenGL.GLUT import *
from physics_object import PhysicsObject, Vector3
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *





class Crop(PhysicsObject):
    
    def __init__(self, position, width=1.0, height=1.0, depth=1.0, threshold=5):
        super().__init__(position, Vector3(0, 0, 0), width, height, depth)
        self.growth_stage = 0  # 0 = seed, 1 = sprout, 2 = grown
        self.color = (0.6, 0.4, 0.2)  # Brown seed
        self.threshold = threshold
        # Timer initialization
        self.start_time = time.perf_counter()
        self.last_second_printed = 0
        self.last_stage_update = 0
        
        print(f"Crop created at position {position}")
        print(f"Timer started: 0 seconds")

    def update(self, delta_time):
        self.update_timer()
        return super().update(delta_time)

    def update_timer(self):
        """Update crop timer and handle growth stages."""
        current_time = time.perf_counter()
        elapsed_time = current_time - self.start_time
        elapsed_seconds = int(elapsed_time)
        
        # Print elapsed time every second
        if elapsed_seconds > self.last_second_printed:
            self.last_second_printed = elapsed_seconds
            print(f"Crop elapsed time: {elapsed_seconds} seconds")
        
        # Update stage every threshold time
        stage_check = elapsed_seconds // self.threshold  
        if stage_check > self.last_stage_update:
            self.last_stage_update = stage_check
            self.grow()
            print(f"Crop stage updated after {elapsed_seconds} seconds - Stage: {self.growth_stage}")

    def grow(self):
        """Advance growth stage and update appearance."""
        if self.growth_stage < 2:
            self.growth_stage += 1

        if self.growth_stage == 1:
            self.color = (0.2, 0.8, 0.2)  # Green sprout
            self.height = 2.0
            print("Crop grew to sprout stage!")
        elif self.growth_stage == 2:
            self.color = (1.0, 1.0, 0.0)  # Yellow harvest-ready
            self.height = 3.0
            print("Crop is ready for harvest!")

    def get_elapsed_seconds(self):
        """Get total elapsed seconds since creation."""
        return int(time.perf_counter() - self.start_time)
    
    def get_time_until_next_stage(self):
        """Get seconds until next growth stage."""
        elapsed = self.get_elapsed_seconds()
        if self.growth_stage >= 2:
            return 0  # Fully grown
        
        next_stage_time = (self.last_stage_update + 1) * 5
        return max(0, next_stage_time - elapsed)
    
    def reset_timer(self):
        """Reset the crop timer (useful for testing)."""
        self.start_time = time.perf_counter()
        self.last_second_printed = 0
        self.last_stage_update = 0
        self.growth_stage = 0
        self.color = (0.6, 0.4, 0.2)
        self.height = 1.0
        print("Crop timer reset!")

    def render(self):
        """Render crop as a small scaled cube with current color."""
        glPushMatrix()
        glColor3f(*self.color)
        
        # Scale based on current size
        glScalef(self.width, self.height, self.depth)
        glutSolidSphere(.3,5,5)
        
        glPopMatrix()

    def draw(self):
        """Main draw method that updates timer and renders."""
        # Update timer first
        self.update_timer()
        
        # Position the crop
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        
        # Render the crop
        self.render()
        
        glPopMatrix()


