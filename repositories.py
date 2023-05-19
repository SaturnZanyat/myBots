import json
import re


async def validate_number(number):
    pattern = "\D"
    matter = re.findall(pattern, number)
    if not matter:
        return number
    else:
        return False

async def check_correct_number(answ, number):
    if number == answ:
        return True
    else:
        return False

async def get_answer(request, chat_id, field: str):
    with open("clients.json", "r") as ff:
        data_from_json = json.load(ff)
    data_from_json[chat_id] = {"{0}".format(field): request}
    with open("clients.json", "w") as ff:
        json.dump(data_from_json, ff, indent=4, ensure_ascii=False)