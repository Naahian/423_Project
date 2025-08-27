import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time

from entities import Floor, Player
from physics_object import Vector3

# Global variables for the game
camera_position = [5.0, 5.0, 15.0]  # Where the camera is
camera_target = [0.0, 0.0, 0.0]     # What the camera looks at
camera_up = [0.0, 1.0, 0.0]         # What is "up" for the camera

entities = []
systems = []
    
# OpenGL and GLUT initialization
def setup_opengl():
    """Setup the OpenGL environment (viewport, projection, etc.)."""
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    # --- Lighting ---
    glEnable(GL_LIGHTING)        # Enable lighting
    glEnable(GL_LIGHT0)          # Enable light source 0
    glEnable(GL_COLOR_MATERIAL)  # Enable material coloring via glColor*

    # Light position and color
    light_position = [10.0, 10.0, 10.0, 1.0]  # Positional light
    light_ambient = [0.2, 0.2, 0.2, 1.0]
    light_diffuse = [0.8, 0.8, 0.8, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

    # Projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 800 / 600, 0.5, 100.0)

    glMatrixMode(GL_MODELVIEW)

def render_scene():
    """Called by GLUT to render the game scene."""
    global entities, camera_position,camera_target, camera_up

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen and depth buffer
    glLoadIdentity()  # Reset transformations

    # Camera Position (move it back along the Z-axis)
    glTranslatef(0.0, 0.0, -15.0)  # Move the camera backwards along Z-axis

    gluLookAt(
        camera_position[0], camera_position[1], camera_position[2],  # Eye (camera position)
        camera_target[0], camera_target[1], camera_target[2],        # Center (look-at point)
        camera_up[0], camera_up[1], camera_up[2]                     # Up vector
    )
    # Update and render game entities
    for entity in entities:
        entity.draw()  # Draw the entity

  
    # Swap buffers to display the frame
    glutSwapBuffers()

def update_game(delta_time):
    """Update game logic (physics, systems, etc.)."""
    pass
    # Additional game logic updates can go here (economy, weather, etc.)

def idle_func():
    """Called when GLUT is idle. Keep updating the game loop."""
    delta_time = 0.016  # Simulate 60 FPS (1/60)
    update_game(delta_time)
    render_scene()  # Re-render the scene after the update

def handle_input(key, x, y):
    """Handle keyboard input."""
    if key == b'\x1b':  # Escape key
        sys.exit(0)  # Exit the game

def init_game():
    """Initialize the game objects and systems."""
    global player, crop, hud, day_night_cycle, game

    # Create game entities
    # Create a Player object with position, velocity, and dimensions
    player = Player(position=Vector3(0.0, 3.0, 0.0),  # Starting position (x, y, z)
                    velocity=Vector3(0.0, 0.0, 0.0),  # Stationary velocity (no movement)
                    width=4.0,  # Player's width
                    height=4.0,  # Player's height
                    depth=4.0)  # Player's depth (same as width for simplicity)

    # Create a Floor object with position and size
    floor = Floor(position=Vector3(0.0, -1.0, 0.0),  # Floor position, slightly below the player
                width=30.0,  # Width of the floor (large surface)
                height=30.0,  # Height of the floor (typically small)
                depth=1.0)  # Depth of the floor (also large for coverage)
    
    global entities, systems
    entities = [player, floor]
    systems = []
    

# Main function to initialize and start the game
def main():
    """Main entry point for the game with OpenGL and GLUT."""
    glutInit(sys.argv)  # Initialize GLUT
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)  # Display mode: RGB, double-buffered, depth-buffered
    glutInitWindowSize(800, 600)  # Set window size
    glutCreateWindow(b"Farming Sim Game")  # Create the OpenGL window

    # Initialize OpenGL
    setup_opengl()

    # Initialize game objects and systems
    init_game()

    # Register GLUT callbacks
    glutDisplayFunc(render_scene)  # Display function for rendering
    glutIdleFunc(idle_func)  # Idle function to keep the game running
    glutKeyboardFunc(handle_input)  # Keyboard input handler

    # Start the GLUT main loop
    glutMainLoop()

if __name__ == "__main__":
    main()
