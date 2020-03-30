class DataObj:
    def __init__(self, data):
        self.id = data['id']
        self.server_group = data
        self.name = data['name']
        self.members = data['members']
        self.policies = data['policies']
# описывает один элемент группы из массива групп, полученных из массива групп реквеста