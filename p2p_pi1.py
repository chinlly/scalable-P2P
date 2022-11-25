import Node
import socket
import _thread
from threading import Thread

interface = 33007
names = globals()
device_name = []  # save the name of device
device_type1 = 'diver'
addr = socket.gethostname()
other_addr = 'rasp-045'


# write into fib of all device when there appears a new device
def connect_node(device):
    # get all device expect the new device
    other_device = list(filter(lambda a: globals()[device_name[a]] != device, range(len(device_name))))
    # write the prefix into fib
    for s in other_device:
        device.router.setFib("/" + device.getType() + "/" + globals()[device_name[s]].getName(),
                             addr,
                             globals()[device_name[s]].getInterface())
        globals()[device_name[s]].router.setFib("/" + device.getType() + "/" + device.getName(),
                                                addr,
                                                device.getInterface())
    # map(lambda x: names[device_name[i]].router.setFib("/"+globals()[device_name[x]].getName(),
    #                                                   globals()[device_name[x]].getInterface()), other_device)
    # names[device_name[i]].router.setFib("/"+names[device_name[i]].getName(), names[device_name[i]].getInterface())


def p2p(device_type):
    for i in range(5):
        #
        names[device_type + str(i + 1)] = Node.Diver(device_type, device_type + str(i + 1), interface + i * 10,
                                                     1, 1, 1, 1, 1, 1, 1, 1, 1)
        # save the name of device
        device_name.append(device_type + str(i + 1))
        # add connection with other devices
        if i > 0:
            connect_node(names[device_type + str(i + 1)])
    #
    # for i in range(len(device_name)):
    # print("FIB of", device_name[i])
    # print(names[device_name[i]].router.getFib())  #


# print(globals())


def type_to_otherPi():
    name = ''
    for i in range(len(device_name)):
        devices = globals()[device_name[i]]
        # print(globals()[device_name[i]])
        if i < len(device_name) - 1:
            name += "/" + devices.getType() + "/" + devices.getName() + ":" + str(devices.getInterface()) + '~'
        else:
            name += "/" + devices.getType() + "/" + devices.getName() + ":" + str(devices.getInterface())
    # print(name)
    return name


def data_split(data):
    # print(type(data))
    content = data.split('~')
    # print(content)
    key = list(map(lambda x: x.split(':')[0], content))
    value = list(map(lambda x: x.split(':')[1], content))
    for i in range(len(device_name)):
        devices = globals()[device_name[i]]
        for j in range(len(key)):
            devices.router.setFib(key[j], value[j])


def serve():
    # next create a socket object
    s = socket.socket()
    print("Socket successfully created")

    # reserve a port on your computer in our
    # case it is 12345 but it can be anything
    port = 33777

    # Next bind to the port
    # we have not typed any ip in the ip field
    # instead we have inputted an empty string
    # this makes the server listen to requests
    # coming from other computers on the network
    s.bind((socket.gethostname(), port))
    print("socket binded to %s" % (port))

    s.listen(5)
    print("socket is listening")
    print(socket.gethostname())

    # a forever loop until we interrupt it or
    # an error occurs
    while True:
        c, addr = s.accept()
        print('Got connection from', addr)

        c.send('Thank you for connecting'.encode())

        data = c.recv(2048)
        # print(data.decode())
        data_split(data.decode())
        c.close()
        break

    s.close()


def client(data):
    s = socket.socket()
    hostname = socket.gethostbyname(socket.gethostname())
    print(hostname)

    # Define the port on which you want to connect
    port = 33777

    # connect to the server on local computer
    s.connect(socket.gethostname, port)

    # receive data from the server and decoding to get the string.
    print(s.recv(1024).decode())

    s.send(data.encode())

    # close the connection
    s.close()


# 兴趣包 name interface signature
class InterestPacket:
    def __init__(self, name, port):
        self.name = name
        self.port = port

    def getName(self):
        return self.name

    def getPort(self):
        return self.port


# 数据包 name data signature
class DataPacket:
    def __init__(self, name, recv_data, freshness):
        self.name = name
        self.recv_data = recv_data
        self.freshness = freshness

    def getName(self):
        return self.name

    def getData(self):
        return self.recv_data

    def getFreshness(self):
        return self.freshness


def select_mode():
    print("select: 1.request data 2. send data 3.exit")
    comm = input('>>> ')

    while True:
        if comm == '1':
            print("request data")
            print("input the request device")
            input_device = input(">>> ")
        elif comm == '2':
            print("send data")
        elif comm == '3':
            break
        else:
            print("please input the correct number!")
            print("select: 1.request data 2. send data 3.exit")
            comm = input('>>> ')


