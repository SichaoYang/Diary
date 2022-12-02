from datetime import datetime, timedelta
from typing import List
import pandas as pd

max_idle_time: timedelta = timedelta(minutes=5)


class Log:
    def __init__(self, name: str, date: str, time: str, idle_ms: str):
        self.name: str = name
        self.date_time: datetime = datetime.strptime(f"{date}{time}", '%Y%m%d%H:%M')
        self.idle_time: timedelta = timedelta(seconds=float(idle_ms) / 1000)


def remove_idle_logs(logs: List[Log]) -> List[Log]:
    clean_logs: List[Log] = []
    idle_start_time = datetime.max
    for log in reversed(logs):
        if idle_start_time < log.date_time:
            continue
        if log.idle_time > max_idle_time:
            idle_start_time = log.date_time - log.idle_time
        else:
            clean_logs.append(log)
    clean_logs.reverse()
    return clean_logs


class Activity:
    def __init__(self, name: str, start_time: datetime, end_time: datetime):
        self.name: str = name
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return f"{self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')} {self.name}"


def aggregate_activities(logs: List[Log]) -> List[Activity]:
    activities: List[Activity] = []
    name_to_last_activity_index = {}
    for log in logs:
        if log.name in name_to_last_activity_index:
            index: int = name_to_last_activity_index[log.name]
            if log.date_time - activities[index].end_time < max_idle_time:
                activities[index].end_time = log.date_time
                continue
        name_to_last_activity_index[log.name] = len(activities)
        activities.append(Activity(log.name, log.date_time, log.date_time))
    return activities


def process_log(date: str):
    # input
    df: pd.DataFrame = pd.read_csv(f"../logs/raw/{date}.csv", names=["time", "idle", "name"])
    logs: List[Log] = []
    for _, row in df.iterrows():
        logs.append(Log(row["name"], date, row["time"], row["idle"]))

    # process
    logs = remove_idle_logs(logs)
    activities: List[Activity] = aggregate_activities(logs)

    # output
    file = open(f"../logs/{date}.txt", "w")
    for activity in activities:
        file.write(f"{activity}\n")
