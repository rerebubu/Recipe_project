import tkinter as tk  # Импортируем библиотеку для создания графического интерфейса
import sqlite3  # Импортируем библиотеку для работы с базой данных SQLite
from tkinter import messagebox  # Импортируем компонент для отображения сообщений пользователю

# Класс для экрана авторизации
class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)  # Инициализация родительского класса
        self.configure(bg="#FFB6C1")  # Устанавливаем розовый фон

        # Создаем и размещаем метку для логина
        self.username_label = tk.Label(self, text="Логин:", bg="#FFB6C1", font=("Arial", 16))
        self.username_label.pack(pady=10)  # Добавляем отступ сверху и снизу

        # Поле для ввода логина
        self.username_entry = tk.Entry(self, font=("Arial", 16))
        self.username_entry.pack(pady=10)  # Упаковываем поле с отступом

        # Создаем и размещаем метку для пароля
        self.password_label = tk.Label(self, text="Пароль:", bg="#FFB6C1", font=("Arial", 16))
        self.password_label.pack(pady=10)

        # Поле для ввода пароля, символы скрыты
        self.password_entry = tk.Entry(self, show='*', font=("Arial", 16))
        self.password_entry.pack(pady=10)

        # Кнопка для входа в приложение
        self.login_button = tk.Button(self, text="Войти", command=self.login, font=("Arial", 16))
        self.login_button.pack(pady=20)  # Упаковываем кнопку с отступом

        self.pack(fill="both", expand=True)  # Заполняем доступное пространство

    def login(self):
        # Переход к главному экрану при успешном входе
        self.master.show_main()

# Класс для экрана добавления рецепта
class AddRecipeFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)  # Инициализация родительского класса
        self.configure(bg="#FFB6C1")  # Устанавливаем нежно-розовый фон

        # Метка для названия рецепта
        self.recipe_name_label = tk.Label(self, text="Название блюда:", bg="#FFB6C1", font=("Arial", 16))
        self.recipe_name_label.pack(pady=10)

        # Поле для ввода названия рецепта
        self.recipe_name_entry = tk.Entry(self, font=("Arial", 16))
        self.recipe_name_entry.pack(pady=10)

        # Метка для ингредиентов
        self.ingredients_label = tk.Label(self, text="Ингредиенты:", bg="#FFB6C1", font=("Arial", 16))
        self.ingredients_label.pack(pady=10)

        # Текстовое поле для ввода ингредиентов
        self.ingredients_text = tk.Text(self, height=5, font=("Arial", 16))
        self.ingredients_text.pack(pady=10)

        # Метка для рецепта
        self.instructions_label = tk.Label(self, text="Рецепт:", bg="#FFB6C1", font=("Arial", 16))
        self.instructions_label.pack(pady=10)

        # Текстовое поле для ввода рецепта
        self.instructions_text = tk.Text(self, height=5, font=("Arial", 16))
        self.instructions_text.pack(pady=10)

        # Кнопка для добавления рецепта в базу данных
        self.add_button = tk.Button(self, text="Добавить рецепт", command=self.add_recipe, font=("Arial", 16))
        self.add_button.pack(pady=10)

        # Кнопка для возврата к главному экрану
        self.back_button = tk.Button(self, text="Вернуться к поиску", command=self.back_to_main, font=("Arial", 16))
        self.back_button.pack(pady=10)

        self.pack(fill="both", expand=True)  # Заполняем доступное пространство

    def add_recipe(self):
        # Получаем данные из полей ввода
        recipe_name = self.recipe_name_entry.get()  # Название блюда
        ingredients = self.ingredients_text.get("1.0", tk.END).strip()  # Ингредиенты
        instructions = self.instructions_text.get("1.0", tk.END).strip()  # Инструкции

        # Подключаемся к базе данных
        conn = sqlite3.connect('recipes.db')
        cursor = conn.cursor()
        # Сохраняем рецепт в базе данных
        cursor.execute("INSERT INTO recipes (name, ingredients, instructions) VALUES (?, ?, ?)",
                       (recipe_name, ingredients, instructions))
        conn.commit()  # Применяем изменения
        conn.close()  # Закрываем соединение

        # Очищаем поля ввода после добавления
        self.recipe_name_entry.delete(0, tk.END)
        self.ingredients_text.delete(1.0, tk.END)
        self.instructions_text.delete(1.0, tk.END)

        # Показываем сообщение об успешном добавлении рецепта
        messagebox.showinfo("Успех", "Рецепт успешно добавлен!")

    def back_to_main(self):
        # Переход к главному экрану
        self.master.show_main()

