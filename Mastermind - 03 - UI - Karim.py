import pygame
import math
from pygame import gfxdraw
from sys import exit
import random

pygame.init()

class Button:
    def __init__(self, screen, x, y, width, height, text, font_path, font_size, action=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = pygame.freetype.Font(font_path, font_size)
        self.action = action
        self.hovered = False
        self.clicked = False
        self.default_color = (106, 190, 77)
        self.hover_color = (90, 147, 71)
        self.clicked_color = (29, 55, 20)
        self.text_color = (255, 255, 255)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        if self.clicked:
            color = self.clicked_color
        elif self.hovered:
            color = self.hover_color
        else:
            color = self.default_color

        pygame.draw.rect(self.screen, color, self.rect)

        text_lines = self.text.split('\n')
        line_height = self.font.get_sized_height() + 2
        start_y = self.y + (self.height - line_height * len(text_lines)) // 2

        for i, line in enumerate(text_lines):
            text_surf, text_rect = self.font.render(line, self.text_color)
            text_rect.centerx = self.rect.centerx
            text_rect.y = start_y + i * line_height
            self.screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos) and self.clicked:
                self.clicked = False
                if all_circles_filled(rows[active_row]):  # Check if all circles are filled before making a move
                    self.action()
                else:
                    print("Not all circles are filled!")  # Provide feedback to the player
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

