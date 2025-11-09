import os
import tkinter as tk
from tkinter import messagebox
import threading
import time

class DarkMessageBox:
    @staticmethod
    def show_info(parent, title, message, duration=2000):
        # Создаем кастомное окно сообщения
        msg_window = tk.Toplevel(parent)
        msg_window.title(title)
        msg_window.geometry("300x150")
        msg_window.configure(bg='#2b2b2b')
        msg_window.overrideredirect(True)  # Убираем стандартную рамку
        
        # Делаем окно поверх всех
        msg_window.attributes('-topmost', True)
        
        # Центрируем окно сообщения
        msg_window.update_idletasks()
        width = msg_window.winfo_width()
        height = msg_window.winfo_height()
        x = (msg_window.winfo_screenwidth() // 2) - (width // 2)
        y = (msg_window.winfo_screenheight() // 2) - (height // 2)
        msg_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Содержимое окна
        tk.Label(msg_window, text=title, bg='#2b2b2b', fg='#ffffff', 
                font=("Arial", 12, "bold")).pack(pady=15)
        tk.Label(msg_window, text=message, bg='#2b2b2b', fg='#ffffff',
                font=("Arial", 10), wraplength=280).pack(pady=5)
        
        # Автоматическое закрытие через duration миллисекунд
        msg_window.after(duration, msg_window.destroy)

class ShutdownApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Таймер выключения Windows")
        self.root.geometry("300x375")
        self.root.configure(bg='#2b2b2b')
        self.root.overrideredirect(True)  # Убираем стандартную рамку
        
        # Центрируем окно
        self.center_window()
        self.setup_ui()
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def show_auto_message(self, title, message, duration=2000):
        """Показывает сообщение, которое автоматически закрывается"""
        # Запускаем в основном потоке, используя after для безопасности
        self.root.after(100, lambda: DarkMessageBox.show_info(self.root, title, message, duration))
    
    def setup_ui(self):
        bg_color = '#2b2b2b'
        fg_color = '#ffffff'
        button_bg = '#404040'
        button_fg = '#ffffff'
        button_active = '#505050'
        entry_bg = '#404040'
        entry_fg = '#ffffff'
        accent_color = '#d9534f'
        title_bg = '#1a1a1a'  # Ещё темнее для заголовка
        
        # Кастомный заголовок
        title_frame = tk.Frame(self.root, bg=title_bg, height=30)
        title_frame.pack(fill='x', side='top')
        title_frame.pack_propagate(False)
        
        # Текст заголовка
        tk.Label(title_frame, text="Таймер выключения Windows", 
                bg=title_bg, fg=fg_color, font=("Arial", 10)).pack(side='left', padx=10)
        
        # Кнопка закрытия
        close_btn = tk.Button(title_frame, text="×", 
                             bg=title_bg, fg=fg_color, 
                             activebackground=accent_color,
                             activeforeground=fg_color,
                             border=0, font=("Arial", 14, "bold"),
                             command=self.root.destroy)
        close_btn.pack(side='right', padx=5)
        
        # Функции для перемещения окна
        def start_move(event):
            self.x = event.x
            self.y = event.y
        
        def stop_move(event):
            self.x = None
            self.y = None
        
        def do_move(event):
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.root.winfo_x() + deltax
            y = self.root.winfo_y() + deltay
            self.root.geometry(f"+{x}+{y}")
        
        # Привязываем события для перемещения
        title_frame.bind("<ButtonPress-1>", start_move)
        title_frame.bind("<ButtonRelease-1>", stop_move)
        title_frame.bind("<B1-Motion>", do_move)
        
        # Основной контент
        content_frame = tk.Frame(self.root, bg=bg_color)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Заголовок
        tk.Label(content_frame, text="Выберите время выключения:", 
                font=("Arial", 12), bg=bg_color, fg=fg_color).pack(pady=10)
        
        # Кнопки с предустановленным временем
        times = [
            ("30 минут", 30),
            ("1 час", 60), 
            ("1.5 часа", 90),
            ("2 часа", 120),
            ("3 часа", 180)
        ]
        
        for text, minutes in times:
            tk.Button(content_frame, text=text, width=20,
                     bg=button_bg, fg=button_fg,
                     activebackground=button_active,
                     activeforeground=fg_color,
                     relief='flat',
                     command=lambda m=minutes: self.set_shutdown(m)).pack(pady=2)
        
        # Поле для ввода своего времени
        tk.Label(content_frame, text="Или введите своё время (минут):",
                bg=bg_color, fg=fg_color).pack(pady=5)
        
        self.custom_entry = tk.Entry(content_frame, width=10,
                                   bg=entry_bg, fg=entry_fg,
                                   insertbackground=fg_color)
        self.custom_entry.pack()
        self.custom_entry.insert(0, "45")
        
        tk.Button(content_frame, text="Установить своё время", 
                 bg=button_bg, fg=button_fg,
                 activebackground=button_active,
                 activeforeground=fg_color,
                 relief='flat',
                 command=self.set_custom_time).pack(pady=5)
        
        # Кнопка отмены
        tk.Button(content_frame, text="Отменить выключение", 
                 command=self.cancel_shutdown, 
                 bg=accent_color, fg=fg_color,
                 activebackground='#c9302c',
                 activeforeground=fg_color,
                 relief='flat',
                 font=("Arial", 9, "bold")).pack(pady=10)
    
    def set_shutdown(self, minutes):
        seconds = minutes * 60
        os.system(f'shutdown -s -f -t {seconds}')
        self.show_auto_message("Успех", f"Выключение через {minutes} минут.")
        # Не закрываем главное окно сразу, даем увидеть сообщение
        self.root.after(3200, self.root.destroy)  # Закрываем после показа сообщения
    
    def set_custom_time(self):
        try:
            minutes = int(self.custom_entry.get())
            if minutes <= 0:
                raise ValueError
            self.set_shutdown(minutes)
        except ValueError:
            self.show_auto_message("Ошибка", "Введите корректное число минут!")
    
    def cancel_shutdown(self):
        os.system('shutdown -a')
        self.show_auto_message("Отменено", "Запланированное выключение отменено!")
        # Не закрываем главное окно сразу, даем увидеть сообщение
        self.root.after(3000, self.root.destroy)  # Закрываем после показа сообщения
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ShutdownApp()
    app.run()
