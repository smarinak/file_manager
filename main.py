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


while True:
    print(f'{current_dir}: ', end='')
    command = input().split()
    try:
        command_name = command[0]
        command_key = command[1:]
        if command_name in ['make_dir']:
            globals()[command_name](*command_key)
        else:
            print('Такой команды не существует')
    except IndexError:
        print('Вы не передали название команды')