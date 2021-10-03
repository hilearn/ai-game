import pygame
import threading
from pathlib import Path
from .gameobject import Player, Action, Stats, Weapon
from .game import Observation, Cell


class RemotePlayer(Player):
    def decide(self):
        self.socket.get_decision()

    def observe(self, sight):
        self.socket.send_sight(sight)


class KeyboardPlayer(Player):
    BORDER_SIZE = 25
    photos_path = Path(__file__).parent / 'photos'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key_pressed = [Action.NOTHING, Action.NOTHING]
        self.loaded = False
        pygame.init()
        listener = threading.Thread(target=self.listener, daemon=True)
        listener.start()

    def decide(self):
        keys = self.key_pressed
        self.key_pressed = [Action.NOTHING, Action.NOTHING]
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    keys[1] = Action.SHOOT
                if keys[0] != Action.NOTHING:
                    break
                if event.key == pygame.K_LEFT:
                    keys[0] = Action.MOVE_LEFT
                elif event.key == pygame.K_RIGHT:
                    keys[0] = Action.MOVE_RIGHT
                elif event.key == pygame.K_UP:
                    keys[0] = Action.MOVE_UP
                elif event.key == pygame.K_DOWN:
                    keys[0] = Action.MOVE_DOWN
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
            if keys[pygame.K_SPACE]:
                self.key_pressed[1] = Action.SHOOT

    def load(self, sight):
        if self.loaded:
            return
        input_map = sight.map_._map
        self.WIDTH, self.HEIGHT = (
            len(input_map[0]) * sight.cell_size + 2 * self.BORDER_SIZE,
            len(input_map) * sight.cell_size + 2 * self.BORDER_SIZE
        )

        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Brutal story of little Ninja")
        FPS = 24

        self.fence_image_width = pygame.image.load(self.photos_path / 'wooden-fence-transparent-background-isolated-garden-barrier-black-color-simple-illustration-farm-fence-banner-rustic-wall-200961194-removebg-preview.png')
        self.fence_w = pygame.transform.scale(
            self.fence_image_width,
            (self.WIDTH, self.BORDER_SIZE))
        self.fence_image_height_l = pygame.image.load(self.photos_path / 'left_border.png')
        self.fence_h_l = pygame.transform.scale(
            self.fence_image_height_l,
            (self.BORDER_SIZE, self.HEIGHT - 2 * self.BORDER_SIZE))
        self.fence_image_height_h = pygame.image.load(self.photos_path / 'right_border.png')
        self.fence_h_r = pygame.transform.scale(
            self.fence_image_height_h,
            (self.BORDER_SIZE, self.HEIGHT - 2 * self.BORDER_SIZE))

        self.barier_image = pygame.image.load(self.photos_path / 'Box.png')
        self.barier_size = (sight.cell_size, sight.cell_size)
        self.barier = pygame.transform.scale(self.barier_image, self.barier_size)

        self.images = {}
        self.locations = {}
        self.angles = {}
        self.loaded = True
    
    def get_image(self, object_, angle):
        if object_.gameobject.image not in self.images:
            image = pygame.image.load(self.photos_path / object_.gameobject.image)
            self.images[object_.gameobject.image] = pygame.transform.scale(
                image,
                object_.size[::-1]
            )
        if (object_.gameobject.image, angle) not in self.images:
            image = pygame.transform.rotate(
                self.images[object_.gameobject.image],
                angle
            )
            self.images[object_.gameobject.image, angle] = image
        return self.images[object_.gameobject.image, angle]

    def observe(self, sight):
        self.load(sight)

        background_color = (255, 255, 255)
        self.WIN.fill(background_color) 

        self.WIN.blit(self.fence_w, (0, 0))
        self.WIN.blit(self.fence_w, (0, self.HEIGHT - self.BORDER_SIZE))
        self.WIN.blit(self.fence_h_l, (0, self.BORDER_SIZE))
        self.WIN.blit(self.fence_h_r, (self.WIDTH - self.BORDER_SIZE, self.BORDER_SIZE))
        for i, row in enumerate(sight.map_._map):
            for j, cell in enumerate(row):
                if cell == Cell.WALL:
                    top_left_coord = (j * sight.cell_size + self.BORDER_SIZE,
                                      i * sight.cell_size + self.BORDER_SIZE)
                    self.WIN.blit(self.barier, top_left_coord)

        new_angles = {}

        for object_ in sight.objects:
            action = object_.direction.to_action()
            if isinstance(object_.gameobject, Weapon):
                if id(object_) not in self.angles:
                    angle = 0
                else:
                    angle = self.angles[id(object_)] + 12
                new_angles[id(object_)] = angle
            elif action == Action.MOVE_LEFT:
                angle = 0
            elif action == Action.MOVE_RIGHT:
                angle = 180
            elif action == Action.MOVE_DOWN:
                angle = 90
            elif action == Action.MOVE_UP:
                angle = 270

            image = self.get_image(object_, angle)
            self.WIN.blit(image,
                          (object_.x + self.BORDER_SIZE,
                           object_.y + self.BORDER_SIZE))

        self.angles = new_angles

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
