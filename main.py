import sys
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from ui import *
from entities import *
from player import Player
from physics_object import Vector3



# Global variables for the game
camera_position = [5.0, 5.0, 15.0]  # Where the camera is
camera_target = [0.0, 0.0, 0.0]     # What the camera looks at
camera_up = [0.0, 1.0, 0.0]         # What is "up" for the camera
timer = None 
elapsed_sec = 0;


entities = []
systems = []

player = None
last_mouse_x = 400
last_mouse_y = 300
mouse_initialized = False

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
    gluPerspective(45.0, 800.0 / 600.0, 0.5, 100.0)

    glMatrixMode(GL_MODELVIEW)

def render_scene():
    """Called by GLUT to render the game scene."""
    global entities, camera_position, camera_target, camera_up

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen and depth buffer
    glLoadIdentity()  # Reset transformations

    # Set up camera view - REMOVED the conflicting glTranslatef
    gluLookAt(
        camera_position[0], camera_position[1], camera_position[2],  # Eye (camera position)
        camera_target[0], camera_target[1], camera_target[2],        # Center (look-at point)
        camera_up[0], camera_up[1], camera_up[2]                     # Up vector
    )

    # Draw all entities
    for entity in entities:
        entity.draw()  # Draw the entity
    
    # Swap buffers to display the frame
    glutSwapBuffers()

def update_game(delta_time):
    """Update game logic (physics, systems, etc.)."""
    global player, camera_position, camera_target, camera_up, entities, elapsed_sec
    print(elapsed_sec)
    if(elapsed_sec == 2):
        entities[3].update(entities[3].stage+1)
    
    if player:
        player.update_movement(delta_time, camera_position, camera_target, camera_up)

    delta_time

def idle_func():
    """Called when GLUT is idle. Keep updating the game loop."""
    delta_time = 0.016  # Simulate 60 FPS (1/60)
    update_game(delta_time)
    render_scene()  # Re-render the scene after the update

def handle_keyboard_down(key, x, y):
    """Handle keyboard key press."""
    global player, entities
    
    if key == b'\x1b':  # Escape key
        sys.exit(0)  # Exit the game

    # Movement keys
    if key in [b'w', b'a', b's', b'd']:
        if player:
            player.set_key_state(key, True)
    
    # Action keys
    elif key in [b'e', b'r', b'f']:
        if player:
            player.action(key, entities)

def handle_keyboard_up(key, x, y):
    """Handle keyboard key release."""
    global player
    
    # Movement keys
    if key in [b'w', b'a', b's', b'd']:
        if player:
            player.set_key_state(key, False)

def handle_mouse(x, y):
    """Handle mouse movement for camera"""
    global player, last_mouse_x, last_mouse_y, camera_position, camera_target, camera_up, mouse_initialized
    
    # Initialize mouse position on first call
    if not mouse_initialized:
        last_mouse_x = x
        last_mouse_y = y
        mouse_initialized = True
        return
    
    dx = x - last_mouse_x
    dy = y - last_mouse_y
    
    if (abs(dx) > 0 or abs(dy) > 0) and player:
        player.mouse_look(dx, dy, camera_position, camera_target, camera_up)
    
    last_mouse_x = x
    last_mouse_y = y

    # Keep mouse centered for FPS-style controls (optional)
    window_center_x, window_center_y = 400, 300
    if abs(x - window_center_x) > 200 or abs(y - window_center_y) > 150:
        glutWarpPointer(window_center_x, window_center_y)
        last_mouse_x = window_center_x
        last_mouse_y = window_center_y

def elapse_time():
    global elapsed_sec
    elapsed_sec = (elapsed_sec+1)%60

def init_game():
    """Initialize the game objects and systems."""
    global player, entities, systems, timer

    # Create game entities
    player = Player(position=Vector3(0.0, 1.0, 0.0), 
                    velocity=Vector3(0.0, 0.0, 0.0), 
                    width=2.0,  
                    height=2.0, 
                    depth=2.0)  

    floor = Floor(position=Vector3(0.0, -1.0, 0.0),  
                width=30.0,  
                height=30.0, 
                depth=1.0)  
    
    crop = Crop(Vector3(0, 1, 0))
    building = Building(Vector3(4, 4, 0))
    healthBar = HealthBar()
    energyBar = EnergyBar()
    houseIcon = HouseIcon()
    cropGrowthBar = CropGrowthBar()

    entities = [healthBar, energyBar, houseIcon, cropGrowthBar, floor, crop, building]
    systems = []

def main():
    """Main entry point for the game with OpenGL and GLUT."""
    glutInit(sys.argv)  # Initialize GLUT
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)  # Display mode: RGB, double-buffered, depth-buffered
    glutInitWindowSize(800, 600)  # Set window size
    glutCreateWindow(b"Farming Sim Game")  # Create the OpenGL window

    # Hide cursor for better FPS controls (optional)
    glutSetCursor(GLUT_CURSOR_NONE)

    # Initialize OpenGL
    setup_opengl()

    # Initialize game objects and systems
    init_game()

    # Register GLUT callbacks
    glutDisplayFunc(render_scene)  # Display function for rendering
    glutIdleFunc(idle_func)  # Idle function to keep the game running
    glutKeyboardFunc(handle_keyboard_down)  # Keyboard key press handler
    glutKeyboardUpFunc(handle_keyboard_up)  # Keyboard key release handler
    glutPassiveMotionFunc(handle_mouse)    # Mouse movement handler
    glutMotionFunc(handle_mouse)           # Mouse movement with button pressed
    
    # Start the GLUT main loop
    glutMainLoop()

if __name__ == "__main__":
    main()