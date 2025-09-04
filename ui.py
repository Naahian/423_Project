from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def render_text(text, x, y, font=GLUT_BITMAP_HELVETICA_12):
    """Helper function to render text at specified position"""
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))


# --------------------
# Health Bar (HUD)
# --------------------
class HealthBar:
    def __init__(self, max_val=100):
        self.max_val = max_val
        self.curr_val = max_val

    def update(self, new_value):
        self.curr_val = max(0, min(self.max_val, new_value))

    def draw(self, x=20, y=560, width=200, height=20):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 800, 0, 600)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Label
        glColor3f(1.0, 1.0, 1.0)  # white text
        render_text("Health", x, y + height + 5)

        # Background bar (dark red)
        glColor3f(0.2, 0.0, 0.0)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

        # Border
        glColor3f(0.8, 0.8, 0.8)
        glLineWidth(2)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

        # Filled portion with gradient-like effect
        ratio = self.curr_val / self.max_val
        if ratio > 0.6:
            glColor3f(0.0, 0.8, 0.0)  # green when healthy
        elif ratio > 0.3:
            glColor3f(1.0, 1.0, 0.0)  # yellow when moderate
        else:
            glColor3f(1.0, 0.0, 0.0)  # red when critical
            
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width * ratio, y)
        glVertex2f(x + width * ratio, y + height)
        glVertex2f(x, y + height)
        glEnd()

        # Health value text
        glColor3f(1.0, 1.0, 1.0)
        health_text = f"{int(self.curr_val)}/{int(self.max_val)}"
        render_text(health_text, x + width//2 - 20, y + height//2 - 3)

        # Restore matrices
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)


# --------------------
# Energy Bar (HUD)
# --------------------
class EnergyBar:
    def __init__(self, max_val=100):
        self.max_val = max_val
        self.curr_val = max_val

    def update(self, new_val):
        self.curr_val = max(0, min(self.max_val, new_val))

    def draw(self, x=20, y=530, width=200, height=20):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 800, 0, 600)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Label
        glColor3f(1.0, 1.0, 1.0)  # white text
        render_text("Energy", x, y + height + 5)

        # Background (dark blue)
        glColor3f(0.0, 0.0, 0.3)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

        # Border
        glColor3f(0.8, 0.8, 0.8)
        glLineWidth(2)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

        # Fill with energy-appropriate colors
        ratio = self.curr_val / self.max_val
        if ratio > 0.7:
            glColor3f(0.0, 0.8, 1.0)  # bright cyan when full
        elif ratio > 0.4:
            glColor3f(0.5, 0.7, 1.0)  # light blue when moderate
        else:
            glColor3f(0.8, 0.4, 1.0)  # purple when low
            
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width * ratio, y)
        glVertex2f(x + width * ratio, y + height)
        glVertex2f(x, y + height)
        glEnd()

        # Energy value text
        glColor3f(1.0, 1.0, 1.0)
        energy_text = f"{int(self.curr_val)}/{int(self.max_val)}"
        render_text(energy_text, x + width//2 - 20, y + height//2 - 3)

        # Restore
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)


# --------------------
# House Icon
# --------------------
class HouseIcon:
    def __init__(self, x=750, y=550, size=40):
        self.x = x
        self.y = y
        self.size = size

    def draw(self):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 800, 0, 600)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Base (house body) - warmer brown
        glColor3f(0.8, 0.5, 0.3)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.size, self.y)
        glVertex2f(self.x + self.size, self.y + self.size)
        glVertex2f(self.x, self.y + self.size)
        glEnd()

        # Door
        glColor3f(0.4, 0.2, 0.1)
        door_width = self.size // 4
        door_height = self.size // 2
        door_x = self.x + self.size // 2 - door_width // 2
        glBegin(GL_QUADS)
        glVertex2f(door_x, self.y)
        glVertex2f(door_x + door_width, self.y)
        glVertex2f(door_x + door_width, self.y + door_height)
        glVertex2f(door_x, self.y + door_height)
        glEnd()

        # Window
        glColor3f(0.7, 0.9, 1.0)  # light blue
        window_size = self.size // 6
        window_x = self.x + self.size // 4
        window_y = self.y + self.size // 2
        glBegin(GL_QUADS)
        glVertex2f(window_x, window_y)
        glVertex2f(window_x + window_size, window_y)
        glVertex2f(window_x + window_size, window_y + window_size)
        glVertex2f(window_x, window_y + window_size)
        glEnd()

        # Roof (triangle) - darker red
        glColor3f(0.7, 0.2, 0.2)
        glBegin(GL_TRIANGLES)
        glVertex2f(self.x - 5, self.y + self.size)
        glVertex2f(self.x + self.size + 5, self.y + self.size)
        glVertex2f(self.x + self.size / 2, self.y + self.size + 25)
        glEnd()

        # Home label
        glColor3f(1.0, 1.0, 1.0)
        render_text("Home", self.x - 5, self.y - 15)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)


