from const import *

class Default(object):
    def __init__(self) -> None:
        self.timer = 0
        self.scatter()

    def update(self, dt) -> None:
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is SCATTER:
                self.chase()
            elif self.mode is CHASE:
                self.scatter()

    def scatter(self) -> None:
        self.mode = SCATTER
        self.time = 10
        self.timer = 0

    def chase(self) -> None:
        self.mode = CHASE
        self.time = 23
        self.timer = 0


class ContollerOfModes(object):
    def __init__(self, entity) -> None:
        self.timer = 0
        self.time = None
        self.default = Default()
        self.current = self.default.mode
        self.entity = entity

    def update(self, dt) -> None:
        self.default.update(dt)
        self.current = self.default.mode
