__all__ = ['main']

import pygame
import pygame_menu
from pygame_menu.examples import create_example_window

from random import randrange
from typing import Tuple, Any, Optional, List
import os
import database
global name1  
global name2 
truc = {
    "nom":"",
    "a":""
}
# Constants and global variables

DIFFICULTY = ['Pokemon shooter']
FPS = 60
WINDOW_SIZE = (690, 480)
dif = ""

clock: Optional['pygame.time.Clock'] = None
main_menu: Optional['pygame_menu.Menu'] = None
surface: Optional['pygame.Surface'] = None


def change_difficulty(value: Tuple[Any, int], difficulty: str) -> None:
    
    selected, index = value
    print(f'Selected difficulty: "{selected}" ({difficulty}) at index {index}')
    DIFFICULTY[0] = difficulty
   


def random_color() -> Tuple[int, int, int]:
  
    return randrange(0, 255), randrange(0, 255), randrange(0, 255)


def play_function(difficulty: List, font: 'pygame.font.Font', test: bool = False) -> None:
    
    assert isinstance(difficulty, list)
    difficulty = difficulty[0]
    
    assert isinstance(difficulty, str)

    # Define globals
    global main_menu
    global clock

    if difficulty == 'Pokemon shooter':
       os.system('py ./new_Pokemon/main.py')
    elif difficulty == 'TRON':
        os.system('py ./tron.py')
    elif difficulty == 'PONG':
        os.system('py ./pong.py')
    elif difficulty == 'MINECRAFT':    
        os.system('py ./main.py')
    else:
        raise ValueError(f'unknown difficulty {difficulty}')

    
def MyTextValue(name):
    
    if name != "":
        truc['nom'] = name      
def MyTextValue2(name):
    
    if name != "":
        truc["a"] = name   
def insert():
    
    task = (truc["nom"], truc["a"])
    datas = database.Database().create_rq_insert_joueur(task) 
                
    

def main_background() -> None:
    """
    Function used by menus, draw on background while menu is active.
    """
    global surface
    surface.fill((128, 0, 128))


def main(test: bool = False) -> None:
    
    """
    Main program.
    :param test: Indicate function is being tested
    """

    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global clock
    global main_menu
    global surface

    # -------------------------------------------------------------------------
    # Create window
    # -------------------------------------------------------------------------
    surface = create_example_window('Arcade Game', WINDOW_SIZE)
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Create menus: Play Menu
    # -------------------------------------------------------------------------
    play_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        title='Play Menu',
        
        width=WINDOW_SIZE[0] * 0.75
    )

    submenu_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    submenu_theme.widget_font_size = 15
   
    joueur_menus= pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.5,
        theme=submenu_theme,
        title='joueurmenu',
        width=WINDOW_SIZE[0] * 0.7
    )
    
    joueur_menus.add.text_input('Name :', default='player 1', onchange= MyTextValue)
    joueur_menus.add.text_input('Name 2 :', default='player 2', onchange= MyTextValue2)
    joueur_menus.add.button('ok',insert)
    poke_menu= pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.9,
        theme=submenu_theme,
        title='pokescore',
        width=WINDOW_SIZE[0] * 0.7
    )
    tron= pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.9,
        theme=submenu_theme,
        title='tron',
        width=WINDOW_SIZE[0] * 0.7
    )
    pong= pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.9,
        theme=submenu_theme,
        title='pong',
        width=WINDOW_SIZE[0] * 0.7
    )
    score_menu=pygame_menu.Menu(
        height=WINDOW_SIZE[1]*0.9,
        theme=submenu_theme,
        title='score',
        width=WINDOW_SIZE[0]*0.7
    )
    score_menu.add.button('pokescore', poke_menu)
    score_menu.add.button('pongscore', pong)
    score_menu.add.button('tronscore', tron)
    
    data = database.Database().select("pokemonshooter", "victoire, score_victoire")
    for dat in data:
        poke_menu.add.button(dat)
    data2 = database.Database().select("pong", "victoire, score_victoire")
    for dat2 in data2:
        pong.add.button(dat2)
    data3 = database.Database().select("tron", "victoire, score_victoire")
    for dat3 in data3:
        tron.add.button(dat3)
    
    play_submenu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.5,
        theme=submenu_theme,
        title='Submenu',
        width=WINDOW_SIZE[0] * 0.7
    )
    
    for i in range(30):
        play_submenu.add.button(f'Back {i}', pygame_menu.events.BACK)
    play_submenu.add.button('Return to main menu', pygame_menu.events.RESET)

    play_menu.add.button('Start',  # When pressing return -> play(DIFFICULTY[0], font)
                         play_function,
                         DIFFICULTY,
                         pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))
    play_menu.add.selector('Select game ',
                           [('1 - Pokemon', 'Pokemon shooter'),
                            ('2 - Tron', 'TRON'),
                            ('3 - Pong', 'PONG'),
                            ('4 - Minecraft', 'MINECRAFT')],
                           onchange=change_difficulty,
                           selector_id='select_difficulty')
    
        
        
    play_menu.add.button('Return to main menu', pygame_menu.events.BACK)

    
    about_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    about_theme.widget_margin = (0, 0)

    

    

    # -------------------------------------------------------------------------
    # Create menus: Main
    # -------------------------------------------------------------------------
    main_theme = pygame_menu.themes.THEME_DEFAULT.copy()

    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.6,
        theme=main_theme,
        title='Main Menu',
        width=WINDOW_SIZE[0] * 0.6
    )

    main_menu.add.button('Play', play_menu)
    main_menu.add.button('Scores', score_menu)
    main_menu.add.button('nom des joueurs', joueur_menus)
    main_menu.add.button('Quit', pygame_menu.events.EXIT)
    

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Main menu
        if main_menu.is_enabled():
            main_menu.mainloop(surface, main_background, disable_loop=test, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()