# --------------------
# Crop Growth Bar
# --------------------
class CropGrowthBar:
    def __init__(self, max_stg=100):
        self.max_stg = max_stg
        self.curr_stg = 0

    def update(self, stage):
        self.curr_stg = max(0, min(self.max_stg, stage))

    def get_growth_stage_text(self):
        if self.curr_stg == 0:
            return "Seed"
        elif self.curr_stg < 25:
            return "Sprout"
        elif self.curr_stg < 50:
            return "Growing"
        elif self.curr_stg < 75:
            return "Flowering"
        elif self.curr_stg < 100:
            return "Ripening"
        else:
            return "Harvest Ready"

    def draw(self, x=350, y=20, width=100, height=15):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 800, 0, 600)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Label
        glColor3f(1.0, 1.0, 1.0)
        render_text("Crop Growth", x, y + height + 5)

        # Background (dark green)
        glColor3f(0.1, 0.2, 0.0)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

        # Border
        glColor3f(0.8, 0.8, 0.8)
        glLineWidth(1)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

        # Growth progress with stage-appropriate colors
        ratio = self.curr_stg / self.max_stg
        if ratio == 0:
            glColor3f(0.4, 0.2, 0.1)  # brown for seed
        elif ratio < 0.25:
            glColor3f(0.5, 0.8, 0.2)  # light green for sprout
        elif ratio < 0.75:
            glColor3f(0.2, 0.8, 0.2)  # green for growing
        elif ratio < 1.0:
            glColor3f(1.0, 1.0, 0.0)  # yellow for flowering/ripening
        else:
            glColor3f(1.0, 0.6, 0.0)  # orange for harvest ready
            
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width * ratio, y)
        glVertex2f(x + width * ratio, y + height)
        glVertex2f(x, y + height)
        glEnd()

        # Growth percentage
        glColor3f(1.0, 1.0, 1.0)
        percent_text = f"{int(self.curr_stg)}%"
        render_text(percent_text, x + width//2 - 10, y + height//2 - 3)

        # Stage text
        stage_text = self.get_growth_stage_text()
        render_text(stage_text, x, y - 15)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)


# --------------------
# Additional HUD Elements
# --------------------
class MoneyDisplay:
    def __init__(self, amount=0):
        self.amount = amount

    def update(self, new_amount):
        self.amount = max(0, new_amount)

    def draw(self, x=600, y=560, width=120, height=25):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 800, 0, 600)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Background
        glColor3f(0.0, 0.3, 0.0)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

        # Border
        glColor3f(0.0, 0.8, 0.0)
        glLineWidth(2)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

        # Money text
        glColor3f(1.0, 1.0, 0.0)  # gold color
        money_text = f"${self.amount:,}"
        render_text(money_text, x + 10, y + height//2 - 3)

        # Label
        glColor3f(1.0, 1.0, 1.0)
        render_text("Money", x + 10, y + height + 5)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)


class TimeDisplay:
    def __init__(self, day=1, hour=6):
        self.day = day
        self.hour = hour

    def update(self, day, hour):
        self.day = day
        self.hour = hour % 24

    def draw(self, x=300, y=560, width=120, height=25):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 800, 0, 600)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Background
        glColor3f(0.1, 0.1, 0.3)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

        # Border
        glColor3f(0.7, 0.7, 1.0)
        glLineWidth(2)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

        # Time text
        glColor3f(1.0, 1.0, 1.0)
        time_text = f"Day {self.day} - {self.hour:02d}:00"
        render_text(time_text, x + 10, y + height//2 - 3)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)