
import math
from crop import Crop
from physics_object import Vector3


class Player:
    def __init__(self, position, velocity, width, height, depth):
        self.position = position
        self.velocity = velocity
        self.width = width
        self.height = height
        self.depth = depth
        
        # Camera angles
        self.yaw = 0.0
        self.pitch = 0.0
        self.mouse_sensitivity = 0.005
        


        # Movement
        self.move_speed = 1.0
        self.keys = {'w': False, 'a': False, 's': False, 'd': False}
        
        # Player stats
        self.crop_count = 0
        self.energy = 100

    def set_key_state(self, key, pressed):
        """Set the state of movement keys"""
        if key == b'w':
            self.keys['w'] = pressed
        elif key == b's':
            self.keys['s'] = pressed
        elif key == b'a':
            self.keys['a'] = pressed
        elif key == b'd':
            self.keys['d'] = pressed

    def update_movement(self, delta_time, camera_position, camera_target, camera_up):
        """Update player movement based on currently pressed keys"""
        # Calculate camera forward vector (normalized)
        forward_x = camera_target[0] - camera_position[0]
        forward_y = camera_target[1] - camera_position[1]
        forward_z = camera_target[2] - camera_position[2]
        
        # Normalize the forward vector
        forward_length = math.sqrt(forward_x**2 + forward_y**2 + forward_z**2)
        if forward_length > 0:
            forward_x /= forward_length
            forward_y /= forward_length
            forward_z /= forward_length
        
        # Calculate right vector (cross product of forward and up)
        right_x = forward_z * camera_up[1] - forward_y * camera_up[2]
        right_y = forward_x * camera_up[2] - forward_z * camera_up[0]
        right_z = forward_y * camera_up[0] - forward_x * camera_up[1]
        
        # Normalize the right vector
        right_length = math.sqrt(right_x**2 + right_y**2 + right_z**2)
        if right_length > 0:
            right_x /= right_length
            right_y /= right_length
            right_z /= right_length
        
        # Calculate movement direction based on keys
        move_x, move_y, move_z = 0.0, 0.0, 0.0
        
        if self.keys['w']:  # Forward
            move_x += forward_x * self.move_speed * delta_time
            move_z += forward_z * self.move_speed * delta_time
        if self.keys['s']:  # Backward
            move_x -= forward_x * self.move_speed * delta_time
            move_z -= forward_z * self.move_speed * delta_time
        if self.keys['a']:  # Left (strafe)
            move_x += right_x * self.move_speed * delta_time
            move_z += right_z * self.move_speed * delta_time
        if self.keys['d']:  # Right (strafe)
            move_x -= right_x * self.move_speed * delta_time
            move_z -= right_z * self.move_speed * delta_time
        
        # Update player position (ignore Y movement for ground-based movement)
        self.position.x += move_x
        self.position.z += move_z
        
        # Update camera to follow player
        self.update_camera(camera_position, camera_target)
        
    def update_camera(self, camera_position, camera_target):
        """Update camera position and target based on player position and rotation"""
        camera_distance = 3.5
        base_height = 2.5
        
        # Calculate camera position behind the player using both yaw and pitch
        camera_position[0] = self.position.x - camera_distance * math.cos(self.yaw) * math.cos(self.pitch)
        camera_position[1] = self.position.y + base_height - camera_distance * math.sin(self.pitch)
        camera_position[2] = self.position.z - camera_distance * math.sin(self.yaw) * math.cos(self.pitch)
        
        # Camera looks at the player
        camera_target[0] = self.position.x
        camera_target[1] = self.position.y 
        camera_target[2] = self.position.z + 1


    def mouse_look(self, dx, dy, camera_position, camera_target, camera_up):
        """Handle mouse movement for camera rotation"""
        self.yaw += dx * self.mouse_sensitivity
        self.pitch -= dy * self.mouse_sensitivity
        
        # Clamp pitch to prevent over-rotation
        self.pitch = max(-math.pi/2 + 0.1, min(math.pi/2 - 0.1, self.pitch))
        
        # Update camera based on new angles
        self.update_camera(camera_position, camera_target)

    def action(self, key, entities):
        """Handle action keys: collect crops, plant crops, interact with buildings"""
        
        if key == b'e':  # Collect/harvest nearby crops
            for entity in entities[:]:  # Use slice to avoid modification during iteration
                if hasattr(entity, 'crop_type'):  # It's a crop
                    distance = math.sqrt((entity.position.x - self.position.x)**2 + 
                                       (entity.position.z - self.position.z)**2)
                    if distance < 3.0:  # Within range
                        if hasattr(entity, 'is_mature') and entity.is_mature():
                            self.crop_count += 1
                            entities.remove(entity)
                            print(f"Harvested crop! Total: {self.crop_count}")
                            break
                            
        elif key == b'r':  # Plant/throw crop
            if self.crop_count > 0:
                # Create new crop at player position
                new_crop = Crop(Vector3(self.position.x + 2, 0, self.position.z))
                entities.append(new_crop)
                self.crop_count -= 1
                print(f"Planted crop! Remaining: {self.crop_count}")
                
        elif key == b'f':  # Interact with buildings
            for entity in entities:
                if hasattr(entity, 'building_type'):  # It's a building
                    distance = math.sqrt((entity.position.x - self.position.x)**2 + 
                                       (entity.position.z - self.position.z)**2)
                    if distance < 4.0:  # Within range
                        self.energy = min(100, self.energy + 20)
                        print(f"Used building! Energy: {self.energy}")
                        break
