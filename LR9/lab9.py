import tkinter as tk
import random
import numpy as np
from os import path
from tkinter import *
from tkinter import Tk, Label, Button, scrolledtext, filedialog, StringVar, ttk
from PIL import Image, ImageTk

def clicked():
    global file
    file = filedialog.askopenfilename(filetypes = (("Image files", "*.bmp"), ("all files", "*.*")), initialdir= path.dirname(__file__))
    if file:
        file = file.split('/')[-1]

        image = Image.open(file)

        image = image.resize((200, 200))
        photo = ImageTk.PhotoImage(image)

        canvas.create_image(0, 0, anchor=NW, image=photo)
        canvas.image = photo


def hiding():
    def ext_pix(image):
        pixels = list(image.getdata())
        print('Пиксели:', pixels[:10])
        for i in range(len(pixels)):
            pixels[i] = list(pixels[i])
            for j in range(len(pixels[i])):
                pixels[i][j] = bin(pixels[i][j])[2:].zfill(8)
        return pixels

    selected_method = combobox.get()

    if selected_method == 'LSB-R':
        print('Метод LSB-R\n_Скрытие сообщения_')
        image = Image.open(file)
        width, height = image.size
        pixels = ext_pix(image)
        print('Пиксели в двоичном виде:', pixels[:10])

        secmes = scr.get("1.0", "end-1c")
        print('Сообщение:', secmes)
        global lenmes
        lenmes = len(secmes)
        binary_secmes = ''.join(format(ord(x), '08b') for x in secmes)
        print('Сообщение в двоичном виде:', binary_secmes)

        raid = int(scale.get())
        print(raid)
        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                r = list(pixels[i][j][-raid:])
                for k in range(len(r)):
                    if binary_secmes == '':
                        break
                    elif r[k] != binary_secmes[0]:
                        r[k] = binary_secmes[0]
                    binary_secmes = binary_secmes[1:]
                pixels[i][j] = pixels[i][j][:-raid] + ''.join(r)
        print('Пиксели с сообщением:', pixels[:10])

        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                pixels[i][j] = int(pixels[i][j], 2)
            pixels[i] = tuple(pixels[i])
        print('Пиксели в десятичном виде с сообщением:', pixels[:10])

        image_LSB_R = Image.new('RGB', (width, height))
        image_LSB_R.putdata(pixels)
        save_path = filedialog.asksaveasfilename(defaultextension=".bmp")
        if save_path:
            image_LSB_R.save(save_path)

        global image_for_ext
        image_for_ext = image_LSB_R

        image_LSB_R = image_LSB_R.resize((200, 200))
        global tk_image
        tk_image = ImageTk.PhotoImage(image_LSB_R)
        canvas1.create_image(0, 0, anchor=NW, image=tk_image)
        canvas1.image = tk_image

    elif selected_method == 'LSB-M':
        print('Метод LSB-M\n_Скрытие сообщения_')
        image = Image.open(file)
        width, height = image.size
        pixels = ext_pix(image)
        print('Пиксели в двоичном виде:', pixels[:10])

        secmes = scr.get("1.0", "end-1c")
        print('Сообщение:', secmes)
        #global lenmes
        lenmes = len(secmes)
        binary_secmes = ''.join(format(ord(x), '08b') for x in secmes)
        print('Сообщение в двоичном виде:', binary_secmes)

        raid = int(scale.get())
        print(raid)
        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                if binary_secmes == '':
                    break
                l = int(binary_secmes[:raid], 2)
                r = pixels[i][j]
                if l != int(r[-raid:], 2):
                    if raid != 1:
                        k1 = 0
                        while l != int(r[-raid:], 2):
                            r = bin(int(r, 2) + 1)[2:]
                            k1 += 1
                        r1 = r
                        r = pixels[i][j]
                        k2 = 0
                        while l != int(r[-raid:], 2) and not (bin(int(r, 2) - 1).startswith('-')):
                            r = bin(int(r, 2) - 1)[2:]
                            k2 += 1
                        r2 = r
                        R = [r1, r2]
                        if k1 > k2:
                            pixels[i][j] = r1
                        elif k1 < k2:
                            pixels[i][j] = r2
                        else:
                            pixels[i][j] = random.choice(R)
                    else:
                        pixels[i][j] = bin(int(pixels[i][j], 2) + random.choice([-1, 1]))[2:]
                binary_secmes = binary_secmes[raid:]

        print('Пиксели с сообщением:', pixels[:10])

        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                pixels[i][j] = int(pixels[i][j], 2)
            pixels[i] = tuple(pixels[i])
        print('Пиксели в десятичном виде с сообщением:', pixels[:10])

        image_LSB_M = Image.new('RGB', (width, height))
        image_LSB_M.putdata(pixels)
        save_path = filedialog.asksaveasfilename(defaultextension=".bmp")
        if save_path:
            image_LSB_M.save(save_path)

        #global image_for_ext
        image_for_ext = image_LSB_M

        image_LSB_L = image_LSB_M.resize((200, 200))
        #global tk_image
        tk_image = ImageTk.PhotoImage(image_LSB_L)
        canvas1.create_image(0, 0, anchor=NW, image=tk_image)
        canvas1.image = tk_image

    elif selected_method == 'Хемминг':
        print('Код Хемминга\n_Скрытие сообщения_')
        image = Image.open(file)
        width, height = image.size
        pixels = ext_pix(image)
        print('Пиксели в двоичном виде:', pixels[:10])

        secmes = scr.get("1.0", "end-1c")
        print('Сообщение:', secmes)
        # global lenmes
        lenmes = len(secmes)
        binary_secmes = ''.join(format(ord(x), '08b') for x in secmes)
        print('Сообщение в двоичном виде:', binary_secmes)

        global H
        H = np.array([list(format(i, '04b')) for i in range(1, 16)], dtype=int).T
        print('Проверочная матрица H:\n', H)

        pr = False
        for i in range(len(pixels)):
            c = np.array(list(pixels[i][0][-5:] + pixels[i][1][-5:] + pixels[i][2][-5:]))
            c = np.array(list(map(int, c)))
            m = np.array(list(binary_secmes[:4]))
            m = np.array(list(map(int, m)))
            binary_secmes = binary_secmes[4:]
            while len(binary_secmes) < 4:
                binary_secmes += '0'
                pr = True
            if pr:
                break

            s = (H @ c + m) % 2

            I = 8 * s[0] + 4 * s[1] + 2 * s[2] + s[3]
            if I == 0:
                continue

            c_mod = c
            c_mod[I - 1] = not c_mod[I - 1]
            c_mod = ''.join(str(x) for x in c_mod)

            pixels[i][0] = pixels[i][0][:-5] + c_mod[:5]
            c_mod = c_mod[5:]
            pixels[i][1] = pixels[i][1][:-5] + c_mod[:5]
            c_mod = c_mod[5:]
            pixels[i][2] = pixels[i][2][:-5] + c_mod[:5]
            c_mod = c_mod[5:]
        print('Пиксели в двоичном виде с сообщением:', pixels)

        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                pixels[i][j] = int(pixels[i][j], 2)
            pixels[i] = tuple(pixels[i])
        print('Пиксели в десятичном виде с сообщением:', pixels[:10])

        image_Hem = Image.new('RGB', (width, height))
        image_Hem.putdata(pixels)
        save_path = filedialog.asksaveasfilename(defaultextension=".bmp")
        if save_path:
            image_Hem.save(save_path)

        # global image_for_ext
        image_for_ext = image_Hem

        image_Hem = image_Hem.resize((200, 200))
        # global tk_image
        tk_image = ImageTk.PhotoImage(image_Hem)

        canvas1.create_image(0, 0, anchor=NW, image=tk_image)
        canvas1.image = tk_image

