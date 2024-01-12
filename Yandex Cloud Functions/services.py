import datetime

import ydb

def insert_activity(pool: ydb.Session, path, user_id, name):
    qtext = """
    DECLARE $user_id AS Utf8;
    DECLARE $name AS Utf8;
    DECLARE $created_at AS Datetime;
    UPSERT INTO activities (user_id, name, created_at) VALUES ($user_id, $name, $created_at);
    """.format(path)

    def fun(session: ydb.Session):
        session.transaction(ydb.SerializableReadWrite()).execute(
            query=session.prepare(qtext), 
            parameters={
                '$user_id': user_id,
                '$name': name,
                '$created_at': int(round(datetime.datetime.now().timestamp())),
            },
            commit_tx=True
        )

    pool.retry_operation_sync(fun)
    

def insert_action(pool: ydb.Session, path, user_id, name, minutes):
    qtext = """
    DECLARE $user_id AS Utf8;
    DECLARE $name AS Utf8;
    DECLARE $start AS Datetime;
    DECLARE $end AS Datetime;
    DECLARE $technique AS Utf8;
    UPSERT INTO actions (user_id, activity_name, start, end, technique) VALUES ($user_id, $name, $start, $end, "Pomodoro");
    """.format(path)

    def fun(session: ydb.Session):
        session.transaction(ydb.SerializableReadWrite()).execute(
            query=session.prepare(qtext), 
            parameters={
                '$user_id': user_id,
                '$name': name,
                '$start': int(round(datetime.datetime.now().timestamp())),
                '$end': int(round((datetime.datetime.now() + datetime.timedelta(minutes=minutes)).timestamp())),
            },
            commit_tx=True
        )

    pool.retry_operation_sync(fun)


def insert_action_interval(pool: ydb.Session, path, user_id, name, start, end):
    qtext = """
    DECLARE $user_id AS Utf8;
    DECLARE $name AS Utf8;
    DECLARE $start AS Datetime;
    DECLARE $end AS Datetime;
    DECLARE $technique AS Utf8;
    UPSERT INTO actions (user_id, activity_name, start, end, technique) VALUES ($user_id, $name, $start, $end, "Pomodoro");
    """.format(path)

    def fun(session: ydb.Session):
        session.transaction(ydb.SerializableReadWrite()).execute(
            query=session.prepare(qtext), 
            parameters={
                '$user_id': user_id,
                '$name': name,
                '$start': int(start.strftime("%s")),
                '$end': int(end.strftime("%s")),
            },
            commit_tx=True
        )

    pool.retry_operation_sync(fun)


def get_activity_by_name(pool: ydb.Session, path, user_id, name):
    qtext = """
    DECLARE $user_id AS Utf8;
    DECLARE $name AS Utf8;
    SELECT * FROM actions
    WHERE `activity_name` = $name AND `user_id` = $user_id;
    """.format(path)

    def fun(session: ydb.Session):
        result_sets = session.transaction(ydb.SerializableReadWrite()).execute(
            query=session.prepare(qtext), 
            parameters={
                '$user_id': user_id,
                '$name': name,
            },
            commit_tx=True
        )

    rs = pool.retry_operation_sync(fun)
    if rs is None or len(rs) == 0:
        return None
    
    return rs[0]


def get_actions_by_period(pool: ydb.Session, path, user_id, period):
    def callee(session):
        query = """
        DECLARE $user_id AS Utf8;
        DECLARE $start AS Datetime;

        SELECT * FROM actions
        WHERE user_id = $user_id AND start >= $start
        ORDER BY start;
        """.format(
            path
        )

        now = datetime.datetime.utcnow() + datetime.timedelta(hours=6)
        today = datetime.datetime(year=now.year, month=now.month, day=now.day)
        end = (today + datetime.timedelta(hours=23, minutes=59, seconds=59))

        if period == "месяц":
            start = today - datetime.timedelta(weeks=4)
        elif period == "неделю":
            start = today - datetime.timedelta(weeks=1)
        else:
            start = today

        prepared_query = session.prepare(query)
        result_sets = session.transaction(ydb.SerializableReadWrite()).execute(
            prepared_query,
            {
                "$user_id": user_id,
                "$start": int(start.strftime("%s")),
            },
            commit_tx=True,
        )
        return result_sets[0].rows

    return pool.retry_operation_sync(callee)
