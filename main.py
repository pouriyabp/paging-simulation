from operator import attrgetter


class Process:
    def __init__(self, name, time, deadline, period, size):
        self.name = name
        self.time = time
        self.tempTime = time
        self.deadline = deadline
        self.tempDeadline = deadline
        self.period = period
        self.tempPeriod = period
        self.size = size
        self.tempSize = size
        self.priority = 0  # set process priority

    def __repr__(self):
        return f"{self.name}"

    def set_priority_for_edf(self):
        """
        set priority for earliest deadline first
        :return: nothing return ---> set priority of each food
        """
        self.priority = self.tempDeadline


def lcm(x, y):
    """
    calculate the LCM between 2 number
    :param x: first number
    :param y: second number
    :return: the LCM between x and y
    """
    if x > y:
        greater = x
    else:
        greater = y
    while (True):
        if (greater % x == 0) and (greater % y == 0):
            lcm = greater
            break
        greater += 1
    return lcm


def calculate_whole_time(list_of_process):
    # first check the lcm between process
    time = 1
    for process in list_of_process:
        time = lcm(process.period, time)
    return time


def earliest_deadline_first(list_of_process, whole_time):
    # get time and return which process must go to cpu and what processes are in the list
    temp_list = list_of_process.copy()
    # in this list save process after scheduling
    scheduling_process = []
    i = 0

    while i <= whole_time:
        if len(temp_list) == 0:
            scheduling_process.append(None)
            i += 1
            for process in list_of_process:
                if i % process.period == 0:
                    temp_list.append(process)
            continue
        if i == 0:
            scheduling_process.append(None)
            print(None)
            i += 1
            continue
        min_process = min(temp_list, key=attrgetter('tempDeadline'))
        min_process.tempTime -= 1
        print(f"{i - 1} {min_process}")
        scheduling_process.append(min_process)
        # remove food if it's done
        if min_process.tempTime == 0:
            min_process.priority = 0
            min_process.tempDeadline = min_process.deadline
            min_process.tempTime = min_process.time
            temp_list.remove(min_process)
        for process in temp_list:
            process.tempDeadline -= 1
        i += 1
        if i < whole_time:
            for process in list_of_process:
                if i % process.period == 0:
                    temp_list.append(process)
    return scheduling_process


process1 = Process("process1", 1, 5, 6, 10)
process2 = Process("process2", 2, 4, 5, 6)
process3 = Process("process3", 4, 8, 10, 15)
list_of_process = [process1, process2, process3]
max_time = calculate_whole_time(list_of_process)
print(max_time)
print(earliest_deadline_first(list_of_process, max_time))
