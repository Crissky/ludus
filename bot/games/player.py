class Player:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    @property
    def user_id(self):
        return self.id

    player_id = user_id
