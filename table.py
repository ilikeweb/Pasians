

class TableCard:
    def __init__(self, deck):

        self.current_deck = deck
        self.pyramid = []
        self.pyramid_rows = 7

    def generate_pyramid(self):

        self._pyramid = [[self.current_deck.deck.pop() for j in range(i)] # создается пирамида
                         for i in range(1, self.pyramid_rows + 1)]

    @property
    def pyramid_deck_linear(self):
        tmp = []
        if self._pyramid:
            for r in self._pyramid:
                for c in r:                                                # Карты представляются ввиде списка
                    tmp.append(c)
        return tmp

    @property
    def additional_deck(self):
        tmp = []
        if self.current_deck.deck:
            for r in self.current_deck.deck:                                # Дек слева сверху(карты)
                tmp.append(r)
        return tmp