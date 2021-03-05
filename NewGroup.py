from config import MONGODB_URL
from pymongo import MongoClient


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
    return output
