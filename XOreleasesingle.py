from tkinter import *
from tkinter import messagebox
import asyncio
import socket
import concurrent.futures

# sock = socket.socket()
# sock.connect(('localhost', 9090))

board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
current_sign = 'X'
root = Tk()

text1 = StringVar()


def generate_frame():
    frame_name = Frame(root, bg='lightblue')
    frame_name.grid(row=0, column=0, sticky='news')
    return frame_name


menu = generate_frame()
pac = generate_frame()
tk = generate_frame()

restart_btn = None


def generate_label(tk, text_: str = '', text_variable=None, bg_: str = 'lightblue', font_name: str = 'Neutral Face',
                   font_size: int = 18,
                   row_: int = 4, column_: int = 0, columnspan_: int = 1, rowspan_: int = 1):
    label = Label(tk, text=text_, textvariable=text_variable, bg=bg_, font=(font_name, font_size))
    label.grid(row=row_, column=column_, columnspan=columnspan_, rowspan=rowspan_)
    return label


def play():
    global tk
    pac.tkraise()


name1 = ''
name2 = ''
generate_label(pac, '                              ', font_size=7, row_=1, column_=1)
generate_label(pac, 'Игрок №1', font_size=15, row_=1, column_=0)
generate_label(pac, 'Игрок №2', font_size=15, row_=1, column_=2)
name1_form = Entry(pac, width=15, font=('Arial Bold', 12))
name1_form.grid(row=2, column=0)
name2_form = Entry(pac, width=15, font=('Arial Bold', 12))
name2_form.grid(row=2, column=2)


def confirm_names():
    global name1, name2
    name1 = name1_form.get()
    name2 = name2_form.get()
    if name1 == '' or name2 == '':
        messagebox.showerror('Выбор имени', 'Не введено имя игрока!')
        return None
    if name1 == name2:
        messagebox.showinfo('Выбор имени', 'Имена не должны совпадать')
        return None
    tk.tkraise()


def generate_buttons(tk, text_: str = 'Рестарт', font_name: str = 'Neutral Face', font_size: int = 16,
                     bg_: str = 'lightgreen', width_: int = 7, height_: int = 3, command_=None, row_: int = 2,
                     column_: int = 1, rowspan_: int = None, columnspan_: int = None, image_=None,
                     font_option: str = 'bold'):
    btn = Button(tk, text=text_, font=(font_name, font_size, font_option), bg=bg_, width=width_, height=height_,
                 command=command_, image=image_)
    btn.grid(row=row_, column=column_, rowspan=rowspan_, columnspan=columnspan_)
    return btn


play_image = PhotoImage(file=r"C:\Users\user\Desktop\git\play.png")
generate_buttons(pac, text_='Начать', font_size=11, width_=52, height_=52, image_=play_image, command_=confirm_names,
                 row_=1,
                 column_=1, rowspan_=2)


def restart():
    global board, restart_btn, buttons, current_sign, online_board
    current_sign = 'X'
    restart_btn.destroy()
    for button in buttons:
        button.destroy()
    play()
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    buttons = [
        generate_buttons(tk, text_=None, width_=5, height_=2, font_size=28, font_name='Arial', font_option='bold',
                         bg_='lightblue', command_=lambda x=i: play_game(x, board))
        for i in range(9)]
    row = 1
    col = 0
    for i in range(9):
        buttons[i].grid(row=row, column=col)
        col += 1
        if col == 3:
            row += 1
            col = 0
    text1.set('')


def play_game(i, board):
    global current_sign, buttons, restart_btn
    if board[i] == 0:
        if current_sign == 'X':
            current_sign = 'O'
            buttons[i].config(text='X', state='disabled', bg='#00ccff')
            board[i] = 1
            # cur_data = bytearray(board)
            # sock.send(cur_data)
        else:
            current_sign = 'X'
            buttons[i].config(text='O', state='disabled', bg='#ff9999')
            board[i] = 2
            # cur_data = bytearray(board)
            # sock.send(cur_data)
        result = get_winner(winning_combinations)
        label = generate_label(tk, text_variable=text1, font_size=13, font_name='Neutral Face', row_=5, column_=0,
                                rowspan_=1,
                                columnspan_=3)
        text1.set(f'Ход игрока с ником: {name1}' if current_sign == 'X' else
                  f'Ход игрока с ником:'
                  f' {name2}')
        if result == 1:
            print('X is Winner!')
            text1.set("Игрок со знаком 'X' победил!" if name1 == '' else
                      f"{name1} со знаком 'X' победил!")
            for k in buttons:
                k.config(state='disabled', bg='#00ccff')
            restart_btn = generate_buttons(tk, command_=restart)
        if result == 2:
            print('O is Winner!')
            text1.set("Игрок со знаком 'O' победил!" if name2 == '' else
                      f"{name2} со знаком 'O' победил!")
            for k in buttons:
                k.config(state='disabled', bg='#ff9999')
            restart_btn = generate_buttons(tk, command_=restart)
        if all(board) != 0:
            text1.set('Ничья! Сыграть ещё?')
            restart_btn = generate_buttons(tk, command_=restart)




buttons = [
    generate_buttons(tk, text_=None, width_=5, height_=2, font_size=28, font_name='Arial', font_option='bold',
                     bg_='lightblue', command_=lambda x=i: play_game(x, board))
    for i in range(9)]

row = 1
col = 0
for i in range(9):
    buttons[i].grid(row=row, column=col)
    col += 1
    if col == 3:
        row += 1
        col = 0

winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                        (0, 3, 6), (1, 4, 7), (2, 5, 8),
                        (0, 4, 8), (2, 4, 6)]


def get_winner(combinations):
    for (x, y, z) in combinations:
        if board[x] == board[y] and board[y] == board[z] and (board[x] == 1 or board[x] == 2):
            return board[x]


generate_label(menu, "          ", font_name='Neutral Face', font_size=6, row_=0, column_=0)
generate_label(menu, "Игра Крестики-Нолики!", font_size=16, row_=0, column_=1)
generate_label(menu, "          ", font_size=6, row_=1, column_=0)
generate_buttons(menu, text_='Играть', width_=11, height_=1, font_size=25, command_=play, row_=2, column_=1)
menu.tkraise()
root.mainloop()

# if __name__ == '__main__':
