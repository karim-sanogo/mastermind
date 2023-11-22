import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 450, 950
BG_COLOR = (30, 30, 30)
PEG_COLORS = ["red", "blue", "green", "yellow", "purple", "pink", "black", "white"]
PEG_RADIUS = 20
COLOR_PICKER_Y_START = SCREEN_HEIGHT - 2 * (PEG_RADIUS * 2)
TRIES = 10
FEEDBACK_RADIUS = 5
BUTTON_COLOR = (0, 255, 0)
BUTTON_TEXT_COLOR = pygame.Color('white')
BUTTON_RECT = pygame.Rect(350, SCREEN_HEIGHT - 100, 100, 50)
PEG_POSITIONS = [(60 + j * (2 * PEG_RADIUS + 10), SCREEN_HEIGHT - 150 - i * (2 * PEG_RADIUS + 10)) for i in range(TRIES) for j in range(4)]

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mastermind")

# Fonts
pygame.font.init()
font = pygame.font.SysFont('arial', 30)

# Create pegs and placeholders
pegs = {color: pygame.Surface((PEG_RADIUS * 2, PEG_RADIUS * 2), pygame.SRCALPHA) for color in PEG_COLORS}
placeholder = pygame.Surface((PEG_RADIUS * 2, PEG_RADIUS * 2), pygame.SRCALPHA)
pygame.draw.circle(placeholder, (150, 150, 150), (PEG_RADIUS, PEG_RADIUS), PEG_RADIUS)
for color, surf in pegs.items():
    pygame.draw.circle(surf, pygame.Color(color), (PEG_RADIUS, PEG_RADIUS), PEG_RADIUS)

# Game variables
current_row = TRIES - 1
selected_color = None
current_guess = [None] * 4
computer_pick = random.sample(PEG_COLORS, 4)
feedback = [[None] * 4 for _ in range(TRIES)]
dragging = False
dragged_peg = None
dragged_peg_pos = (0, 0)
peg_rects = [pygame.Rect(x, y, PEG_RADIUS * 2, PEG_RADIUS * 2) for x, y in [(50 + PEG_RADIUS * 3 * i, COLOR_PICKER_Y_START) for i in range(4)] + [(50 + PEG_RADIUS * 3 * i, COLOR_PICKER_Y_START + PEG_RADIUS * 2 + 10) for i in range(4)]]
notification_msg = ''
notification_time = 0

def draw_board():
    # Draw the grey placeholders for guesses and feedback for each try
    for i in range(TRIES):
        for j in range(4):  # 4 grey circles for guesses
            pygame.draw.circle(screen, (150, 150, 150),
                               PEG_POSITIONS[i * 4 + j], PEG_RADIUS)
        if i < TRIES - 1:  # Skip the last row for feedback
            for k in range(2):  # 2 smaller grey circles for feedback, in two rows
                for l in range(2):
                    pygame.draw.circle(screen, (150, 150, 150),
                                       (PEG_POSITIONS[i * 4 + 3][0] + 45 + k * (FEEDBACK_RADIUS * 2 + 5),
                                        PEG_POSITIONS[i * 4 + 3][1] - 5 + l * (FEEDBACK_RADIUS * 2 + 5)),
                                        FEEDBACK_RADIUS)

def draw_ui():
    # Draw the "Make Move" button with text
    pygame.draw.rect(screen, BUTTON_COLOR, BUTTON_RECT)
    text_surface = font.render('Make Move', True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=BUTTON_RECT.center)
    screen.blit(text_surface, text_rect.topleft)

    # Draw the color picker pegs in two rows
    for i, rect in enumerate(peg_rects):
        screen.blit(pegs[PEG_COLORS[i]], rect.topleft)

    # Draw notification message
    if notification_msg:
        notification_surf = font.render(notification_msg, True, pygame.Color('red'))
        screen.blit(notification_surf, (50, 10))

def handle_drag_and_drop(event):
    global selected_color, dragging, dragged_peg_surface, current_guess, dragging_from_current_guess
    mouse_pos = pygame.mouse.get_pos()

    if event.type == pygame.MOUSEBUTTONDOWN:
        # Check if the click is on any of the color pegs to start dragging
        for i, rect in enumerate(peg_rects):
            if rect.collidepoint(mouse_pos) and not dragging:
                selected_color = PEG_COLORS[i]
                dragging = True
                dragged_peg_surface = pegs[selected_color].copy()  # Create a copy of the peg surface to drag
                dragging_from_current_guess = False
                return
        # Check if the click is on the current row's pegs to pick up a color
        for i, pos in enumerate(PEG_POSITIONS[current_row * 4:(current_row + 1) * 4]):
            rect = pygame.Rect(pos[0] - PEG_RADIUS, pos[1] - PEG_RADIUS, PEG_RADIUS * 2, PEG_RADIUS * 2)
            if rect.collidepoint(mouse_pos) and not dragging:
                if current_guess[i] is not None:
                    selected_color = current_guess[i]
                    current_guess[i] = None
                    dragging = True
                    dragged_peg_surface = pegs[selected_color].copy()  # Create a copy of the peg surface to drag
                    dragging_from_current_guess = True
                return

    elif event.type == pygame.MOUSEBUTTONUP and dragging:
        # When releasing the mouse button, try to place the peg in the current row
        for i, pos in enumerate(PEG_POSITIONS[current_row * 4:(current_row + 1) * 4]):
            rect = pygame.Rect(pos[0] - PEG_RADIUS, pos[1] - PEG_RADIUS, PEG_RADIUS * 2, PEG_RADIUS * 2)
            if rect.collidepoint(mouse_pos):
                if current_guess[i] is None:  # Only place the peg if the spot is empty
                    current_guess[i] = selected_color
                    break
        dragging = False
        dragged_peg_surface = None

    elif event.type == pygame.MOUSEMOTION and dragging:
        dragged_peg_pos = (mouse_pos[0] - PEG_RADIUS, mouse_pos[1] - PEG_RADIUS)



def check_guess():
    global feedback, current_row, current_guess, notification_msg, notification_time
    if None in current_guess:
        notification_msg = "You must select all 4 colors!"
        notification_time = pygame.time.get_ticks()
    else:
        correct_color = 0
        correct_position = 0
        guess_copy = current_guess[:]
        pick_copy = computer_pick[:]
        # First check for correct color and position
        for i in range(4):
            if guess_copy[i] == pick_copy[i]:
                correct_position += 1
                guess_copy[i] = pick_copy[i] = None
        # Then check for correct color
        for i in range(4):
            if guess_copy[i] and guess_copy[i] in pick_copy:
                correct_color += 1
                pick_copy[pick_copy.index(guess_copy[i])] = None
        # Update feedback for correct guesses
        feedback[current_row] = ['black'] * correct_position + ['white'] * correct_color
        current_row -= 1  # Move to the next row
        current_guess = [None] * 4

# Main loop
running = True
while running:
    screen.fill(BG_COLOR)
    mouse_pos = pygame.mouse.get_pos()  # Update mouse position every frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            handle_drag_and_drop(event)

    if BUTTON_RECT.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
        check_guess()

    # Update notification message
    if notification_msg and pygame.time.get_ticks() - notification_time > 2000:
        notification_msg = ''

    draw_board()
    draw_ui()

    # If we're dragging a peg, blit it at the mouse position
    if dragging and dragged_peg_surface:
        screen.blit(dragged_peg_surface, dragged_peg_pos)

    pygame.display.flip()

pygame.quit()
