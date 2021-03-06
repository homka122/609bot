from config import MONGODB_URL
from pymongo import MongoClient
from pymongo import errors as mongodbErrors


def info():
    client = MongoClient(MONGODB_URL)
    collection = client['Homka122']['Groups']
    output = ""
    for pj in list(collection.find()):
        output += f"Название проекта: {pj['_id']}\n"
        if pj['limit']:
            output += f"Лимит участников: {pj['limit']}\n"
        output += f"Темы:\n"
        for theme_name, theme in pj['themes'].items():
            output += f"ᅠ{theme_name.capitalize()}:\n"
            for person in theme:
                output += f"ᅠᅠ{person}\n"
        output += "\n"
    client.close()
    return output


def create_project(name, limit=0):
    client = MongoClient(MONGODB_URL)
    collection = client['Homka122']['Groups']
    try:
        collection.insert_one({"_id": name, "limit": limit, "themes": {}})
        print("Проект выполнен")
    except mongodbErrors.DuplicateKeyError:
        print("Данный проект уже существует")
    client.close()


def create_theme(name_project, name):
    client = MongoClient(MONGODB_URL)
    collection = client['Homka122']['Groups']
    theme = collection.find_one({"_id": name_project, f"themes.{name}": {"$exists": "true"}})
    if not theme:
        collection.update_one({"_id": name_project}, {"$set": {f"themes.{name}": []}})
        print("Тема создана")
    else:
        print("Тема существует")
    client.close()


def insert_user(name_project, name, user):
    client = MongoClient(MONGODB_URL)
    collection = client['Homka122']['Groups']
    users = collection.find_one({"_id": name_project})['themes'][name]
    if user in users:
        print("Данный пользователь уже в группе")
    else:
        collection.update_one({"_id": name_project}, {"$push": {f"themes.{name}": user}})
    client.close()


def delete_user(name_project, name, user):
    client = MongoClient(MONGODB_URL)
    collection = client['Homka122']['Groups']
    users = collection.find_one({"_id": name_project})['themes'][name]
    if not (user in users):
        print("Данный пользователя нет в группе")
    else:
        collection.update_one({"_id": name_project}, {"$pull": {f"themes.{name}": user}})
    client.close()
