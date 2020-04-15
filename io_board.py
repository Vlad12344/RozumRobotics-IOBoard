import socket

from struct import pack, unpack

class IOBoard:
    """"""
    def __init__(
        self,
        ip: str = '127.0.0.1',
        port: int = 502,
        timeout: float = 0.1
    ):

        self.IP = ip
        self.PORT = port
        self.TIMOUT = timeout

        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__server_address = (self.IP, self.PORT)
        self.__sock.settimeout(self.TIMOUT)
        self.__resetIO()

        self.__bitesCounter = set()

        self.__digital_output_bites = {
            1: 1,
            2: 2,
            3: 4,
            4: 8,
            5: 16,
            6: 32,
            7: 64,
            8: 128
            }

        self.__digital_input_bites = {
            1: 1,
            2: 2,
            4: 3,
            8: 4,
            16: 5,
            32: 6,
            64: 7,
            128: 8,
            256: 9,
            512: 10,
            1024: 11,
            2048: 12,
            }

    def __resetIO(self):
        """Set all digital output in the LOW state"""
        message = pack('IIiHH', 1, 0, 25000, 0, 0)
        self.__sock.sendto(message, self.__server_address)

    def __check_state(self, numberPin: int):
        message = pack('IIiHH', 1, 0, 25000, numberPin, 0)
        self.__sock.sendto(message, self.__server_address)
        data, _ = self.__sock.recvfrom(4096)
        data = unpack('IIQHHHHfffffI', data)

        d_in = data[4]
        d_out = data[6]

        return d_in, d_out

    def __nearest(self, lst, target):
        return min(lst, key=lambda x: abs(x-target))

    def set_digital_output(self, numberPin: int, state: str) -> None:
        if numberPin not in self.__digital_output_bites.keys():
            raise AssertionError(f'Incorrect output pin number {numberPin}')

        if state == 'HIGH':
            numberPin = numberPin
            self.__bitesCounter.add(numberPin)
            value = sum([self.__digital_output_bites[bit] for bit in self.__bitesCounter])
            self.__check_state(value)
        elif state == 'LOW':
            numberPin = numberPin
            try:
                self.__bitesCounter.remove(numberPin)
            except KeyError:
                pass
            value = sum([self.__digital_output_bites[bit] for bit in self.__bitesCounter])
            self.__check_state(value)

    def get_digital_inputs(self) -> set:
        listOfInputs = set()
        bites = self.__digital_input_bites.keys()

        value = sum([self.__digital_output_bites[bit] for bit in self.__bitesCounter])
        d_in, _ = self.__check_state(value)

        while d_in != 0:
            nearest_input_bit = self.__nearest(bites, d_in)
            d_in = nearest_input_bit - d_in
            listOfInputs.add(self.__digital_input_bites[nearest_input_bit])

        return listOfInputs

    def get_digital_outputs(self) -> set:
        """"""
        return self.__bitesCounter

    def get_digital_input(self, numberInput: int) -> bool:
        if numberInput not in self.__digital_input_bites.values():
            raise AssertionError(f'Incorrect input pin number {numberInput}')

        listOfInputs = self.get_digital_inputs()

        if numberInput in listOfInputs:
            print('HIGH')
            return True
        else:
            print('LOW')
            return False