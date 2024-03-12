import os
import settings

work_dir = settings.working_directory
current_dir = settings.working_directory


def make_dir(*dir_names):
    if not command_key:
        print('Вы не передали параметры')
    else:
        try:
            for name in dir_names:
                os.mkdir(os.path.join(current_dir, name))
        except FileExistsError:
            print(f'Папка с именем "{name}" уже существует')


def delete_dir(*dir_names):
    if not command_key:
        print('Вы не передали параметры')
    else:
        try:
            for name in dir_names:
                os.rmdir(os.path.join(current_dir, name))
        except FileNotFoundError:
            print(f'Папки с именем "{name}" не существует внутри текущей директории')
        except OSError:
            print('Ошибка удаления папки')


while True:
    print(f'{current_dir}: ', end='')
    command = input().split()
    try:
        command_name = command[0]
        command_key = command[1:]
        if command_name in ['make_dir', 'delete_dir']:
            globals()[command_name](*command_key)
        else:
            print('Такой команды не существует')
    except IndexError:
        print('Вы не передали название команды')