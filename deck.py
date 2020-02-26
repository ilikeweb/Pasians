from random import shuffle
from PyQt5.QtGui import QPixmap


class Card:
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']  # Наименование карты
    SUITS = ['S', 'D', 'C', 'H']

    def __init__(self, rank, suit, status=False):

        self.rank = rank
        self.suit = suit
        self.status = status
        self.value = self.RANKS.index(rank) + 1
        self.face = None
        self.back = None

        self.load_images()

    def load_images(self):
        self._face = QPixmap('cards/{}_{}.png'.format(self.rank, self.suit))        # каждой карте присваевается ее картинка лицо
        self._back = QPixmap('images/close.png')                                     # каждой карте присваевается задняя ее часть

    @property
    def pixmap(self):
        if self.status:
            return self._face                                                      # если статус ТРУ то возвращает лицевую часть иначе заднюю
        else:
            return self._back


class DeckGenerator:

    def __init__(self):

        self.card_deck = []
        self.iter = 0

        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.card_deck.append(Card(rank, suit))                          # Генернирует дек из каторого будут браться карты

    @property
    def deck(self):
        return self.card_deck

    def shuffle(self):
        return shuffle(self.card_deck)