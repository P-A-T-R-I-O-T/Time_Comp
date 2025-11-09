import os
import tkinter as tk
from tkinter import messagebox
import sys

class ShutdownApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Таймер выключения Windows")
        self.root.geometry("300x375")
        self.setup_ui()
    
    def setup_ui(self):
        tk.Label(self.root, text="Выберите время выключения:", 
                font=("Arial", 12)).pack(pady=10)
        
        # Кнопки с предустановленным временем
        times = [
            ("30 минут", 30),
            ("1 час", 60), 
            ("1.5 часа", 90),
            ("2 часа", 120),
            ("3 часа", 180)
        ]
        
        for text, minutes in times:
            tk.Button(self.root, text=text, width=20,
                     command=lambda m=minutes: self.set_shutdown(m)).pack(pady=2)
        
        # Поле для ввода своего времени
        tk.Label(self.root, text="Или введите своё время (минут):").pack(pady=5)
        
        self.custom_entry = tk.Entry(self.root, width=10)
        self.custom_entry.pack()
        self.custom_entry.insert(0, "45")
        
        tk.Button(self.root, text="Установить своё время", 
                 command=self.set_custom_time).pack(pady=5)
        
        # Кнопка отмены
        tk.Button(self.root, text="Отменить выключение", 
                 command=self.cancel_shutdown, bg="lightcoral").pack(pady=10)
    
    def set_shutdown(self, minutes):
        if messagebox.askyesno("Подтверждение", 
                              f"Выключить компьютер через {minutes} минут?"):
            seconds = minutes * 60
            os.system(f'shutdown -s -f -t {seconds}')
            messagebox.showinfo("Успех", 
                              f"Таймер установлен! Выключение через {minutes} минут.")
            self.root.destroy()
    
    def set_custom_time(self):
        try:
            minutes = int(self.custom_entry.get())
            if minutes <= 0:
                raise ValueError
            self.set_shutdown(minutes)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число минут!")
    
    def cancel_shutdown(self):
        os.system('shutdown -a')
        messagebox.showinfo("Отменено", "Запланированное выключение отменено!")
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ShutdownApp()
    app.run()
