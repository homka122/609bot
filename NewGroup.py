import json

with open("homka.json", 'r', encoding='UTF-8') as f:
    all_projects = json.load(f)


def parse_text(text):
    data = {'count': 1, 'themes': [], 'limit': {'exist': 0, "count": 0}, 'cmd': '', "project": '', "error": 0}
    if len(text) >= 2:
        data['cmd'] = text[1]
        data['count'] += 1
    if len(text) >= 3:
        data['project'] = text[2]
        data['count'] += 1
    for i in range(3, len(text)):
        if text[i] == "лимит":
            data['limit']["exist"] = 1
            data['count'] += 1
            if i != len(text) - 1:
                data['limit']["count"] = int(text[i+1])
                data['count'] += 1
                break
            else:
                break
        else:
            data['themes'].append(text[i])
            data['count'] += 1
    if data['limit']['exist'] and not data['limit']['count']:
        data['error'] = 1
    if data['count'] != len(text):
        data['error'] = 1
    return data


def new_group(bot, text):
    print(all_projects)
    text = text.split()
    map(str.lower, text)
    data = parse_text(text)

    if data['count'] == 1:
        bot.write_msg(help_text()),
        return 0

    cmd = data['cmd']
    if cmd == "добавить":
        result = add_new_themes(data, bot)
        if type(result) == type(int()):
            all_projects[data['project']]['limit'] = result
            bot.write_msg("Лимит установлен")
        elif result:
            all_projects[data['project']]['themes'].update(result)
            bot.write_msg("Добавлены новые темы проекта")
    elif cmd == "вступить":
        join_to_project(all_projects, data, bot)
    elif cmd == "инфо":
        info(all_projects, data, bot)
    elif cmd == "создать":
        new_project = add_new_project(all_projects, data, bot)
        if new_project:
            all_projects.update(new_project)
            bot.write_msg("Проект успешно добавлен")
    else:
        bot.write_msg(help_text())

    return all_projects


def add_new_themes(data, bot):
    themes = data['themes']
    if not themes and not data['limit']['exist']:
        bot.write_msg("Введите темы, которые нужно добавить или лимит, который нужно установить")
        return {}
    if data['limit']['exist'] and data['limit']['count']:
        return data['limit']['count']
    new_themes = {}
    for theme in themes:
        new_themes.update({theme: []})
    return new_themes


def join_to_project(projects, data, bot):
    error = False
    error_message = ''
    if not (data['project'] in projects):
        error = True
        error_message += 'Проект с этим именем не существует\n'
    elif not (data['themes']):
        error = True
        error_message += 'Введите тему\n'
    elif not (data['themes'][0] in projects[data['project']]['themes']):
        error = True
        error_message += 'Такой темы нет\n'
    elif bot.get_full_name() in projects[data['project']]['themes'][data['themes'][0]]:
        error = True
        error_message += 'Вы уже состоите в этой Теме\n'
    if len(data['themes']) > 1:
        error = True
        error_message += 'Тема должна быть одна\n'
    if data['error']:
        error = True
        error_message += 'Иная ошибка\n'
    if projects[data['project']]['limit'] == len(projects[data['project']]['themes'][data['themes'][0]]):
        error = True
        error_message += 'Места нет!\n'
    if error:
        bot.write_msg(error_message)
        return 0
    else:
        all_projects[data['project']]['themes'][data['themes'][0]].append(bot.get_full_name())
        bot.write_msg("Вы успешно вступили!")


def add_new_project(projects, data, bot):
    name_of_project = data['project']
    error = False
    error_message = ""
    if name_of_project in projects:
        error = True
        error_message += 'Проект с этим именем уже существует\n'
    if not data['themes']:
        error = True
        error_message += 'Добавьте темы проекта\n'
    if data['error']:
        error = True
        error_message += 'Еще какая-либо ошибка\n'
    if error:
        bot.write_msg(error_message)
        return 0

    new_project = {name_of_project: {"limit": data['limit']['count'], "themes": {}}}
    for name_theme in data['themes']:
        new_project[name_of_project]["themes"].update({name_theme: []})
    return new_project


def help_text():
    help_text = "Название проекта - 1 слово, Название Темы - 1 слово, можно использовать -\\._ и тд\n"
    help_text += "•нгру создать (название проекта)(Темы)(Лимит n, необязательно) - создает проект с темами\n"
    help_text += "•нгру добавить (название проекта)(темы или лимит n) - добавляет темы проекту или меняет лимит\n"
    help_text += "•нгру инфо (необязально: название проекта) - показывает Проекты, Темы, Участников, Лимит, если таковой есть\n"
    help_text += "•нгру вступить (название проекта)(1 Тема) - добавляет вас в Тему соотвествующего проекта\n"
    help_text += "•нгру удалить лимит (название проекта) - Удаляет лимит (не реализовано)\n"
    help_text += "•нгру выйти (название проекта)(1 Тема) - Вы выходите из темы определенной группы (не реализовано)\n"
    return help_text


def info(projects, data, bot):
    named_project = data['project']
    if named_project:
        if named_project in projects:
            temp = projects[named_project]
            projects.clear()
            projects[named_project] = temp
        else:
            bot.write_msg("Данный проект не существует")
            return 0
    output = ""
    i = 0
    for project_name, project in projects.items():
        i += 1
        # "ᅠ" - невидимый символ
        output += f"Название проекта: {project_name}\n"
        if project['limit']:
            output += f"Лимит участников: {project['limit']}\n"
        output += f"Темы:\n"
        for theme_name, theme in project['themes'].items():
            output += f"ᅠ{theme_name.capitalize()}:\n"
            for person in theme:
                output += f"ᅠᅠ{person}\n"

        if not (len(projects) == i):
            output += "\n"
    bot.write_msg(output)
