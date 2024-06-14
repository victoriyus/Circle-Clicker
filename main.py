"""
Date: 06/14/2024
Name: Circle Clicker
Description: A game where you click the falling circles to the beat
"""
import pygame
import button_class
import song

pygame.init()
pygame.mixer.init()
pygame.font.init()

# Defining the colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 105, 105)
GREEN = (105, 255, 105)
BLUE = (105, 105, 255)

# Dimensions
x = 1280
y = 960

# Setting the logo
# pygame.display.set_icon(pygame.image.load("resources/logo.png"))

# Setting the window name
pygame.display.set_caption("Rhythm Game")

# Setting the display surface
display_surface = pygame.display.set_mode((x, y))

# Initializing images
titleImage = pygame.image.load("res/images/title.png")
playImage = pygame.image.load("res/images/play_button.png")
menuImage = pygame.image.load("res/images/menu_button.png")
clickImageD = pygame.image.load("res/images/click_goal_d.png")
clickImageF = pygame.image.load("res/images/click_goal_f.png")
clickImageJ = pygame.image.load("res/images/click_goal_j.png")
clickImageK = pygame.image.load("res/images/click_goal_k.png")

noteImages = [pygame.image.load("res/images/note_red.png"),
              pygame.image.load("res/images/note_blue.png"),
              pygame.image.load("res/images/note_green.png"),
              pygame.image.load("res/images/note_yellow.png")]

# Initializing fonts
general_font = pygame.font.Font("res/fonts/AldotheApache.ttf", 40)
results_font = pygame.font.Font("res/fonts/AldotheApache.ttf", 60)
results_title_font = pygame.font.Font("res/fonts/AldotheApache.ttf", 80)

# Initializing buttons
playButton = button_class.clickableButton(
    x / 2, y * 4/5, playImage, 0.5, display_surface)

playButtonHover = button_class.clickableButton(
    playButton.x, playButton.y, playImage, 0.6, display_surface)

menuButton = button_class.clickableButton(
    x / 2, y * 4/5, menuImage, 0.5, display_surface)

menuButtonHover = button_class.clickableButton(
    menuButton.x, menuButton.y, menuImage, 0.6, display_surface)

gameClickButton0 = button_class.Button(
    2/7 * x, y * 3/4, clickImageD, 2, display_surface)

gameClickButton1 = button_class.Button(
    3/7 * x, y * 3/4, clickImageF, gameClickButton0.scale, display_surface)

gameClickButton2 = button_class.Button(
    4/7 * x, y * 3/4, clickImageJ, gameClickButton0.scale, display_surface)

gameClickButton3 = button_class.Button(
    5/7 * x, y * 3/4, clickImageK, gameClickButton0.scale, display_surface)

# Game values
screen_notes = []
current_notes = []
index = -1
score = 0
combo = 0
max_combo = 0
misses = 0
stall = True
start_time = None
song_started = False
pixels_offset_per_frame = 13
delay = 720 / pixels_offset_per_frame / 60 * 1000
last_index_count = 0
current_song = song.song_1

# Setting the default scene to menu
scene = "menu"

# dictionary of active keys
activated_keys = {"d": False, "f": False, "j": False, "k": False}

# Making a pygame clock object to limit fps
clock = pygame.time.Clock()


# Scene for initializing the song when a level is loaded
def initialize_song(song):

    global scene

    pygame.mixer.music.load(f"res/songs/{song.name}/{song.name}.mp3")

    pygame.mixer.music.play(start=song.offset)

    scene = "game"


