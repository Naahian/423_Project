import sys
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from ui import *
from floor import *
from crop import *
from building import *
from player import Player
from physics_object import Vector3
import time

# Global game state
game_state = {
    'ui_entities': [],
    'world_entities': [],
    'systems': [],
    'player': None,
    'elapsed_sec': 0,
    'camera_position': [5.0, 5.0, 15.0],
    'camera_target': [0.0, 0.0, 0.0],
    'camera_up': [0.0, 1.0, 0.0],
    'last_mouse_x': 400,
    'last_mouse_y': 300,
    'mouse_initialized': False,
    'light_pos': [15.0, 40.0, 30.0, 1.0]
}


DELTA_TIME = 1.0 / 60.0  # 60 FPS
start_time = time.time()


def setup_lighting():
    """Configure OpenGL lighting."""
    global game_state
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    # Light configuration
    light_props = {
        GL_POSITION: game_state['light_pos'],
        GL_AMBIENT: [0.2, 0.2, 0.2, 1.0],
        GL_DIFFUSE: [0.8, 0.8, 0.8, 1.0],
        GL_SPECULAR: [1.0, 1.0, 1.0, 1.0]
    }
    
    for prop, values in light_props.items():
        glLightfv(GL_LIGHT0, prop, values)


def setup_projection():
    """Configure OpenGL projection matrix."""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 800.0 / 600.0, 0.5, 100.0)
    glMatrixMode(GL_MODELVIEW)


def setup_opengl():
    """Initialize OpenGL settings."""
    glClearColor(0.85, 0.88, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    setup_lighting()
    setup_projection()


def set_camera_view():
    """Set up the camera view matrix."""
    gluLookAt(
        *game_state['camera_position'],
        *game_state['camera_target'],
        *game_state['camera_up']
    )


def render_scene():
    """Render the complete game scene."""
    global game_state
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    
    set_camera_view()
    
    for entity in game_state['ui_entities']:
        entity.draw()
    for entity in game_state['world_entities']:
        entity.draw()
    
    draw_sun(game_state)

    glutSwapBuffers()




def update_timer():
    """Update the game timer."""


#######################################################################################
#######################################################################################

def handle_special_events():
    """Process special timed events."""
    # plant update
    # harvest update
    # etc

def update_player(delta_time):
    """Update player movement and state."""
    player = game_state['player']
    if player:
        player.update_movement(
            delta_time,
            game_state['camera_position'],
            game_state['camera_target'],
            game_state['camera_up']
        )


def update_game(delta_time):
    """Update all game systems."""
    global game_state
    
    handle_special_events()
    update_player(delta_time)
    
    if(game_state['mouse_initialized']):
        glutSetCursor(GLUT_CURSOR_NONE)
    else:
        glutSetCursor(GLUT_CURSOR_LEFT_ARROW)


def game_loop():
    """Main game loop called by GLUT idle function."""
    update_game(DELTA_TIME)
    render_scene()
    update_timer()


def handle_keyboard_down(key, x, y):
    """Process keyboard key press events."""
    global game_state
    player = game_state['player']
    
    if key == b'\x1b':  # Escape key
        game_state['mouse_initialized'] = not game_state['mouse_initialized']
    
    if key == b't':
        print(game_state['elapsed_sec'])

    # Movement keys
    if key in [b'w', b'a', b's', b'd'] and player:
        player.set_key_state(key, True)
    
    # Action keys
    elif key in [b'e', b'r', b'f'] and player:
        player.action(key, game_state['world_entities'])


def handle_keyboard_up(key, x, y):
    """Process keyboard key release events."""
    player = game_state['player']
    
    if key in [b'w', b'a', b's', b'd'] and player:
        player.set_key_state(key, False)


def recenter_mouse_if_needed(x, y):
    """Recenter mouse cursor if it moves too far from center."""
    center_x, center_y = 400, 300
    
    if abs(x - center_x) > 200 or abs(y - center_y) > 150:
        glutWarpPointer(center_x, center_y)
        game_state['last_mouse_x'] = center_x
        game_state['last_mouse_y'] = center_y


def handle_mouse_movement(x, y):
    """Process mouse movement for camera control."""
    if not game_state['mouse_initialized']:
        game_state['last_mouse_x'] = x
        game_state['last_mouse_y'] = y
        return

    dx = x - game_state['last_mouse_x']
    dy = y - game_state['last_mouse_y']
    
    player = game_state['player']
    if (dx != 0 or dy != 0) and player:
        player.mouse_look(
            dx, dy,
            game_state['camera_position'],
            game_state['camera_target'],
            game_state['camera_up']
        )
    
    game_state['last_mouse_x'] = x
    game_state['last_mouse_y'] = y
    
    # recenter_mouse_if_needed(x, y)


def create_player():
    """Create and return the player entity."""
    return Player(
        position=Vector3(0.0, 0.2, 0.0),
        velocity=Vector3(0.0, 0.0, 0.0),
        width=2.0, height=2.0, depth=2.0
    )


def create_world_entities():
    """Create and return world entities."""
    floor = Floor(
        position=Vector3(0.0, -1.0, 0.0),
        width=100.0, height=100.0, depth=1.0,
        texture_file= "assets/terrain.jpg",
        texture_repeat= 30
    )
    crop = Crop(Vector3(0, -1, 0))
    building = Building(Vector3(4, 0, 0), wall_texture="assets/wall.jpg",roof_texture="assets/roof.png")
    
    return [floor, crop, building]


def create_ui_entities():
    """Create and return UI entities."""
    return [
        HealthBar(),
        EnergyBar(),
        HouseIcon(),
        CropGrowthBar()
    ]



###########################################################################################
###########################################################################################

def initialize_entities():
    """Initialize all game entities."""
    game_state['player'] = create_player()
    
    ui_entities = create_ui_entities()
    world_entities = create_world_entities()
    
    game_state['ui_entities'] = ui_entities
    game_state['world_entities'] = world_entities


def setup_glut_window():
    """Initialize GLUT window and settings."""
    global game_state
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(1,-1)
    glutCreateWindow(b"Farming Game")
    glutSetCursor(GLUT_CURSOR_NONE)
    

def register_callbacks():
    """Register all GLUT callback functions."""
    global game_state
    glutDisplayFunc(render_scene)
    glutIdleFunc(game_loop)
    glutKeyboardFunc(handle_keyboard_down)
    glutKeyboardUpFunc(handle_keyboard_up)
    glutPassiveMotionFunc(handle_mouse_movement)
    glutMotionFunc(handle_mouse_movement)


def initialize_game():
    """Initialize the complete game."""
    global game_state
    setup_glut_window()
    setup_opengl()
    initialize_entities()
    register_callbacks()
    game_state['mouse_initialized'] = True

def main():
    """Main entry point for the game."""
    global game_state
    initialize_game()
    glutMainLoop()


if __name__ == "__main__":
    main()