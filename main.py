import os  # импорт библиотек для работы с операционной системой
import shutil
import hashlib  # импорт библиотеки для создания хэша

import settings  # импорт пакета с настройками

root_dir = settings.working_directory  # корневая директория менеджера
user_root_dir = settings.user_working_directory  # корневая директория текущего пользователя
current_dir = settings.user_working_directory  # текущая директория


# функция для создания директорий
def mkdir(*dir_names):
    for name in dir_names:
        try:
            os.mkdir(os.path.join(current_dir, name))  # создание директории
        except FileExistsError:
            print(f'Папка с именем "{name}" уже существует')


# функция для удаления директорий
def rmdir(*dir_names):
    for name in dir_names:
        try:
            shutil.rmtree(os.path.join(current_dir, name))  # рекурсивное удаление директорий
        except FileNotFoundError:
            print(f'Папки с именем "{name}" не существует внутри текущей директории')
        except OSError:
            print('Ошибка удаления папки')


# функция для смены директории
def cd(*dir_name):  # передается имя директории или относительный путь к ней
    global current_dir
    if len(dir_name) > 1:
        print('Вам следует передать только 1 параметр')
    else:
        new_dir = os.path.abspath(os.path.join(current_dir, dir_name[0]))
        if os.path.isdir(new_dir):
            if user_root_dir in new_dir:  # если корневая папка входит в путь
                current_dir = new_dir
            else:
                print('Нельзя подняться выше корневой папки')
        else:
            print('Папки с таким путем не существует')


# функция создания файлов
def mkfile(*file_names):
    for name in file_names:
        try:
            file_path = os.path.join(current_dir, name)
            open(file_path, 'w').close()
        except FileExistsError:
            print(f'Файл с именем "{name}" уже существует')


# функция записи текста в файл
def write(*params):
    if len(params) > 1:
        print('Вам следует передать только 1 параметр')
    else:
        try:
            file_name = params[0]  # имя файла
            file_path = os.path.join(current_dir, file_name)  # путь к файлу
            with open(file_path, 'w') as file:
                print("Введите текст. Введите пустую строку, чтобы закончить")
                lines = []
                while True:  # цикл для ввода текста
                    line = input("> ")
                    if not line:
                        break
                    lines.append(line + "\n")
                file.writelines(lines)
        except IsADirectoryError:
            print(f'"{file_name}" является директорией')
        except PermissionError:
            print(f'Доступ для записи в файл "{file_name}" запрещен')


# функция для чтения текста из файла
def read(*file_name):
    if len(file_name) > 1:
        print('Вам следует передать только 1 параметр')
    else:
        try:
            file_path = os.path.join(current_dir, file_name[0])
            with open(file_path, 'r') as file:
                print(file.read())
        except FileNotFoundError:
            print(f'Файла "{file_name[0]}" не существует внутри текущей папки')
        except IsADirectoryError:
            print(f'"{file_name[0]}" является директорией')
        except PermissionError:
            print(f'Доступ для чтения файла "{file_name[0]}" запрещен')


# функция для удаления файлов
def rmfile(*file_names):
    for name in file_names:
        try:
            file_path = os.path.join(current_dir, name)
            os.remove(file_path)
        except FileNotFoundError:
            print(f'Файла "{name}" не существует внутри текущей папки')


# функция копирования файла
def copy(*params):
    if len(params) == 2:
        file_name = params[0]
        dir_path = params[1]
        try:
            out_path = os.path.join(current_dir, file_name)
            in_path = os.path.abspath(os.path.join(current_dir, dir_path, file_name))
            if user_root_dir in in_path:  # чтобы не выйти из корневой директории
                shutil.copyfile(out_path, in_path)
            else:
                print('Нельзя подняться выше корневой папки')
        except FileNotFoundError:
            print(f'Файла "{file_name}" не существует внутри текущей папки\nИли относительный путь к директории указан неверно')
        except shutil.SameFileError:
            print('Нельзя копировать файл в ту же самую директорию')
    else:
        print('Вам следует передать 2 параметра: имя файла для копирования и путь в директорию')


