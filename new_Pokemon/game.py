import pygame
import pytmx
import pyscroll
import time
from player import Player
from player2 import Player2


class Game:

    def __init__(self):

        self.screen2 = pygame.display.set_mode((800, 810))
        pygame.display.set_caption("Pokemon shooter")

        tmx_data = pytmx.util_pygame.load_pygame('new_Pokemon\carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, self.screen2.get_size())
        map_layer.zoom = 1

        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)
        player2_position = tmx_data.get_object_by_name("player2")
        self.player2 = Player2(player2_position.x, player2_position.y)

        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(
                    obj.x, obj.y, obj.width, obj.height))

        self.group = pyscroll.PyscrollGroup(
            map_layer=map_layer, default_layer=5)
        self.group.add(self.player)
        self.group.add(self.player2)

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        

        if pressed[pygame.K_UP]:
            print('haut')
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            print('bas')
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT]:
            print('gauche')
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            print('droite')
            self.player.move_right()
            self.player.change_animation('right')

        if pressed[pygame.K_w]:
            print('haut')
            self.player2.move_up()
            self.player2.change_animation('up')
        elif pressed[pygame.K_s]:
            print('bas')
            self.player2.move_down()
            self.player2.change_animation('down')
        elif pressed[pygame.K_q]:
            print('gauche')
            self.player2.move_left()
            self.player2.change_animation('left')
        elif pressed[pygame.K_d]:
            print('droite')
            self.player2.move_right()
            self.player2.change_animation('right')

    def update(self):
        self.group.update()

        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.player.save_location()
            self.player2.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect)
            # self.group.center(self.player2.rect)

            # self.group.draw(self.screen)
            self.group.draw(self.screen2)

            # self.group.zoom(0)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)
        pygame.quit()
