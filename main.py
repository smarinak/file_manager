import os
import shutil
import hashlib

import settings

root_dir = settings.working_directory
user_root_dir = settings.user_working_directory
current_dir = settings.user_working_directory


def mkdir(*dir_names):
    for name in dir_names:
        try:
            os.mkdir(os.path.join(current_dir, name))
        except FileExistsError:
            print(f'Папка с именем "{name}" уже существует')


def rmdir(*dir_names):
    for name in dir_names:
        try:
            shutil.rmtree(os.path.join(current_dir, name))
        except FileNotFoundError:
            print(f'Папки с именем "{name}" не существует внутри текущей директории')
        except OSError:
            print('Ошибка удаления папки')


def cd(*dir_name):
    global current_dir
    if len(dir_name) > 1:
        print('Вам следует передать только 1 параметр')
    else:
        if '..' in dir_name[0]:
            if user_root_dir not in current_dir:
                current_dir = os.path.abspath(os.path.join(current_dir, dir_name[0]))
            else:
                print('Нельзя подняться выше корневой папки')
        else:
            new_dir = os.path.join(current_dir, dir_name[0])
            if os.path.isdir(new_dir):
                current_dir = new_dir
            else:
                print('Такой папки не существует внутри текущей')


def mkfile(*file_names):
    for name in file_names:
        try:
            file_path = os.path.join(current_dir, name)
            open(file_path, 'w').close()
        except FileExistsError:
            print(f'Файл с именем "{name}" уже существует')


def write(*params):
    if len(params) > 1:
        print('Вам следует передать только 1 параметр')
    else:
        try:
            file_name = params[0]
            file_path = os.path.join(current_dir, file_name)
            with open(file_path, 'w') as file:
                print("Введите текст. Введите пустую строку, чтобы закончить")
                lines = []
                while True:
                    line = input("> ")
                    if not line:
                        break
                    lines.append(line + "\n")
                file.writelines(lines)
        except IsADirectoryError:
            print(f'"{file_name}" является директорией')
        except PermissionError:
            print(f'Доступ для записи в файл "{file_name}" запрещен')


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


def rmfile(*file_names):
    for name in file_names:
        try:
            file_path = os.path.join(current_dir, name)
            os.remove(file_path)
        except FileNotFoundError:
            print(f'Файла "{name}" не существует внутри текущей папки')


def copy(*params):
    if len(params) == 2:
        file_name = params[0]
        dir_path = params[1]
        try:
            out_path = os.path.join(current_dir, file_name)
            in_path = os.path.abspath(os.path.join(current_dir, dir_path, file_name))
            if user_root_dir in in_path:
                shutil.copyfile(out_path, in_path)
            else:
                print('Нельзя подняться выше корневой папки')
        except FileNotFoundError:
            print(f'Файла "{file_name}" не существует внутри текущей папки\nИли относительный путь к директории указан неверно')
        except shutil.SameFileError:
            print('Нельзя копировать файл в ту же самую директорию')
    else:
        print('Вам следует передать 2 параметра: имя файла для копирования и путь в директорию')


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


def reguser(*params):
    if len(params) == 2:
        username = params[0]
        password = params[1]
        try:
            exist = False
            with open('users.txt', 'r') as file:
                for line in file:
                    stored_username, _ = line.strip().split(':')
                    if stored_username == username:
                        print(f"Пользователь с именем '{username}' уже существует")
                        exist = True
            if not exist:
                os.mkdir(os.path.join(root_dir, username))
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                with open('users.txt', 'a') as file:
                    file.write(f"{username}:{hashed_password}\n")
        except Exception as e:
            print(f"Ошибка регистрации пользователя '{username}': {e}")
    else:
        print('Вам следует передать 2 параметра: имя нового пользователя и пароль')


def chuser(*params):
    global current_dir, user_root_dir
    if len(params) == 2:
        username = params[0]
        password = params[1]
        try:
            right_name_password = False
            # Хэшируем введенный пользователем пароль для сравнения с хэшем из файла
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            with open('users.txt', 'r') as file:
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


command_list = ['mkdir', 'rmdir', 'cd', 'mkfile', 'write', 'read', 'rmfile', 'copy', 'move', 'chname', 'reguser', 'chuser', 'dflist']
while True:
    print(f'{current_dir}: ', end='')
    command = input().split()
    try:
        command_name = command[0]
        command_key = command[1:]
        if command_name in command_list:
            if command_key or command_name == 'dflist':
                globals()[command_name](*command_key)
            else:
                print('Вы не передали параметры')
        else:
            print('Такой команды не существует')
    except IndexError:
        if (input('Если вы хотите завершить работу напишите "true", иначе любое другое сообщение\n')) == 'true':
            break
        else:
            print('Вы не передали название команды')