def extraction():
    def ext_pix(image):
        pixels = list(image.getdata())
        print('Пиксели:', pixels[:10])
        for i in range(len(pixels)):
            pixels[i] = list(pixels[i])
            for j in range(len(pixels[i])):
                pixels[i][j] = bin(pixels[i][j])[2:].zfill(8)
        return pixels

    selected_method = combobox.get()

    if selected_method == 'LSB-R' or selected_method == 'LSB-M':
        raid = int(scale.get())
        print('\n_Извлечение сообщения_')
        image = image_for_ext
        pixels = ext_pix(image)
        print('Пиксели в двоичном виде:', pixels)
        secmes = ''
        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                secmes += pixels[i][j][-raid:]
        print('Сообщение в двоичном виде: ', secmes)
        chunks = [secmes[i:i + 8] for i in range(0, len(secmes), 8)]
        mes = ''.join(chr(int(chunk, 2)) for chunk in chunks)
        print('Сообщение:', mes[:lenmes])

        scr1.insert(tk.END, 'Извлеченное сообщение: '+ "\n\n" + mes[:lenmes] + "\n\n")


    elif selected_method == 'Хемминг':
        print('\n_Извлечение сообщения_')
        image = image_for_ext
        pixels = ext_pix(image)
        print('Пиксели в двоичном виде:', pixels)
        secmes_err = ''
        for i in range(len(pixels)):
            secmes_err += pixels[i][0][-5:] + pixels[i][1][-5:] + pixels[i][2][-5:]
        print('Сообщение в двоичном виде с ошибкой:', secmes_err)

        secmes = ''
        for i in range(0, len(secmes_err), 15):
            ser_err = (H @ np.array(list(int(x) for x in secmes_err[i: i + 15])).tolist()) % 2
            ser_err = ''.join(str(x) for x in ser_err)
            secmes += str(ser_err)
        print(secmes)
        chunks = [secmes[i:i + 8] for i in range(0, len(secmes), 8)]
        mes = ''.join(chr(int(chunk, 2)) for chunk in chunks)
        print('Сообщение:', mes[:lenmes])

        scr1.insert(tk.END, 'Извлеченное сообщение: ' + "\n\n" + mes[:lenmes] + "\n\n")