# функция для перемещения файла
def move(*params):
    if len(params) == 2:
        file_name = params[0]
        dir_path = params[1]
        try:
            out_path = os.path.join(current_dir, file_name)
            in_path = os.path.abspath(os.path.join(current_dir, dir_path, file_name))
            if user_root_dir in in_path:
                shutil.move(out_path, in_path)
            else:
                print('Нельзя подняться выше корневой папки')
        except FileNotFoundError:
            print(f'Файла "{file_name}" не существует внутри текущей папки\nИли относительный путь к директории указан неверно')
    else:
        print('Вам следует передать 2 параметра: имя файла для перемещения и путь в директорию')


# функция для изменения имени файла
def chname(*params):
    if len(params) == 2:
        old_name = params[0]
        new_name = params[1]
        try:
            old_path = os.path.join(current_dir, old_name)
            new_path = os.path.join(current_dir, new_name)
            os.rename(old_path, new_path)
        except FileNotFoundError:
            print(f'Файла "{old_name}" не существует внутри текущей папки')
    else:
        print('Вам следует передать 2 параметра: текущее и новое имя файла')


# функция для регистрации нового пользователя
def reguser(*params):
    if len(params) == 2:
        username = params[0]
        password = params[1]
        try:
            exist = False  # флаг для проверки того, что пользователь уже существует
            with open('users.txt', 'r') as file:
                for line in file:
                    stored_username, _ = line.strip().split(':')
                    if stored_username == username:
                        print(f"Пользователь с именем '{username}' уже существует")
                        exist = True
            if not exist:  # если пользователя нет, то создаем
                os.mkdir(os.path.join(root_dir, username))
                hashed_password = hashlib.sha256(password.encode()).hexdigest()  # хэшируем пароль
                with open('users.txt', 'a') as file:
                    file.write(f"{username}:{hashed_password}\n")
        except Exception as e:
            print(f"Ошибка регистрации пользователя '{username}': {e}")
    else:
        print('Вам следует передать 2 параметра: имя нового пользователя и пароль')


# сменить пользователя
def chuser(*params):
    global current_dir, user_root_dir
    if len(params) == 2:
        username = params[0]
        password = params[1]
        try:
            right_name_password = False
            # хэшируем введенный пользователем пароль для сравнения с хэшем из файла
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            with open('users.txt', 'r') as file:  # ищем пользователя и проверяем пароль
                for line in file:
                    stored_username, stored_hashed_password = line.strip().split(':')
                    if stored_username == username and stored_hashed_password == hashed_password:
                        current_dir = os.path.join(root_dir, username)
                        user_root_dir = os.path.join(root_dir, username)
                        right_name_password = True
            if not right_name_password:
                print("Неверное имя пользователя или пароль")
        except Exception as e:
            print(f"Ошибка аутентификации пользователя '{username}': {e}")
    else:
        print('Вам следует передать 2 параметра: имя пользователя и пароль')


# функция для вывода содержимого текущей директории
def dflist():
    try:
        files_and_directories = os.listdir(current_dir)
        if files_and_directories:
            for item in files_and_directories:
                print(item)
        else:
            print("Нет файлов и папок в текущей директории")
    except Exception as e:
        print(f"Ошибка: {e}")


# функция для ознакомления со всеми командами
def help():
    with open('commands.txt', 'r') as file:
        print(file.read())


# список названий команд
command_list = ['mkdir', 'rmdir', 'cd', 'mkfile', 'write', 'read', 'rmfile', 'copy', 'move', 'chname', 'reguser', 'chuser', 'dflist', 'help']
while True:  # основной цикл программы
    print(f'{current_dir}: ', end='')  # вывод текущей директории для пользователя
    command = input().split()
    try:
        command_name = command[0]
        command_key = command[1:]
        if command_name in command_list:  # команда существует
            if command_key or command_name in ['dflist', 'help']:  # нужны ли параметры
                globals()[command_name](*command_key)  # по текстовому имени команды вызываем ее с помощью глобального пространства имен
            else:
                print('Вы не передали параметры')
        else:
            print('Такой команды не существует')
    except IndexError:
        # выход из программы
        if (input('Если вы хотите завершить работу напишите "true", иначе любое другое сообщение\n')) == 'true':
            break
        else:
            print('Вы не передали название команды')