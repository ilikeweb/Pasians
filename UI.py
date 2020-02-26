from random import shuffle
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.Qt import QApplication, QWidget
from PyQt5.QtGui import *
from deck import Card, DeckGenerator
from table import TableCard


class UI(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)                        # Эти строчки идут по дефолту
        self.ui = uic.loadUi('pyramid.ui')
        self.palette = QPalette()
        img = QImage('images/index.jpg')
        scaled = img.scaled(self.ui.size())
        self.palette.setBrush(QPalette.Window, QBrush(scaled)) # Присваеваем фону картинку
        self.ui.setPalette(self.palette)

        self.ui.label_29.setPixmap(QPixmap('images/close.png'))   # Присваеваем закрытой карте ее заднюю часть

        self.main_card_list = [self.ui.label_0, self.ui.label_1, self.ui.label_2, self.ui.label_3, self.ui.label_4,
                               self.ui.label_5, self.ui.label_6, self.ui.label_7, self.ui.label_8, self.ui.label_9,
                               self.ui.label_10, self.ui.label_11, self.ui.label_12, self.ui.label_13, self.ui.label_14,
                               self.ui.label_15, self.ui.label_16, self.ui.label_17, self.ui.label_18, self.ui.label_19,
                               self.ui.label_20, self.ui.label_21, self.ui.label_22, self.ui.label_23, self.ui.label_24,
                               self.ui.label_25, self.ui.label_26, self.ui.label_27, self.ui.label_28]

        self.ui.mousePressEvent = self.mousePressEvent         # Перевызначаю стандартный MausEvent
        self.mouse_x_y = []

        for i in self.main_card_list:
            self.mouse_x_y.append([i.x(), i.y()])              # С каждой карты списываем ее координату

        d = DeckGenerator()
        d.shuffle()
        t = TableCard(d)
        t.generate_pyramid()

        self.deck = t.pyramid_deck_linear
        self.stack = t.additional_deck

        for card in range(21, 28):
            self.deck[card].status = True
        for i in self.stack:
            i.status = True

        for i in range(len(self.deck)):
            eval('self.ui.label_{}.setPixmap(self.deck[{}].pixmap)'.format(i, i))

        self.index_stac = 0
        self.ui.label_28.setPixmap(self.stack[self.index_stac].pixmap)                   # 28 лейблу присвоили его лицо (стек слева сверху)

        self.dict_card = dict(zip(self.main_card_list[:28], self.deck))

        self.ui.pushButton.clicked.connect(self.next_card)
        self.ui.actionNew_game.triggered.connect(self.new_game)
        self.ui.actionExit.triggered.connect(self.exit)
        self.ui.actionWin_the_game.triggered.connect(self.win)
        self.ui.show()

        self.a, self.z = [], []

    def mousePressEvent(self, event):

        count = 0
        for i in self.mouse_x_y:
            if event.x() in range(i[0], i[0] + 100) and event.y() in range(i[1], i[1] + 100):
                self.selectedcard_press = self.main_card_list[count]
            count += 1
        try:
            if self.selectedcard_press == self.ui.label_28:

                if self.stack[self.index_stac].value == 13 and self.stack[self.index_stac].status is True:           # Если карта король то мы ее удаляем
                    del self.stack[self.index_stac]
                    self.upgrade_stack()

                elif self.stack[self.index_stac] not in self.a and self.stack[self.index_stac].status is True:
                    self.a.append(self.stack[self.index_stac])                                                       # если карта не король
                    self.z.append(self.selectedcard_press)
                    self.selectedcard_press.setStyleSheet('border-style: solid; border-width: 3px; border-color: blue;')

            elif self.dict_card[self.selectedcard_press].value == 13 and self.dict_card[
                self.selectedcard_press].status is True:                                                              # если карта в деке кароль она удаляется
                self.dict_card[self.selectedcard_press].status = None
                self.upgrade()
            elif self.dict_card[self.selectedcard_press] not in self.a and self.dict_card[
                self.selectedcard_press].status is True:                                                              # если карта тру и не кароль то она прибавляется в список а и z
                self.a.append(self.dict_card[self.selectedcard_press])

                self.z.append(self.selectedcard_press)
                self.selectedcard_press.setStyleSheet('border-style: solid; border-width: 3px; border-color: blue;')

            if len(self.a) == 2:
                if self.a[0].value + self.a[1].value == 13:                                                            # если сумма карт в списке а равна 13 то я присваеваю им нон и отчищаею список а

                    self.a[0].status = None
                    self.a[1].status = None

                    if self.a[0] in self.stack:
                        self.stack.remove(self.a[0])
                        self.upgrade_stack()
                    if self.a[1] in self.stack:
                        self.stack.remove(self.a[1])
                        self.upgrade_stack()
                self.a = []
                self.upgrade()
                for i in self.z:
                    i.setStyleSheet('')

        except AttributeError:
            pass

    def upgrade_stack(self):
        self.index_stac -= 1

        if self.index_stac == -1:
            self.ui.label_28.setPixmap(QPixmap('images/close.png'))                                       # если мы удалил карту и снизу ничего нет то ставим закрытую
            self.index_stac = 0
        else:
            self.ui.label_28.setPixmap(self.stack[self.index_stac].pixmap)                                # если использовали из стака карту возвращаем предыдущую

    def upgrade(self):
        rows = [self.deck[0], self.deck[1:3], self.deck[3:6], self.deck[6:10],
                self.deck[10:15], self.deck[15:21], self.deck[21:28]]
        for q in range(len(rows) - 1):
            if q != 0:
                for n in range(len(rows[q])):
                    if rows[q + 1][n].status is None and rows[q + 1][n + 1].status is None:                 # если карта под индексом n и карта под индексом n+1 в ряде q+1 равны NONE то карта из ряда выше q под индексом n становится TRUE
                        if rows[q][n].status != None:
                            rows[q][n].status = True
            else:
                if rows[0].status is None:
                    self.win()

                elif rows[1][0].status is None and rows[1][1].status is None:                               # исключение для верхней троицы карт
                    rows[0].status = True

        for i in range(len(self.deck)):
            if self.deck[i].status != None:
                eval('self.ui.label_{}.setPixmap(self.deck[{}].pixmap)'.format(i, i))      #  Проганяем по списку и устанавливаем каждой карте их вид
            else:
                self.main_card_list[i].setVisible(False)

    def next_card(self):
        if len(self.z) > 0:
            for i in self.z:
                i.setStyleSheet('')
        try:
            self.index_stac += 1

            self.ui.label_28.setPixmap(self.stack[self.index_stac].pixmap)            #  Вызывается следующаяя карта (смотреть выше)

        except:
            self.index_stac = 0
            self.ui.label_28.setPixmap(self.stack[self.index_stac].pixmap)

    def new_game(self):
        try:
            self.ui_2.close()             #  при нажатии на новую игру оконо закрывается и начинается новая игра
        except:
            pass
        d = DeckGenerator()
        d.shuffle()
        t = TableCard(d)
        t.generate_pyramid()

        self.deck = t.pyramid_deck_linear
        self.stack = t.additional_deck              #  выполняется все то же самое что и и верху. создаются карты мешаются и создается пирамида
        for card in range(21, 28):
            self.deck[card].status = True
        for i in self.stack:
            i.status = True

        for i in range(len(self.deck)):
            eval('self.ui.label_{}.setVisible(True)'.format(i))
            eval('self.ui.label_{}.setPixmap(self.deck[{}].pixmap)'.format(i, i))

        self.index_stac = 0
        self.ui.label_28.setPixmap(self.stack[self.index_stac].pixmap)
        self.dict_card = dict(zip(self.main_card_list[:28], self.deck))
        self.z = []

    def win(self):
        for i in range(len(self.deck)):
            self.main_card_list[i].setVisible(False)

        self.ui_2 = uic.loadUi('victory.ui')   #  открываем окно victory
        mov = QMovie('images/win.gif')         #  устанавливаем ему гиф анимацию
        self.ui_2.label.setMovie(mov)
        mov.start()

        self.ui_2.setPalette(self.palette)

        self.ui_2.pushButton.clicked.connect(self.new_game)
        self.ui_2.pushButton_2.clicked.connect(self.exit)
        self.ui_2.show()

    def exit(self):                     #  закрывает оба окна.
        try:
            self.ui_2.close()
        except:
            pass
        self.ui.close()


if __name__ == "__main__":            #  должны быть по дефолту
    app = QApplication(sys.argv)
    my_app = UI()
    sys.exit(app.exec_())
