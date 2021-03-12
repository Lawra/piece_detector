import snap7
from snap7.util import *
from snap7.types import *


class Comunication:
    def __init__(self, ip, rack, slot):
        self.ip = ip
        self.rack = rack
        self.slot = slot

        # *************  configuracio comunicació
        self.plc = snap7.client.Client()
        self.plc.connect(ip, rack, slot)

        # *************  Informació de l'estat del PLC
        self.plc_info = self.plc.get_cpu_info()
        self.StatCPU = self.plc.get_cpu_state()

        print(f'PLC : {self.plc_info.ModuleTypeName}')
        print(f'CPU : {self.StatCPU}')

    def reading_bool(self, Ndb, PosM, bit):
        result = self.plc.read_area(areas['DB'], Ndb, PosM, S7WLBit)
        return get_bool(result, 0, bit)

    def writing_bool(self, Ndb, PosM, bit, variable):
        result = self.plc.read_area(areas['DB'], Ndb, PosM, S7WLBit)
        set_bool(result, 0, bit, variable)
        self.plc.write_area(areas["DB"], Ndb, PosM, result)

    def writing_real(self, Ndb, PosM, variable):
        result = self.plc.read_area(
            areas['DB'], Ndb, PosM, S7WLReal)     # S7WLReal 4 Bytes
        set_real(result, 0, variable)
        self.plc.write_area(areas["DB"], Ndb, PosM, result)

    def writing_byte(self, Ndb, PosM, variable):
        result = self.plc.read_area(
            areas['DB'], Ndb, PosM, S7WLByte)     # S7WLByte 2 Bytes
        set_int(result, 0, variable)
        self.plc.write_area(areas["DB"], Ndb, PosM, result)
