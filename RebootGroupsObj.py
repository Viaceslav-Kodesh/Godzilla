import random
import time


class RebootGroupsObj:
    __groups = None
    __close_time = None
    __percent = None
    __nova_client_list = None

    def __init__(self, nova_client, groups, close_time, percent):
        self.__groups = groups
        self.__close_time = close_time
        self.__percent = percent
        self.__nova_client_list = nova_client.servers.list()

    def reboot_percent_machines(self):
        for group in self.__groups:
            count_machines = len(group.members)
            count_reboot_machines = int((count_machines * self.__percent) / 100)
            nova_client_machines = self.get_machines_items(group)
            self.__reboot(count_reboot_machines, nova_client_machines)
            if self.check_total_time():
                break

    def get_machines_items(self, group):
        items = []
        for machine in group.members:
            for nova_item in self.__nova_client_list:
                if nova_item.id == machine:
                    items.append(nova_item)
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
        return time.time() > self.__close_time
