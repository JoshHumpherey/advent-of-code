from typing import Dict, List
from lib.parse import parse_strings
from datetime import datetime

class TimeSheet:

    def __init__(self, id: str):
        self.id = id
        self.mins = [0]*60

    def total_sleep_time(self) -> int:
        return sum(self.mins)
    
    def sleepiest_minute(self) -> int:
        idx = 0
        best = 0

        for i in range(len(self.mins)):
            if self.mins[i] >= best:
                idx = i
                best = self.mins[i]
        
        return idx

    def add_shift(self, start_time: str, end_time: str) -> None:
        while start_time != end_time:
            raw_hours, raw_mins = start_time.split(":")
            hours, mins = int(raw_hours), int(raw_mins)
            self.mins[mins] += 1

            mins += 1
            if mins >= 60:
                hours += 1
                mins = 0
            if hours >= 24:
                hours = 0
            
            start_time = f"{str(hours).zfill(2)}:{str(mins).zfill(2)}"

def sort_events(raw_events: List[str]) -> List[str]:
    def timestamp_sort_key(s):
        timestamp_str = s[s.index('[') + 1:s.index(']')]
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M')
        return timestamp

    return sorted(raw_events, key=timestamp_sort_key)

def create_timesheets() -> List[TimeSheet]:
    data = parse_strings("2018/day4/input.txt")
    shifts = []
    curr = []
    timesheets: Dict[str, TimeSheet] = {}

    for d in sort_events(data):
        if not curr:
            curr.append(d)
        elif "#" in d:
            shifts.append(curr)
            curr = [d]
        else:
            curr.append(d)

    if len(curr) != 0:
        shifts.append(curr)
    
    for s in shifts:
        id = s[0].split(" ")[3][1:]
        if id not in timesheets:
            timesheets[id] = TimeSheet(id=id)

        for i in range(1, len(s)):
            if "wakes up" in s[i]:
                raw_end_time = s[i].split(" ")[1]
                raw_start_time = s[i-1].split(" ")[1]
                start_time, end_time = raw_start_time[:len(raw_start_time)-1], raw_end_time[:len(raw_end_time)-1]
                timesheets[id].add_shift(start_time, end_time)
    
    return timesheets.values() # type: ignore

def strategy_1() -> int:
    timesheets = create_timesheets()
    max_timesheet = TimeSheet(id="")
    max_time = 0

    for t in timesheets:
        if t.total_sleep_time() >= max_time:
            max_time = t.total_sleep_time()
            max_timesheet = t
    
    return int(max_timesheet.id) * max_timesheet.sleepiest_minute()

def strategy_2() -> int:
    timesheets = create_timesheets()
    max_timesheet = TimeSheet(id="")
    max_time = 0

    for t in timesheets:
        if t.mins[t.sleepiest_minute()] >= max_time:
            max_time = t.mins[t.sleepiest_minute()]
            max_timesheet = t

    return int(max_timesheet.id) * max_timesheet.sleepiest_minute()

print(strategy_1())
print(strategy_2())



    