window = Tk()
window.minsize(width=750, height=570)
window.title('StegoRGB')
window.configure(bg="#A0AECD")

canvas = Canvas(window, width=200, height=200)
canvas.place(x=490, y=50)
canvas.create_rectangle(0, 0, 300, 300, fill="#D3D3D3", outline="", state="disabled")

canvas1 = Canvas(window, width=200, height=200)
canvas1.place(x=490, y=345)
canvas1.create_rectangle(0, 0, 300, 300, fill="#D3D3D3", outline="", state="disabled")

lbl00 = Label(window, text='Скрываемое сообщение:', font = ('Times New Roman', 14), bg="#A0AECD")
lbl00.grid(column=0, row=0, pady=(15,0), padx=90, sticky='W')

lbl01 = Label(window, text='Контейнер', font = ('Times New Roman', 14), bg="#A0AECD")
lbl01.grid(column=1, row=0, pady=(15,0), padx=145, sticky='W')

scr = scrolledtext.ScrolledText(window, width=45, height=9)
scr.grid(column=0, row=1, pady=(10,0), padx=10)
scr.focus()

lbl02 = Label(window, text='Метод скрытия:', font = ('Times New Roman', 14), bg="#A0AECD")
lbl02.place(x=75, y=215)
# lbl02.grid(column=0, row=2, pady=(5,0), padx=65, sticky='W')

methods = ['LSB-R', 'LSB-M', 'Хемминг']
methods_var = StringVar(value=methods[0])

label = ttk.Label(textvariable=methods_var)

combobox = ttk.Combobox(textvariable=methods_var, values=methods, font = ('Times New Roman', 12), width=12)
combobox.place(x=220, y=215)
combobox.current(0)

combobox.bind("<FocusIn>", lambda event: combobox.selection_clear())

lbl03 = Label(window, text='Выбор рейта:', font = ('Times New Roman', 14), bg="#A0AECD")
lbl03.place(x=85, y=267)

scale = Scale(window, from_= 1, to=8, orient=HORIZONTAL)
scale.place(x=220, y=250)

btn00 = Button(window, text="Выберите изображение", font=('Times New Roman', 11), bg="#A0AECD", command=clicked)
btn00.grid(column=1, row=2, padx=10, pady=(60,0), sticky='N')

lbl04 = Label(window, text='Контейнер 2', font = ('Times New Roman', 14), bg="#A0AECD")
lbl04.grid(column=1, row=3, pady=(20,0), padx=145, sticky='W')

btn01 = Button(window, text="Спрятать информацию", font=('Times New Roman', 14), bg="#A0AECD", command=hiding)
btn01.place(x=110, y=305)

btn01 = Button(window, text="Извлечь информацию", font=('Times New Roman', 12), bg="#A0AECD", command=extraction)
btn01.place(x=127, y=350)

scr1 = scrolledtext.ScrolledText(window, width=45, height=9)
scr1.place(x=10, y=400)

# button02 = tk.Button(window, text='🔐', font=('Arial', 18), bg="#A0AECD", command='extraction2')
# button02.place(x=705, y=502)


# Функция, вызываемая при изменении выбранного элемента в combobox
def show_scale(event):
    if combobox.get() == 'Хемминг':
        scale.place_forget()

    else:
        lbl03.place(x=85, y=267)
        scale.place(x=220, y=250)


# Привязка функции к событию изменения выбранного элемента в combobox
combobox.bind('<<ComboboxSelected>>', show_scale)


window.mainloop()