# for interest packet to send data
# 查找CS
def search_CS(device, packet):
    # device = globals()[device]
    info = device.router.getCS()
    if packet.name in info.key():
        return info.get(packet)
        # 写一个返回data的方法代替return并删除else中的return--------rewrite
    else:
        search_PIT(device, packet)
        # if data_cs is not None:
        #    device.router.setCS(packet, data_cs)
        # else:
        data_cs = "There is no such value!!"
        return data_cs


def search_PIT(device, packet):
    # print(device.getInterface())
    # print(packet.port)
    info = device.router.getPit()
    if packet.name in info.keys():
        print(info[packet.name])
        for i in range(len(info[packet.name])):
            print(info[packet.name][i])
            if packet.port == info[packet.name][i]:
                # print(packet.port)
                # print(info[packet.name][i])
                # print("0")
                break
            if i + 1 == len(info[packet.name]) & packet.port != info[packet.name][i]:
                device.router.setPit(packet.name, addr, packet.port)
                forwarder(device, packet)
                # print("1")
            else:
                device.router.setPit(packet.name, addr, packet.port)
                # print(device.router.getPit())
    else:
        device.router.setPit(packet.name, addr, packet.port)
        forwarder(device, packet)
        # print(device.router.getPit())


def longestCommonPrefix(strs: list) -> str:
    """
    :type strs: List[str]
    :rtype: str
    """
    res = ""  # 定义一个空字符串存结果
    if len(strs) == 0:
        return ""
    for tuples in zip(*strs):  # zip()函数将原列表解压
        if len(set(tuples)) == 1:  # 利用集合判断是不是每个元素都相同
            res += tuples[0]  # 相同的就连接在一起
        else:  # 否则直接返回
            return res


def fib_client(addr, port, packet):
    # Create a socket object
    s = socket.socket()
    hostname = socket.gethostbyname(socket.gethostname())

    # connect to the server on local computer
    s.connect((addr, port))

    # receive data from the server and decoding to get the string.
    s.send(packet).encode()
    # close the connection
    s.close()


# return the longest common prefix of Interest name and a name in fib table
def longestPrefix(str_packet, str_fib):
    re = ''
    # split the url with '/'
    packet_len = len(str_packet.split('/'))
    fib_len = len(str_fib.split('/'))
    # get the length of the shorter string
    loop_len = fib_len if packet_len > fib_len else packet_len
    prefix_len = 0
    # print(loop_len)
    for i in range(loop_len):
        if str_packet.split('/')[i] == str_fib.split('/')[i]:
            prefix_len += 1
        else:
            break
    # print(prefix_len)
    if loop_len == 1:
        return re
    else:
        for i in range(prefix_len):
            if i != 0:
                re += "/" + str_packet.split('/')[i]
        return re


# select_mode()
# set Routing Jump
# Note: 判定是否在同一个pi上 使用prefix第一个
def forwarder(device, packet):
    fib = ''
    prefix = dict()
    prefix_sorted = dict()
    if device.router.getFib():
        fib = device.router.getFib()
        # print(fib.keys())

        for i in fib.keys():
            str1 = longestPrefix(i, packet.name)
            if str1:
                prefix[str1] = packet.port

        if prefix:
            for i in sorted(prefix.keys()):
                prefix_sorted[i] = prefix[i]
                if packet.name == i:
                    # fib_client(addr, prefix[i], packet.name+'~'+str(packet.port))
                    break
                elif i.split('/')[1] == device_type1:
                    pass
                    # fib_client(addr, prefix[i], packet.name+'~'+str(packet.port))
                else:
                    pass
                    # fib_client(other_addr, prefix[i], packet.name + '~' + str(packet.port))
    else:
        print("Interest packet is thrown!")
        pass


p2p(device_type1)

# serve()

# print(globals()[device_name[0]].router.getFib())

data = type_to_otherPi()
# client(data)

# 为每个device instance设置一个socket & 线程
# _thread.start_new_thread()

# test PIT
globals()[device_name[0]].router.setPit('/diver/diver2/temperature', addr, globals()[device_name[1]].getInterface())
interest = InterestPacket('/diver/diver2/temperature', globals()[device_name[1]].getInterface() + 1)
search_PIT(globals()[device_name[0]], interest)
interest = InterestPacket('/diver/diver2/temper', globals()[device_name[1]].getInterface())
search_PIT(globals()[device_name[0]], interest)
interest = InterestPacket('/hhh', globals()[device_name[1]].getInterface())
search_PIT(globals()[device_name[0]], interest)
print(globals()[device_name[0]].router.getPit())

# test FIB




