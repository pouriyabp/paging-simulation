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
        self.frameSize = -1
        self.splitProcess = []

    def get_frame_size(self, frame_size):
        self.frameSize = frame_size

    def split_process(self):
        count = self.size / self.frameSize
        if int(count) < count:
            count = int(count) + 1
        else:
            count = int(count)
        for n in range(count):
            self.splitProcess.append(self.name + "-chunk" + str(n + 1))

    def __repr__(self):
        return f"{self.name}"

    def set_priority_for_edf(self):
        """
        set priority for earliest deadline first
        :return: nothing return ---> set priority of each food
        """
        self.priority = self.tempDeadline


class Ram:
    def __init__(self, size_of_memory, frame_size):
        self.size = size_of_memory
        self.frameSize = frame_size

        count_of_frames = int(self.size / self.frameSize)
        self.arr_of_frames = Ram.split_memory(count_of_frames)

    @staticmethod
    def split_memory(count_of_frames):
        arr_of_frames = []
        for n in range(count_of_frames):
            arr_of_frames.append(None)
        return arr_of_frames

    def __repr__(self):
        text = "-----------------------\n"
        for n in self.arr_of_frames:
            text += "|" + str(n) + "|\n"
            text += "-----------------------\n"
        return text


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
            x = (None, temp_list)
            scheduling_process.append(x)
            i += 1
            for process in list_of_process:
                if i % process.period == 0:
                    temp_list.append(process)
            continue
        if i == 0:
            scheduling_process.append(None)
            # print(None)
            i += 1
            continue
        min_process = min(temp_list, key=attrgetter('tempDeadline'))
        min_process.tempTime -= 1
        # print(f"{i - 1} {min_process}")

        x = (min_process, tuple(temp_list))
        scheduling_process.append(x)
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
    # remove first None in list
    scheduling_process.remove(None)
    return scheduling_process


def set_frame_size(list_of_process, ram):
    for process in list_of_process:
        process.get_frame_size(ram.frameSize)
        process.split_process()


def calculate_memory_process(list_of_process, result_scheduling, whole_time, ram):
    for i in range(whole_time):
        time = f"{i}-{i + 1}"
        temp = result_scheduling[i]
        process_in_cpu = temp[0]
        temp_list = temp[1]
        print(f"{time}: {process_in_cpu} is in the CPU.")
        print(f"list of process that are wait: {list(temp_list)}")

        # calculate function are in ram
        # ==============================================================================================================
        # # remove process that are finished (not in temp list or waiting list)
        # for process in list_of_process:
        #     if process not in temp_list:
        #         for i in range(len(ram.arr_of_frames)):
        #             if ram.arr_of_frames[i] in process.splitProcess:
        #                 ram.arr_of_frames[i] = None
        # ==============================================================================================================
        list_of_process_in_the_hard = []
        # put chunk of process must be in ram
        if process_in_cpu is not None:
            # check that chunk are in the ram or not
            all_chunk_in_ram = True
            for chunk in process_in_cpu.splitProcess:
                if chunk in ram.arr_of_frames:
                    continue
                else:
                    all_chunk_in_ram = False
                    break
            # if chunk are not in ram then put them in ram
            if all_chunk_in_ram is False:
                for chunk in process_in_cpu.splitProcess:
                    put_chunk = False
                    for i in range(len(ram.arr_of_frames)):
                        if ram.arr_of_frames[i] is None:
                            ram.arr_of_frames[i] = chunk
                            put_chunk = True
                            break
                    if put_chunk is False:
                        for i in range(len(ram.arr_of_frames)):
                            if ram.arr_of_frames[i] not in process_in_cpu.splitProcess:
                                # process that go to hard because no enough space in ram
                                edit = ram.arr_of_frames[i]
                                edit = edit.split("-")
                                list_of_process_in_the_hard.append(edit[0])
                                # replace that process with chunk
                                ram.arr_of_frames[i] = chunk
                                break
        print(f"process is going to hard: {(list(dict.fromkeys(list_of_process_in_the_hard)))}")
        # ==============================================================================================================
        # remove process if part of it is not in list of frames
        for i in range(len(ram.arr_of_frames)):
            if ram.arr_of_frames[i] is not None:
                for process in list_of_process:
                    if ram.arr_of_frames[i] in process.splitProcess:
                        is_all_in = True
                        for chunk in process.splitProcess:
                            if chunk in ram.arr_of_frames:
                                continue
                            else:
                                is_all_in = False
                                break
                        if is_all_in is False:
                            for i in range(len(ram.arr_of_frames)):
                                if ram.arr_of_frames[i] in process.splitProcess:
                                    ram.arr_of_frames[i] = None
        # ==============================================================================================================

        print(ram)


ram = Ram(20, 2)
process1 = Process("process1", 1, 5, 6, 16)
process2 = Process("process2", 2, 4, 5, 4)
process3 = Process("process3", 4, 8, 10, 8)
list_of_process = [process1, process2, process3]

set_frame_size(list_of_process, ram)
print(process1.splitProcess)
print(process2.splitProcess)
print(process3.splitProcess)
max_time = calculate_whole_time(list_of_process)
print(f"max time is {max_time}")
result_scheduling = earliest_deadline_first(list_of_process, max_time)
calculate_memory_process(list_of_process, result_scheduling, max_time, ram)
