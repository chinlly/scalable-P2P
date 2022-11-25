import json


class Router:
    def __init__(self, name):
        self.name = name  # device name
        self.cs = dict()  # name: data
        self.pit = list(tuple())  # name, ip address, coming interface
        self.fib = list(tuple())  # prefix, ip address, ongoing interface
        with open("interfaces.json", 'r') as load_f:
            load_dict = json.load(load_f)
        # get the current device's neighbours
        # print(self.name)
        neighbours_list = list()
        for i in range(len(load_dict)):
            device_name = list(load_dict[i].keys())[0]
            # print(device_name)
            if device_name == self.name:
                neighbours_dict = load_dict[i][device_name][1]  # neighbours dictionary
                neighbours_list = neighbours_dict[list(neighbours_dict.keys())[0]]  # neighbours list
                # print(neighbours_list)

        # add neighbours into the current fib
        for neighbour_name in neighbours_list:
            for i in range(len(load_dict)):
                device_name = list(load_dict[i].keys())[0]
                if device_name == neighbour_name:
                    device_detail = load_dict[i][device_name][0]
                    listen_port = device_detail[list(device_detail.keys())[0]]
                    addr = device_detail[list(device_detail.keys())[2]]
                    self.setFib(device_name, addr, listen_port)

    def getName(self):
        return self.name

    def getCS(self):
        return self.cs

    # cache new data
    def setCS(self, name, data):
        self.cs[name] = data

    def getPit(self):
        return self.pit

    # record the incoming interface of Interest Packet
    def setPit(self, name, addr, interface):  # incoming interface
        self.pit.append((name, addr, interface))

    def getFib(self):
        return self.fib

    # for scalable ????
    def setFib(self, prefix, addr, interface):  # ongoing interface
        t = (prefix, addr, interface)
        self.fib.append(tuple(t))
