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
        print(f"Default mode: {self.mode}, Timer: {self.timer}, Time: {self.time}")


    def scatter(self) -> None:
        self.mode = SCATTER
        self.time = 7
        self.timer = 0
        print("Switching to SCATTER mode")

    def chase(self) -> None:
        self.mode = CHASE
        self.time = 20
        self.timer = 0
        print("Switching to CHASE mode")


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