class RoundCircle:
    def __init__(self, screen, x, y, r, color):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def draw_circle(self):
        # Prettier circles than pygame.draw.circle
        gfxdraw.filled_circle(self.screen, self.x, self.y, self.r, self.color)
        gfxdraw.aacircle(self.screen, self.x, self.y, self.r, self.color)

    def update_circle(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def is_clicked(self, mouse_pos):
        distance = math.sqrt((self.x - mouse_pos[0]) ** 2 + (self.y - mouse_pos[1]) ** 2)
        return distance <= self.r


class CircleRow:
    def __init__(self, screen, start_y, big_radius, small_radius, color, start_x=80, big_gap=10, small_gap=10, small_big_gap=30, include_small=True):
        self.screen = screen
        self.start_y = start_y
        self.big_radius = big_radius
        self.small_radius = small_radius
        self.color = color
        self.start_x = start_x
        self.big_gap = big_gap
        self.small_gap = small_gap
        self.include_small = include_small
        self.circles = []

        for i in range(4):
            x = start_x + i * (2 * big_radius + big_gap)
            self.circles.append(RoundCircle(screen, x, start_y, big_radius, color))

        # Create a separate list for hint circles
        self.hint_circles = []
        if include_small:
            small_start_x = start_x + 4 * (2 * big_radius) + small_big_gap
            # Create hint circles
            for i in range(4):
                x = small_start_x + (i % 2) * (2 * small_radius + small_gap)
                y_offset = 0 if i < 2 else -2 * small_radius - small_gap
                self.hint_circles.append(RoundCircle(screen, x, start_y + 16 + y_offset, small_radius, color))


    def draw(self):
        for circle in self.circles + self.hint_circles:  # Zeichnen aller Kreise, einschließlich der Hinweiskreise
            circle.draw_circle()

screen = pygame.display.set_mode((450, 950))

pygame.display.set_caption("Mastermind")
pygame.display.set_icon(pygame.image.load("Mastermind/Assets/Images/mastermind_icon.png"))

clock = pygame.time.Clock()

header_font = pygame.freetype.Font("Mastermind/Assets/Fonts/Inter-Bold.ttf", 20)
header_title, header_rect = header_font.render("MASTERMIND", (255, 255, 255))

header = pygame.Surface((450, 53))
header.fill(("#4F4F4F"))

header_arrow = pygame.image.load("Mastermind/Assets/Images/back-arrow.png")

clr_store = pygame.Surface((290, 150))
clr_store.fill(("#4F4F4F"))

blue = RoundCircle(screen, 80, 813, 30, (10, 156, 170))
orange = RoundCircle(screen, 150, 813, 30, (255, 142, 20))
red = RoundCircle(screen, 220, 813, 30, (255, 82, 93))
purple = RoundCircle(screen, 290, 813, 30, (134, 79, 172))
dark_green = RoundCircle(screen, 80, 883, 30, (1, 95, 77))
light_green = RoundCircle(screen, 150, 883, 30, (80, 185, 72))
black = RoundCircle(screen, 220, 883, 30, (0, 0, 0))
white = RoundCircle(screen, 290, 883, 30, (255, 255, 255))

colors = [blue, orange, red, purple, dark_green, light_green, black, white]
tries = 10

def generate_secret_code(color_objects):
    color_values = [obj.color for obj in color_objects]
    return random.sample(color_values, 4)

# Funktion, um die Übereinstimmungen zu überprüfen
def check_guess(guess, secret_code):
    result = {'black': 0, 'white': 0}  # Schwarz für richtige Farbe und Position, Weiß für nur richtige Farbe
    temp_secret_code = list(secret_code)  # Temporäre Kopie, um Treffer zu markieren

    # Überprüfen Sie zuerst auf exakte Treffer (Schwarz)
    for i in range(len(guess)):
        if guess[i] == temp_secret_code[i]:
            result['black'] += 1
            temp_secret_code[i] = None  # Markieren Sie diesen Treffer, um Doppelzählungen zu vermeiden

    # Überprüfen Sie auf richtige Farbe, aber falsche Position (Weiß)
    for i in range(len(guess)):
        if guess[i] in temp_secret_code and guess[i] != secret_code[i]:
            result['white'] += 1
            temp_secret_code[temp_secret_code.index(guess[i])] = None  # Markieren Sie diesen Treffer

    return result

# Erzeugen Sie den Secret Code beim Start des Spiels
secret_code_colors = generate_secret_code(colors)

# Function to check if all large circles in the active row are filled with color
def all_circles_filled(row):
    default_color = (54, 54, 54)  # Annahme, dass dies die Standardfarbe ist
    return all(circle.color != default_color for circle in row.circles[:4])  # Assuming (54, 54, 54) is the default color

# Funktion, um das Ergebnis in den kleinen Kreisen anzuzeigen
def display_result(row_number, result):
    # Mischen der Ergebnisse, um eine zufällige Reihenfolge zu erhalten
    results = ['black'] * result['black'] + ['white'] * result['white']
    random.shuffle(results)
    
    # Anzeigen der Ergebnisse in den kleinen Kreisen
    for i, res in enumerate(results):
        color = (0, 0, 0) if res == 'black' else (255, 255, 255)
        rows[row_number].hint_circles[i].color = color
    
    # Nicht verwendete kleine Kreise auf Standardfarbe setzen
    for i in range(len(results), 4):
        rows[row_number].hint_circles[i].color = (54, 54, 54)

# Funktion, um den geheimen Code in der obersten Reihe anzuzeigen
def display_secret_code(secret_code_colors):
    for i, color in enumerate(secret_code_colors):
        rows[9].circles[i].color = color

game_over = False

# Refactored make_move function for better readability and logic flow
def make_move():
    global active_row  # Access the global active_row variable
    active_row_circles = rows[active_row].circles[:4]  # Reference to the large circles in the active row
    
    if not all_circles_filled(rows[active_row]):
        print("Not all fields are filled!")  # Replace with actual feedback in your game
        return  # Exit the function if not all circles are filled
    
    guess = [circle.color for circle in active_row_circles]  # Get colors of the filled circles
    result = check_guess(guess, secret_code_colors)
    
    # Visualize the result in the hint circles
    hint_circles = rows[active_row].hint_circles  # Reference to the hint circles in the active row
    # Reset hint circles to default color before applying new hints
    for hint_circle in hint_circles:
        hint_circle.color = (54, 54, 54)
        
    hints = ['black'] * result['black'] + ['white'] * result['white']
    for i, hint in enumerate(hints):
        hint_color = (0, 0, 0) if hint == 'black' else (255, 255, 255)
        hint_circles[i].color = hint_color
    
    # Überprüfen der Farben und Anzeigen der Ergebnisse
    guess = [circle.color for circle in rows[active_row].circles[:4]]
    result = check_guess(guess, secret_code_colors)
    display_result(active_row, result)

    # Überprüfen Sie, ob das Spiel vorbei ist (der Code erraten wurde)
    if result['black'] == 4:
        display_secret_code(secret_code_colors)
        game_over = True  # Spielende, wenn der Code erraten wurde
        return

    # Wechseln Sie zur nächsten Reihe, wenn das Spiel noch nicht vorbei ist
    if active_row < tries - 2:
        active_row += 1
    else:
        # Zeigen Sie den geheimen Code in der obersten Reihe an, wenn alle Versuche aufgebraucht sind
        display_secret_code(secret_code_colors)
        game_over = True  # Spielende, wenn alle Versuche aufgebraucht sin


make_move_button = Button(
    screen, x=340, y=773, width=60, height=150,
    text="MAKE\nMOVE",
    font_path="Mastermind/Assets/Fonts/Inter-Bold.ttf",
    font_size=10,
    action=make_move
)


for color in colors:
    color.dragging = False
    color.original_position = (color.x, color.y)
    color.drag_offset = (0, 0)

rows = []
y_start = 733
big_radius = 30
small_radius = 12
row_gap = 70

active_row = 0

for i in range(tries):
    # Last row doesn't have small circles
    include_small = i < 9
    row = CircleRow(screen, y_start - i * row_gap, big_radius, small_radius, (54, 54, 54), include_small=include_small)
    rows.append(row)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for color in colors:
                    if color.is_clicked(event.pos):
                        color.dragging = True
                        color.drag_offset = (color.x - event.pos[0], color.y - event.pos[1])
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for color in colors:
                    if color.dragging:
                        color.dragging = False
                        # Erlaube das Platzieren von Farben nur, wenn das Spiel nicht vorbei ist und nicht in der obersten Reihe
                        if not game_over and active_row < tries - 1:
                            for circle in rows[active_row].circles[:4]:
                                if circle.is_clicked(event.pos):
                                    circle.update_circle(circle.x, circle.y, circle.r, color.color)
                        color.x, color.y = color.original_position

        elif event.type == pygame.MOUSEMOTION:
            for color in colors:
                if color.dragging:
                    color.x = event.pos[0] + color.drag_offset[0]
                    color.y = event.pos[1] + color.drag_offset[1]
        make_move_button.handle_event(event)
    
    if make_move_button.clicked:  # Wenn der Button geklickt wurde
        make_move_button.action()  # Rufen Sie die Aktion des Buttons auf
        make_move_button.clicked = False  # Setzen Sie den Status zurück

    screen.fill(("#252525"))
    screen.blit(header, (0, 0))
    screen.blit(header_title, (156, 19))
    screen.blit(header_arrow, (23, 18))
    screen.blit(clr_store, (40, 773))

    make_move_button.draw()

    blue.draw_circle()
    orange.draw_circle()
    red.draw_circle()
    purple.draw_circle()
    dark_green.draw_circle()
    light_green.draw_circle()
    black.draw_circle()
    white.draw_circle()
    
    for color in colors:
        if not color.dragging:  # Only draw the color if not currently being dragged
            color.draw_circle()
    
    for row in rows:
        row.draw()

    # If dragging a color, draw it on top
    for color in colors:
        if color.dragging:
            color.draw_circle()
    
    pygame.display.update()
    clock.tick(60)