# Класс для главного экрана
class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)  # Инициализация родительского класса
        self.configure(bg="#FFB6C1")  # Устанавливаем нежно-розовый фон

        # Поле для ввода названия рецепта для поиска
        self.recipe_entry = tk.Entry(self, font=("Arial", 16))
        self.recipe_entry.pack(pady=10)

        # Кнопка для выполнения поиска рецепта
        self.find_button = tk.Button(self, text="Найти рецепт", command=self.find_recipe, font=("Arial", 16))
        self.find_button.pack(pady=10)

        # Поле для отображения найденного рецепта
        self.result_text = tk.Text(self, font=("Arial", 16))
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Полоса прокрутки для текстового поля
        self.scrollbar = tk.Scrollbar(self.result_text)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=self.scrollbar.set)  # Связываем прокрутку с текстом
        self.scrollbar.config(command=self.result_text.yview)  # Настройка прокрутки

        # Кнопка для перехода на экран добавления рецепта
        self.add_recipe_button = tk.Button(self, text="Добавить рецепт", command=self.master.show_add_recipe, font=("Arial", 16))
        self.add_recipe_button.pack(pady=10)

        self.pack(fill="both", expand=True)  # Заполняем доступное пространство

    def find_recipe(self):
        # Получаем название рецепта из поля поиска
        recipe_name = self.recipe_entry.get()
        conn = sqlite3.connect('recipes.db')  # Подключаемся к базе данных
        cursor = conn.cursor()

        # Выполняем запрос на поиск рецепта по названию
        cursor.execute("SELECT ingredients, instructions FROM recipes WHERE name=?", (recipe_name,))
        result = cursor.fetchone()  # Получаем результат запроса

        self.result_text.delete(1.0, tk.END)  # Очищаем текстовое поле перед отображением результата

        if result:
            ingredients, instructions = result  # Распаковываем найденные данные
            # Отображаем ингредиенты и инструкции в текстовом поле
            self.result_text.insert(tk.END, f"Ингредиенты:\n{ingredients}\n\nРецепт:\n{instructions}")
        else:
            self.result_text.insert(tk.END, "Такого рецепта нет!")  # Уведомляем, если рецепт не найден

        conn.close()  # Закрываем соединение с базой данных

# Основной класс приложения
class App(tk.Tk):
    def __init__(self):
        super().__init__()  # Инициализация основного окна приложения
        self.title("Рецепты")  # Установка заголовка окна
        self.geometry("400x600")  # Установка размера окна

        # Создаем экземпляры всех экранов приложения
        self.login_frame = LoginFrame(self)
        self.main_frame = MainFrame(self)
        self.add_recipe_frame = AddRecipeFrame(self)

        self.show_login()  # Показать экран авторизации

    def show_login(self):
        # Скрываем другие экраны и показываем экран авторизации
        self.main_frame.pack_forget()
        self.add_recipe_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

    def show_main(self):
        # Скрываем экран авторизации и показываем главный экран
        self.login_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)

    def show_add_recipe(self):
        # Скрываем главный экран и показываем экран добавления рецепта
        self.main_frame.pack_forget()
        self.add_recipe_frame.pack(fill="both", expand=True)

# Запускаем приложение
if __name__ == "__main__":
    app = App()  # Создаем экземпляр приложения
    app.mainloop()  # Запускаем основной цикл обработки событий