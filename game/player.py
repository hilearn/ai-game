import pygame
import threading
from pathlib import Path
from .gameobject import Player, Action, Stats
from .game import Observation, Cell


class RemotePlayer(Player):
    def decide(self):
        self.socket.get_decision()

    def observe(self, sight):
        self.socket.send_sight(sight)


class KeyboardPlayer(Player):
    photos_path = Path(__file__).parent / 'photos'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
            keys = pygame.key.get_pressed()
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
            pygame.event.pump()

    def observe(self, sight):
        input_map = sight.map_._map
        BORDER_SIZE = 25
        WIDTH, HEIGHT = (len(input_map[0]) * sight.cell_size+ 2 * BORDER_SIZE,
                         len(input_map) * sight.cell_size + 2 * BORDER_SIZE)

        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Brutal story of little Ninja")
        background_color = (255, 255, 255)
        FPS = 24

        fence_image_width = pygame.image.load(self.photos_path / 'wooden-fence-transparent-background-isolated-garden-barrier-black-color-simple-illustration-farm-fence-banner-rustic-wall-200961194-removebg-preview.png')
        fence_w = pygame.transform.scale(fence_image_width, (WIDTH, BORDER_SIZE))
        fence_image_height_l = pygame.image.load(self.photos_path / 'left_border.png')
        fence_h_l = pygame.transform.scale(fence_image_height_l, (BORDER_SIZE, HEIGHT - 2 * BORDER_SIZE))
        fence_image_height_h = pygame.image.load(self.photos_path / 'right_border.png')
        fence_h_r = pygame.transform.scale(fence_image_height_h, (BORDER_SIZE, HEIGHT - 2 * BORDER_SIZE))

        barier_image = pygame.image.load(self.photos_path / 'Box.png')
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
            ninja_image = pygame.image.load(self.photos_path / object_.gameobject.image)
            ninja = pygame.transform.scale(ninja_image, object_.size[::-1])
            WIN.blit(ninja, (object_.x + BORDER_SIZE, object_.y + BORDER_SIZE))

        pygame.display.update()


class Bot(Player):
    def __init__(self, strategy, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.strategy = strategy
        self.state = None

    def decide(self):
        return self._parse(self.strategy.decide(bot=self))

    def observe(self, sight: Observation):
        self.state = sight

    @staticmethod
    def _parse(decision: list[float]) -> list[Action]:
        sorted_decision = sorted(range(len(decision)),
                                 key=lambda k: decision[k])
        actions = [Action(sorted_decision[-1])]
        if sorted_decision[-2] == 5:
            actions.append(Action.SHOOT)
        return actions
