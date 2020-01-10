class dummyport:
    """A Dummy port implementation for our dummy Art-Net Node"""

    def __init__(self, universe: int = 0, mode: str="Art-Net"):
        self.universe = universe
        self.mode = mode
        self.tod = list()
