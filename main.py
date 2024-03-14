import os
import settings

work_dir = settings.working_directory
current_dir = settings.working_directory


def mkdir(*dir_names):
    try:
        for name in dir_names:
            os.mkdir(os.path.join(current_dir, name))
    except FileExistsError:
        print(f'Папка с именем "{name}" уже существует')


def rm(*dir_names):
    try:
        for name in dir_names:
            os.rmdir(os.path.join(current_dir, name))
    except FileNotFoundError:
        print(f'Папки с именем "{name}" не существует внутри текущей директории')
    except OSError:
        print('Ошибка удаления папки')  # пояснить!!!


def cd(*dir_name):
    global current_dir
    if len(dir_name) > 1:
        print('Вам следует передать только 1 параметр')
    else:
        if dir_name[0] == '..':
            if current_dir != work_dir:
                current_dir = os.path.dirname(os.path.join(dir_name[0], current_dir))  # пояснить!!!
            else:
                print('Нельзя подняться выше корневой папки')
        else:
            new_dir = os.path.join(current_dir, dir_name[0])
            if os.path.isdir(new_dir):
                current_dir = new_dir
            else:
                print('Такой папки не существует внутри текущей')


def mkfile(*file_names):
    try:
        for name in file_names:
            file_path = os.path.join(current_dir, name)
            open(file_path, 'w').close()
    except FileExistsError:
        print(f'Файл с именем "{name}" уже существует')


def write(*params):
    file_name = params[0]
    text = ' '.join(params[1:])
    try:
        file_path = os.path.join(current_dir, file_name)
        with open(file_path, 'w') as file:
            file.write(text)
    except IsADirectoryError:
        print(f'"{file_name[0]}" является директорией')
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



while True:
    print(f'{current_dir}: ', end='')
    command = input().split()
    try:
        command_name = command[0]
        command_key = command[1:]
        if command_name in ['mkdir', 'rm', 'cd', 'mkfile', 'write', 'read']:
            if command_key:
                globals()[command_name](*command_key)  # пояснить!!!
            else:
                print('Вы не передали параметры')
        else:
            print('Такой команды не существует')
    except IndexError:
        print('Вы не передали название команды')