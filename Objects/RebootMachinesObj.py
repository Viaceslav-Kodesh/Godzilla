import random
import time


class RebootMachinesObj:
    __machines = None
    __close_time = None
    __percent = None
    __groups = None

    def __init__(self, machines, groups, close_time, percent):
        self.__machines = machines
        self.__close_time = close_time
        self.__percent = percent
        self.__groups = groups

    def reboot_percent_machines(self):

        machines = self.check_groups()
        count_machines = len(machines)
        count_reboot_machines = int((count_machines * self.__percent) / 100)
        self.__reboot(count_reboot_machines, machines)

    def check_groups(self):
        items = []
        groups_machines_id = []
        for group in self.__groups:
            for machine in group.members:
                groups_machines_id.append(machine)

        for machine in self.__machines:
            if machine.id not in groups_machines_id:
                items.append(machine)

        return items

    def __reboot(self, count_reboot_machines, machines):
        for i in range(0, count_reboot_machines):
            value = random.randint(0, len(machines) - 1)
            reboot_type = 'HARD'
            if machines[value].status == 'ACTIVE':
                try:
                    machines[value].reboot(reboot_type)
                except:
                    while True:
                        y = random.randint(0, len(machines) - 1)
                        if value != y:
                            break
                    value = y
                    machines[value].reboot(reboot_type)
                print('Server {0} is in state {1}'.format(machines[value].name, machines[value].status))
                while True:
                    if machines[value].status == 'ACTIVE':
                        break
                    if self.check_total_time():
                        break

            if self.check_total_time():
                break

    def check_total_time(self):
        return time.time() > self.__close_time;
