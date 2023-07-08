import serial
import serial.tools.list_ports
class Sensor:
    __string_uid = ""
    __string_uid_temp = ""
    __serialinst: serial = None

    def initSerialSensor(self):
        ports = serial.tools.list_ports.comports()
        self.__serialinst = serial.Serial()
        portList = []
        print("Port yang sedang terhubung: ")
        for port in ports:
            portList.append(str(port))
            print(str(portList))

        inputan_user = input("Pilih Port yang ingin disambungkan: COM")

        for i in range(0, len(portList)):
            if portList[i].startswith("COM" + str(inputan_user)):
                port_pilihan = "COM" + inputan_user
                print(port_pilihan)

        self.__serialinst.baudrate = 9600
        self.__serialinst.port = port_pilihan

        try:
            self.__serialinst.open()
        except:
            print("error")


    def getStringUid(self):
        return self.__string_uid

    def getStringUidTemp(self):
        return self.__string_uid_temp

    def getBoolUpdateStringUid(self):
        return self.__bool_update_string_uid

    def setBoolUpdateStringUid(self, boolean):
        self.__bool_update_string_uid = boolean

    def getSerialinst(self):
        return self.__serialinst
    def closeSerialSensor(self):
        self.__serialinst.close()

    def readSensor(self):
        while True:
            print("sadaw")
            if self.serialinst.in_waiting:
                self.__string_uid_temp = self.__serialinst.readline().decode('utf').rstrip('\n')