# Scene for the results after a level is completed
def results():

    # globals
    global screen_notes, current_notes, index, score, combo, max_combo, misses
    global scene, stall, start_time, song_started, pixels_offset_per_frame, delay
    global last_index_count

    # Black background
    display_surface.fill(BLACK)

    # Results text
    results_title_surface = results_title_font.render(
        "RESULTS", False, WHITE)
    results_title_rect = pygame.Rect(
        0, 0, results_title_surface.get_width(), results_title_surface.get_height())
    results_title_rect.center = (x // 2, int(y * 1/6))

    # Combo text
    max_combo_surface = results_font.render(
        f"Max Combo Achieved: {max_combo}", False, RED)
    max_combo_rect = pygame.Rect(
        0, 0, max_combo_surface.get_width(), max_combo_surface.get_height())
    max_combo_rect.center = (
        x // 2, int(y * 1/3))

    # Misses text
    misses_surface = results_font.render(
        f"Misses Achieved: {misses}", False, BLUE)
    misses_rect = pygame.Rect(
        0, 0, misses_surface.get_width(), misses_surface.get_height())
    misses_rect.center = (x // 2, int(y * 1/3 + y * 1/10))

    # Score text
    score_surface = results_font.render(
        f"Score Achieved: {int(score)}", False, GREEN)
    score_rect = pygame.Rect(
        0, 0, score_surface.get_width(), score_surface.get_height())
    score_rect.center = (x // 2, int(y * 1/3 + y * 2/10))

    # Displaying
    display_surface.blit(results_title_surface, results_title_rect)
    display_surface.blit(score_surface, score_rect)
    display_surface.blit(max_combo_surface, max_combo_rect)
    display_surface.blit(misses_surface, misses_rect)

    # Button hovering + click logic
    if menuButton.hover() == False:

        menuButton.draw()

    else:

        menuButtonHover.draw()

    if menuButton.click():

        scene = "menu"
        screen_notes = []
        current_notes = []
        index = -1
        score = 0
        combo = 0
        max_combo = 0
        misses = 0
        stall = True
        start_time = None
        song_started = False
        pixels_offset_per_frame = 13
        delay = 720 / pixels_offset_per_frame / 60 * 1000
        last_index_count = 0


# Menu scene
def menu():

    # globals
    global scene

    # black background
    display_surface.fill(BLACK)

    # Display title image
    display_surface.blit(titleImage, (x / 2 - 400, y * 1/10))

    # Button hovering + click logic
    if playButton.hover() == False:

        playButton.draw()

    else:

        playButtonHover.draw()

    if playButton.click():

        scene = "game"


# Game scene
def game(song):

    # globals
    global screen_notes, scene, current_notes, activated_keys, index, stall
    global start_time, song_started, delay, last_index_count, combo
    global score, max_combo, misses

    # Black background
    display_surface.fill(BLACK)

    # changes last index variable to last frame's index
    last_index = index

    # Checks if stalling
    if stall:

        # if a start_time hasn't been set, use current time
        if not start_time:

            start_time = pygame.time.get_ticks()

        else:

            difference = pygame.time.get_ticks() - start_time

            # If stalling before the song starts, use difference to calculate index
            if not song_started:

                index = int((difference) / 60000 * song.bpm * 4)

            # Else use song position + difference
            else:

                index = int((pygame.mixer.music.get_pos() + difference) /
                            60000 * song.bpm * 4 + len(song.note_list))

            # if the stall time is over, start the song and reset variables
            if difference > delay:

                if not song_started:

                    song_started = True
                    scene = "initialize_song"
                    delay = 720 / pixels_offset_per_frame / 60 * 1000 * 1.2
                else:

                    delay = 720 / pixels_offset_per_frame / 60 * 1000

                stall = False

                start_time = None

    # If not stalling, use song to calculate index
    else:

        index = int((pygame.mixer.music.get_pos() +
                     delay) / 60000 * song.bpm * 4)

    # If the index has changed
    if last_index != index:

        # Get the current notes
        current_notes = song.get_current_notes(index)

        # If the song is over and the gameplay isn't stalling, go to the results screen
        if pygame.mixer.music.get_pos() == -1 and not stall:

            scene = "results"
            return

        # If the end hasn't been reached, create game notes and append them to the current note list
        for i in range(len(current_notes)):

            if current_notes[i] == 1:

                current_button = button_class.gameButton(
                    i, (2+i)/7 * x, 0, noteImages[i], 1, display_surface)

                screen_notes.append(current_button)

    # Draw game threshold buttons (buttons where you click the falling notes)
    gameClickButton0.draw()
    gameClickButton1.draw()
    gameClickButton2.draw()
    gameClickButton3.draw()

    # create/reset variables
    new_screen_notes = []

    # Checks if a note was hit or missed + figures out which notes should be deleted
    for i in range(len(screen_notes)):

        alive = True

        currentCenter = screen_notes[i].rect.center

        # If note is within click range
        if currentCenter[1] > y*3/4 - y*1/16 and currentCenter[1] < y*3/4 + y*1/16:

            # Get pressed keys state
            keys = list(activated_keys.keys())

            # Add combo/score if a note has been clicked
            for j in range(len(activated_keys.keys())):

                if activated_keys[keys[j]] == True and screen_notes[i].index == j:

                    activated_keys[keys[j]] = False
                    alive = False
                    score += 300 * 1.05**combo
                    combo += 1

        # If a note is still alive after reaching click threshold, break combo
        elif currentCenter[1] > y*3/4 + y * 1/12 and screen_notes[i].has_broken_combo() == False:

            combo = 0
            misses += 1

        # Delete note if no longer on screen
        if currentCenter[1] > y:

            alive = False

        # Keep alive notes
        if alive:

            new_screen_notes.append(screen_notes[i])

        # Track max combo
        if combo > max_combo:

            max_combo = combo

    # update screen notes
    screen_notes = new_screen_notes

    # draw updated screen notes
    for i in screen_notes:

        currentCenter = i.rect.center
        i.move(currentCenter[0], currentCenter[1] + pixels_offset_per_frame)
        i.draw()

    # Combo and score
    combo_surface = general_font.render(f"COMBO: {combo}x", False, WHITE)
    score_surface = general_font.render(f"SCORE: {int(score)}", False, WHITE)
    display_surface.blit(combo_surface, (40, y - 80))
    display_surface.blit(score_surface, (40, 40))


# Main loop
while True:

    # Limit fps to 60
    clock.tick(60)

    # Choose correct scene
    if scene == "menu":

        menu()

    elif scene == "game":

        game(current_song)

    elif scene == "initialize_song":

        initialize_song(current_song)

    elif scene == "results":

        results()

    for event in pygame.event.get():

        # Input
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_d:
                # implement in 1 sec
                activated_keys["d"] = True
            if event.key == pygame.K_f:
                # implement in 1 sec
                activated_keys["f"] = True
            if event.key == pygame.K_j:
                # implement in 1 sec
                activated_keys["j"] = True
            if event.key == pygame.K_k:
                # implement in 1 sec
                activated_keys["k"] = True

        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_d:
                # implement in 1 sec
                activated_keys["d"] = False
            if event.key == pygame.K_f:
                # implement in 1 sec
                activated_keys["f"] = False
            if event.key == pygame.K_j:
                # implement in 1 sec
                activated_keys["j"] = False
            if event.key == pygame.K_k:
                # implement in 1 sec
                activated_keys["k"] = False

        elif event.type == pygame.QUIT:

            pygame.quit()
            quit()

    pygame.display.update()
