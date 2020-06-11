from modules.class_rectangle import Rectangle
from time import sleep
import threading
import logging
WRITE_LOG_TO_FILE = False
LOG_FORMAT = '%(name)s (%(levelname)s) %(asctime)s: %(message)s'
# LOG_LEVEL = logging.DEBUG
LOG_LEVEL = logging.INFO
# LOG_LEVEL = logging.WARNING

if WRITE_LOG_TO_FILE:
    logging.basicConfig(filename='jarvis_log.txt', filemode='w', format=LOG_FORMAT, level=LOG_LEVEL,
                        datefmt='%d.%m.%y %H:%M:%S')
else:
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL, datefmt='%d.%m.%y %H:%M:%S')

class Laser(Rectangle):
    logger = logging.getLogger('laser')

    def __init__(self, x_min, x_max, y_min, y_max):
        super().__init__(x_min, x_max, y_min, y_max)
        self._laser_on = False
        self._game_mode = False
        self._game_thread = threading.Thread(target=self.game, args=(), daemon=True)
        self._game_thread.start()

    @property
    def game_mode(self):
        return self._game_mode

    def rev_laser(self):
        self._laser_on = not self._laser_on
        if self._laser_on:
            self.logger.info('laser ON')
            return 'on'
        else:
            self.logger.info('laser OFF')
            return 'off'

    def rev_game_mode(self):
        self._game_mode = not self._game_mode
        if self._game_mode:
            self.logger.info('game mode ON')
        else:
            self.logger.info('game mode OFF')

    def move_axis_to_coord(self, x, y, speed_x, speed_y):
        x = self.check_values(x, self._x_min, self._x_max)
        y = self.check_values(y, self._y_min, self._y_max)
        while self.game_mode and (abs(self.x - x) >= speed_x or abs(self.y - y) >= speed_y):
            if self.x< x:
                self.x += speed_x
            elif self.x > x:
                self.x -= speed_x

            if self.y < y:
                self.y += speed_y
            elif self.y > y:
                self.y -= speed_y
            sleep(0.03)

    def move_axis(self, direction, speed_x, speed_y):
        if direction == 'up':
            self.y += speed_y
        elif direction == 'down':
            self.y -= speed_y
        elif direction == 'left':
            self.x += speed_x
        elif direction == 'right':
            self.x -= speed_x
        sleep(0.01)

    def game(self):
        while True:
            if self.game_mode:
                self.move_axis_to_coord(144, 150, 2, 2)
                self.move_axis_to_coord(132, 135, 3, 3)
                self.move_axis_to_coord(108, 130, 2, 2)
                self.move_axis_to_coord(48, 130, 2, 2)
                self.move_axis_to_coord(42, 95, 1,1)
                self.move_axis_to_coord(88, 55, 2, 2)
                self.move_axis_to_coord(159, 100, 3, 3)
                self.move_axis_to_coord(150, 140, 2, 2)
                self.move_axis_to_coord(123, 55, 2, 2)
                # self.logger.info('alive')
            sleep(0.001)