import ydb

import datetime

from chatGPT import get_analysis
from database import ydb_client
from services import insert_activity, get_activity_by_name, insert_action, insert_action_interval, get_actions_by_period
from Analytics import SaveAnalyticsInDatabase, GetAnalyticsFromDatabase
# from normalize_words import normal_form


def handler(event, context):
    text = "Привет! Я помощник вашей продуктивности. Я буду рад поставить таймер для ваших активностей, а также вывести аналитику по вашим активностям за определнный период.\n\nДля знакомства с моим функционалом спроси меня 'Что ты умеешь?'"
    if "request" in event and \
            "original_utterance" in event["request"] \
            and len(event["request"]["original_utterance"]) > 0:

        user_id = event["session"]["user"]["user_id"]
        req = event["request"]["original_utterance"]
        
        productivity = event["request"]["nlu"]["intents"].get("productivity")
        analytics = event["request"]["nlu"]["intents"].get("analytics")

        if req.lower().find("завершить") != -1 or req.lower().find("пока") != -1:
            return {
                "version": event["version"],
                "session": event["session"],
                "request": event["request"],
                "response": {
                    "text": "Рада была помочь",
                    "end_session": "true"
                },
            }
        elif req.lower().find("что ты умеешь") != -1:
            text = "Я умею помгать вам следить за прогрессом.\n\nВы можете попросить меня добавить существующую запись: 'Внеси деятельность английский с 8:00 до 9:00',\n\nпоставить таймер на некоторое количество минут: 'Поставь таймер для английского на 40 минут',\n\nпопросить меня проанализировать ваши успехи за [сегодня, неделю, месяц] и предложить рекомендации: 'Аналитика за неделю'"

        elif req.lower().find("отчет") != -1:
            text = GetAnalyticsFromDatabase(user_id)[0]

        elif (productivity is not None and analytics is not None) or (productivity is None and analytics is None and req.find("деятель") == -1):
            text = "Ваш запрос не корректен, пожалуйста, попробуйте снова!"

        elif productivity is not None:
            how_long = productivity["slots"]["how_long"]["value"]
            action = productivity["slots"]["action"]["value"]
            ###
            # action = normal_form(action)

            with ydb.SessionPool(ydb_client.driver) as pool:
                activity_name = get_activity_by_name(pool, "", user_id, action)
                if activity_name is None:
                    insert_activity(pool, "", user_id, action)
                insert_action(pool, "", user_id, action, how_long)
            
            text = f"Таймер для {action} на {how_long} минут установлен!"
        
        elif analytics is not None:
            period = analytics["slots"].get("when").get("value")
            data = f"за период ({period})\n"
            
            with ydb.SessionPool(ydb_client.driver) as pool:
                result = get_actions_by_period(pool, "", user_id, period)
                date = None
                for a in result:
                    s = ""
                    if date is None or datetime.datetime.fromtimestamp(a.start).date() > date:
                        date = datetime.datetime.fromtimestamp(a.start).date()
                        s += f"\n\nДата {date}:\n"
                    
                    start = datetime.datetime.fromtimestamp(a.start)
                    end = datetime.datetime.fromtimestamp(a.end)
                    s_hour = f"0{start.hour}" if start.hour < 10 else start.hour
                    e_hour = f"0{end.hour}" if end.hour < 10 else end.hour
                    s_minute = f"0{start.minute}" if start.minute < 10 else start.minute
                    e_minute = f"0{end.minute}" if end.minute < 10 else end.minute
                    act = f"{s_hour}:{s_minute}-{e_hour}:{e_minute} - {a.activity_name}\n"
                    s += act
                    data += s
                    #####################################
                    SaveAnalyticsInDatabase(data, period, user_id)

            text = f"Ваша статистика за {period}:\n{data}\n\nИдет сохранение автоматизированного отчета...\n\nВаша аналитика будет доступна через 30 секунд по команде 'Получить отчет'."

        else:
            l = event["request"]["original_utterance"].split(" ")
            action = l[2]
            now = datetime.datetime.utcnow().date()
            start = [l[i+1] for i in range(len(l)) if l[i] == "с"][0].split(":")
            end = [l[i+1] for i in range(len(l)) if l[i] == "до"][0].split(":")
            start = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=int(start[0]), minute=int(start[1]))
            end = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=int(end[0]), minute=int(end[1]))
            with ydb.SessionPool(ydb_client.driver) as pool:
                activity_name = get_activity_by_name(pool, "", user_id, action)
                if activity_name is None:
                    insert_activity(pool, "", user_id, action)
                insert_action_interval(pool, "", user_id, action, start, end)
            
            text = f"Запись для {action} успешно добавлена!"


    return {
        "version": event["version"],
        "session": event["session"],
        "request": event["request"],
        "response": {
            "text": text,
            "end_session": "false"
        },
    }
