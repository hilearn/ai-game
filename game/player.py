import pygame
import threading
import os
from .gameobject import Player, Action, Stats


class RemotePlayer(Player):
    def decide(self):
        self.socket.get_decision()

    def observe(self, sight):
        self.socket.send_sight(sight)


class KeyboardPlayer(Player):
    def __init__(self, stats: Stats):
        super().__init__(stats)
        self.key_pressed = [Action.NOTHING, Action.NOTHING]
        pygame.init()
        listener = threading.Thread(target=self.listener, daemon=True)
        listener.start()

    def decide(self):
        keys = self.key_pressed
        self.key_pressed = [Action.NOTHING, Action.NOTHING]
        return keys

    def listener(self):
        while True:
            keys = pygame.key.get_pressed(sight.map_._map)
            if keys[pygame.K_LEFT]:
                self.key_pressed[0] = Action.MOVE_LEFT
            elif keys[pygame.K_RIGHT]:
                self.key_pressed[0] = Action.MOVE_RIGHT
            elif keys[pygame.K_DOWN]:
                self.key_pressed[0] = Action.MOVE_DOWN
            elif keys[pygame.K_UP]:
                self.key_pressed[0] = Action.MOVE_UP
            elif keys[pygame.K_SPACE]:
                self.key_pressed[1] = Action.SHOOT
            # pygame.event.pump()

    def observe(self, sight):
        input_map = sight.map_._map
        BORDER_SIZE = 25
        WIDTH, HEIGHT = len(input_map[0])+ 2 * BORDER_SIZE, len(input_map) + 2 * BORDER_SIZE
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Brutal story of little Ninja")
        background_color = (255, 255, 255)
        FPS = 24


        fence_image_width = pygame.image.load(os.path.join('photos', 'wooden-fence-transparent-background-isolated-garden-barrier-black-color-simple-illustration-farm-fence-banner-rustic-wall-200961194-removebg-preview.png'))
        fence_w = pygame.transform.scale(fence_image_width, (WIDTH, BORDER_SIZE))
        fence_image_height_l = pygame.image.load(os.path.join('photos', 'left_border.png'))
        fence_h_l = pygame.transform.scale(fence_image_height_l, (BORDER_SIZE, HEIGHT - 2 * BORDER_SIZE))
        fence_image_height_h = pygame.image.load(os.path.join('photos', 'right_border.png'))
        fence_h_r = pygame.transform.scale(fence_image_height_h, (BORDER_SIZE, HEIGHT - 2 * BORDER_SIZE))

        barier_image = pygame.image.load(os.path.join('photos', 'images-removebg-preview.png'))
        barier_size = (sight.cell_size, sight.cell_size)
        barier = pygame.transform.scale(barier_image, barier_size)

        WIN.fill(background_color) 

        WIN.blit(fence_w, (0,0))
        WIN.blit(fence_w, (0,HEIGHT - BORDER_SIZE))
        WIN.blit(fence_h_l, (0, BORDER_SIZE))
        WIN.blit(fence_h_r, (WIDTH - BORDER_SIZE, BORDER_SIZE))

        for i, row in enumerate(input_map):
            for j, cell in enumerate(row):
                if cell == Cell.WALL:
                    top_left_coord = (j * sight.cell_size + BORDER_SIZE, i * sight.cell_size + BORDER_SIZE)
                    WIN.blit(barier, top_left_coord)

        for object_ in sight.objects:
            print(object_)

        pygame.display.update()


class Bot(Player):
    def __init__(self, stats: Stats, strategy):
        super().__init__(stats)
        self.strategy = strategy

    def decide(self):
        return self.parse(self.strategy.decide(self.state))

    def parse(self, decision: list[float]) -> Action:
        pass
