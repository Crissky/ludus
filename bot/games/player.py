class Player:
    def __init__(self, id: str, name: str):
        self.id = str(id)
        self.name = name

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Player(id={self.id}, name={self.name})'

    @property
    def user_id(self):
        return self.id

    player_id = user_id
