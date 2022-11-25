import json
from collections import defaultdict


class Sensor:
    def __init__(self, name, interface, data, router, device_name, device_type, addr):
        self.name = name
        self.interface = interface
        self.data = data
        # 添加sensor接口到该设备路由表
        # add sensor interface into fib of current device
        router.setFib("/" + device_type + "/" + device_name + "/" + name, addr, interface)


# define Diver class
class Diver:
    def __init__(self, device_type, name, addr, interface, light, oxygen, position,
                 pressure, radar, heartrate, battery, alert, notifier):
        self.device_type = device_type
        self.name = name
        self.interface = interface
        self.router = Router(name)
        self.light = Sensor('light', interface + 1, light, self.router, self.name, self.device_type)
        self.oxygen = Sensor('oxygen', interface + 2, oxygen, self.router, self.name, self.device_type)
        self.position = Sensor('position', interface + 3, position, self.router, self.name, self.device_type)
        self.pressure = Sensor('pressure', interface + 4, pressure, self.router, self.name, self.device_type)
        self.radar = Sensor('radar', interface + 5, radar, self.router, self.name, self.device_type)
        self.heartrate = Sensor('heartrate', interface + 6, heartrate, self.router, self.name, self.device_type)
        self.battery = Sensor('battery', interface + 7, battery, self.router, self.name, self.device_type)
        self.alert = Sensor('alert', interface + 8, alert, self.router, self.name, self.device_type)
        self.notifier = Sensor('notifier', interface + 9, notifier, self.router, self.name, self.device_type)

    # test
    def info(self):
        print(f'sensor\'s name is {self.name}')
        print('sensor\'s information:')
        print(f'interface:{self.interface}')

    def getName(self):
        return self.name

    def getInterface(self):
        return self.interface

    # 当前device连接其他device
    def connect_sensor(self, prefix, interface):
        self.router.setPit(prefix, interface)

    def setRouter(self):
        return self.router

    def getType(self):
        return self.device_type


# NDN component
class Router:
    def __init__(self, name):
        self.name = name    # device name
        self.cs = dict()  # name: data
        self.pit = list(tuple())  # name, ip address, coming interface
        self.fib = tuple()  # prefix, ip address, ongoing interface

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
        self.fib.append((prefix, addr, interface))





