from tkinter import *
from api_naumen import API_Naumen
from tkinter import messagebox
import threading
from selenium.common.exceptions import NoSuchElementException
from tkinter import scrolledtext
import time


class App:
    api = API_Naumen()

    def __init__(self, gui_window):

        """Создание окна первого фрейма"""
        self.gui_window = gui_window
        self.gui_window.title('Send comments')
        self.gui_window.geometry('550x600')
        self.gui_window['bg'] = '#5F5F5F'

        self.lbl_l_naumen = Label(self.gui_window, text='Login Naumen', font=("Arial Bold", 20), bg='#5F5F5F',
                                  fg='white')
        self.lbl_p_naumen = Label(self.gui_window, text='Password Naumen', font=("Arial Bold", 20), bg='#5F5F5F',
                                  fg='white')

        self.login_area = Entry(self.gui_window, width=30)
        self.password_area = Entry(self.gui_window, width=30, show='*')

        self.btn_send = Button(text='Отправить логин\nи пароль', command=self.send_log_pass, bg='#5F5F5F',
                               fg='white', font=("Arial", 13))
        self.btn_clear = Button(text='Очистить поле\nлогина и пароля', command=self.clear, bg='#5F5F5F', fg='white',
                                font=("Arial", 13))

        self.lbl_l_naumen.place(relx=0.35, rely=0.35)
        self.login_area.place(relx=0.35, rely=0.41)
        self.lbl_p_naumen.place(relx=0.32, rely=0.45)
        self.password_area.place(relx=0.35, rely=0.51)

        self.btn_send.place(relx=0.24, rely=0.59)
        self.btn_clear.place(relx=0.54, rely=0.59)

        """Создание второго фрейма"""

        self.text_comments_area = scrolledtext.ScrolledText(gui_window, width=60, height=5,
                                                            font=("Times New Roman", 12), bg='#707070', fg='white')
        self.list_request_area = scrolledtext.ScrolledText(gui_window, width=25, height=17,
                                                           font=("Times New Roman", 12), bg='#707070', fg='white')
        self.btn_start = Button(gui_window, text='Направить\nкомментарии', command=self.begin, bg='#5F5F5F',
                                fg='white', font=("Arial", 15))
        self.private_var = BooleanVar()
        self.chb_private = Checkbutton(text='Комментарий приватный?', variable=self.private_var, bg='#5F5F5F', fg='white',
                                       font=("Arial", 14), selectcolor='#5F5F5F')
        self.lbl_count = Label(text='Нажми на кнопку,\nполучишь результат', bg='#5F5F5F', fg='white',
                               font=("Arial", 14))

        self.btn_view_browser = Button(gui_window, text='Показать процесс\nв браузере', command=self.begin, bg='#5F5F5F',
                                fg='white', font=("Arial", 15))

    def clear(self):
        self.login_area.delete('0', END)
        self.password_area.delete('0', END)

    def send_log_pass(self):

        login = self.login_area.get()
        password = self.password_area.get()
        if login == '' or password == '':
            messagebox.showinfo('Ошибка', 'Не заполнены\nлогин и пароль')
            self.clear()
            return
        login = self.login_area.get()
        password = self.password_area.get()
        """ЗАПУСК НАУМЕНА"""
        self.api.start_naumen(login, password)
        self.clear()
        flag = False
        try:
            # print(login, password)
            # flag = True  # фиктивный проход авторизации/требуется убрать
            self.api.driver.find_element_by_xpath('//*[@id="LogonForm"]/p')
            messagebox.showinfo('Ошибка', 'Не верный логин или пароль')
        except NoSuchElementException:
            flag = True

        if flag:
            """Сокрытие кнопок"""
            self.btn_send.configure(state='disabled')
            self.btn_clear.configure(state='disabled')
            self.btn_send.place(relx=-1, rely=0.59)
            self.btn_clear.place(relx=1, rely=0.59)
            self.lbl_l_naumen.place(relx=-1, rely=0.35)
            self.login_area.place(relx=-1, rely=0.41)
            self.lbl_p_naumen.place(relx=-1, rely=0.45)
            self.password_area.place(relx=-1, rely=0.51)

            """Создание нового фрейма"""
            lbl_text_comment = Label(text='Какой текст требуется написать в каждой заявке?', bg='#5F5F5F', fg='white',
                                     font=("Arial", 14))
            lbl_text_comment.pack()
            self.text_comments_area.pack()

            self.chb_private.place(relx=0.3, rely=0.22)

            lbl_list_request = Label(text='Список заявок, где требуется\nдобавить комментарий', bg='#5F5F5F',
                                     fg='white',
                                     font=("Arial", 14))
            lbl_list_request.place(relx=0.06, rely=0.29)
            self.list_request_area.place(relx=0.1, rely=0.40)
            self.btn_start.place(relx=0.61, rely=0.50)

            self.lbl_count.place(relx=0.6, rely=0.65)

            return

    def func(self):
        bad = []
        lst_request = self.list_request_area.get('0.1', END).split('\n')
        text_comment = self.text_comments_area.get('0.1', END)

        n = lst_request.count('')
        count = 0
        self.lbl_count.configure(text='Сейчас начнется\nвыполнение')
        for _ in range(n):
            lst_request.remove('')
        total_request = len(lst_request)
        if total_request == 0:
            messagebox.showinfo('Ошибка', 'Не найдена ни одна заявка')
            return
        private = self.private_var.get()

        self.btn_start.configure(state='disabled')
        self.btn_start.place(relx=-1, rely=-1)
        self.btn_view_browser.place(relx=0.61, rely=0.50)
        for request in lst_request:
            count += 1
            try:
                self.api.send_comments(request, text_comment, private)
                time.sleep(1)
            except NoSuchElementException:
                bad.append(request)
            self.lbl_count.place(relx=0.68, rely=0.65)
            self.lbl_count.configure(text=f'Выполнено\n{count} из {total_request}')
            self.gui_window.title(f'{count} из {total_request}')
        if len(bad) > 0:
            with open('errors.txt', 'w') as bad_file:
                for query in bad:
                    bad_file.write(f'{query}\n')
        self.api.driver.close()
        messagebox.showinfo('Done', 'Все было отправлено\n'
                                    'Требуется проверить файл\n'
                                    'errors.txt, если есть')

    def begin(self):
        threading.Thread(target=self.func, daemon=True).start()


if __name__ == '__main__':

    gui_window = Tk()
    app = App(gui_window)
    gui_window.mainloop()
