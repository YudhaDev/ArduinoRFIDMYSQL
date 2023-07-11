import serial.tools.list_ports
import tkinter
import tkinter.messagebox
import threading
import time
import mysql
import mysql.connector
from mysql.connector import MySQLConnection
from enum import Enum

from windowupdatekartu import WindowUpdateKartu
from db_management import DBManagement

# Inisialiasi UI
window = tkinter.Tk()
window.title("Program Scan Kartu")
frame1 = tkinter.Frame(window)
frame1.pack()
frame2 = tkinter.Frame(window)
frame2.pack()


###########################################FungsiUI#########################################
def registerRfidBaru():
    try:
        db_object = DBManagement()
        db_object.connectDB()
        db_object.changeDB("database_sensor")
        pesan = db_object.regisSensor(str(input_kartu_entry2.get()), str(input_nama_entry.get()))
        tkinter.messagebox.showinfo("Informasi", pesan)
    except mysql.connector.Error as err:
        tkinter.messagebox.showerror("Error", str(err))


###########################################
# card_info_frame = tkinter.LabelFrame(frame1, text="Informasi kartu")
# card_info_frame.grid(row=0, column=0)
# card_info_frame.rowconfigure(0, weight=1)
# uid_kartu_label = tkinter.Label(card_info_frame, text="UID kartu")
# uid_kartu_label.grid(row=0, column=0)
# uid_kartu_label.rowconfigure(0, weight=1)
# input_kartu_entry = tkinter.Entry(card_info_frame)
# input_kartu_entry.grid(row=1, column=0)

def callback(*args):
    match clicked.get():
        case "Scan":
            object_sensor.reset()
            disableRegisterFrame()
        case "Register":
            object_sensor.reset()
            enableRegisterFrame()
        case "Login":
            object_sensor.reset()
            disableRegisterFrame()

    tkinter.messagebox.showinfo("Perhatian", "Mode berganti ke: " + clicked.get())


options = ["Scan", "Register", "Login"]
clicked = tkinter.StringVar()
clicked.set(options[0])
clicked.trace("w", callback)

mode_dropdown_frame = tkinter.LabelFrame(frame1, text="Pilih Mode Aplikasi:")
mode_dropdown_frame.grid(row=0, column=0)
mode_dropdown = tkinter.OptionMenu(mode_dropdown_frame, clicked, *options)
mode_dropdown.grid(row=0, column=0)

card_register_frame = tkinter.LabelFrame(frame1, text="Register kartu Baru")
card_register_frame.grid(row=0, column=1)
uid_kartu_label2 = tkinter.Label(card_register_frame, text="UID kartu")
uid_kartu_label2.grid(row=0, column=0)
input_kartu_entry2 = tkinter.Entry(card_register_frame)
input_kartu_entry2.grid(row=1, column=0)
uid_kartu_label2 = tkinter.Label(card_register_frame, text="Nama Pemilik Kartu")
uid_kartu_label2.grid(row=2, column=0)
input_nama_entry = tkinter.Entry(card_register_frame)
input_nama_entry.grid(row=3, column=0)
simpan_uid_button = tkinter.Button(card_register_frame, text="Simpan", command=registerRfidBaru)
simpan_uid_button.grid(row=1, column=1)

update_kartu_button_frame = tkinter.LabelFrame(frame1, text="Buka/Blokir Kartu")
update_kartu_button_frame.grid(row=0, column=2)


def enableRegisterFrame():
    for child in card_register_frame.winfo_children():
        child.configure(state=tkinter.NORMAL)


def disableRegisterFrame():
    for child in card_register_frame.winfo_children():
        child.configure(state=tkinter.DISABLED)


################State Awal###################
disableRegisterFrame()
#############################################
sensor_info_frame = tkinter.LabelFrame(frame2, text="Stream Data Sensor")
sensor_info_frame.grid(row=1, column=0)
sensor_stream_text = tkinter.Text(sensor_info_frame)
sensor_stream_text.grid(row=0, column=0)
sensor_stream_text.insert("end-1c", "menunggu data sensor... \n")
sensor_stream_text.insert("end-1c", "menunggu data sensor...")


##########################################SERIAL##############################################
class Sensor:
    __string_uid = ""
    __string_uid_temp = "null"
    __bool_update_string_uid = False
    __status_sensor = "Mati"
    __check_kartu = 0  # check kartu di login

    ports = serial.tools.list_ports.comports()
    serialinst = serial.Serial()


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

    serialinst.baudrate = 9600
    serialinst.port = port_pilihan

    try:
        serialinst.open()
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
    def getStatusSensor(self):
        return self.__status_sensor

    def setStatusSensor(self, value_sensor):
        self.__status_sensor = value_sensor

    def reset(self):
        self.__string_uid = ""
        self.__string_uid_temp = ""
        self.__bool_update_string_uid = False

        print("nilai uid sekarang: "+self.__string_uid_temp)

    def closeSerialSensor(self):
        self.serialinst.close()

    def readSensor(self):
        if self.__status_sensor == "Hidup":
            self.__status_sensor = "Mati"
            while True:
                # get sensor terus
                # self.__string_uid_temp = str(self.serialinst.readline().decode('utf').rstrip('\n'))

                if self.serialinst.in_waiting:
                    self.__string_uid_temp = self.serialinst.readline().decode('utf').rstrip('\n')

                print("Nilai uid temp: "+str(self.__string_uid_temp))

                # Jika mode Scan
                if clicked.get() == str(options[0]):
                    print("Masuk Scan.")
                # Jika mode Register
                if clicked.get() == str(options[1]):
                    if not self.__string_uid_temp == "null":
                        print("lah kok masuk")
                        input_kartu_entry2.insert(0, self.__string_uid_temp)
                        # print("Masuk Register.")
                        return

                # Jika mode Login
                if clicked.get() == str(options[2]):
                    print("Masuk login.")
                    if not self.__string_uid_temp == "null":
                        # print("masuk pak eko.")
                        # print("UID_TEMP " + self.__string_uid_temp)
                        db_object = DBManagement()
                        db_object.connectDB()
                        db_object.changeDB("database_sensor")
                        text = db_object.scanKartu(str(self.__string_uid_temp))
                        if text == "Kartu belum teregister":
                            self.__check_kartu += 1
                            if self.__check_kartu == 3:
                                tkinter.messagebox.showinfo("Perhatian", "kartu terblokir")
                            else:
                                tkinter.messagebox.showinfo("Perhatian", text)
                        else:
                            tkinter.messagebox.showinfo("Perhatian", str(text))
                        self.__string_uid_temp = ""
                        db_object.closeDB()
                        self.__status_sensor = "Mati"
                        return
                time.sleep(0.25)

        else:
            print("Sensor sudah berjalan.")


#######################################Inisialisasi DB#################################
object_database = DBManagement()
object_database.connectDB()
object_database.createDatabase()
object_database.createTable("rfid_table")
object_database.getAllRFID()
object_database.closeDB()

# Object Sensor
object_sensor = Sensor()


# object_sensor.readSensor()
# threading_sensor = threading.Thread(target=object_sensor.readSensor)
# threading_sensor.start()

# fungsi buka window baru
def openWindowBukaBlokir():
    window_baru = WindowUpdateKartu(window)
    object_sensor.closeSerialSensor()
    window_baru.openBukaBlokirKartuWindow()
    window_baru.bacaSensor()


def startStopSensor():
    object_sensor.setStatusSensor("Hidup")
    object_sensor.readSensor()


update_kartu_button = tkinter.Button(update_kartu_button_frame, text="Buka/Blokir Kartu", command=openWindowBukaBlokir)
update_kartu_button.grid(row=0, column=0)

sensor_start_button_label_frame = tkinter.LabelFrame(frame1, text="Tombol Scan Sensor")
sensor_start_button_label_frame.grid(row=1, column=0)
sensor_start_button = tkinter.Button(sensor_start_button_label_frame, text="Start Sensor", command=startStopSensor)
sensor_start_button.grid(row=0, column=0)

sensor_status_label_frame = tkinter.LabelFrame(frame1, text="Status Sensor Sekarang:")
sensor_status_label_frame.grid(row=1, column=1)

sensor_status_text = tkinter.Label(sensor_status_label_frame, text="Mati")
sensor_status_text.grid(row=0, column=0)


# Set UI
def updateUI():
    while True:
        # if object_sensor.getBoolUpdateStringUid():
        #     print("masuk")
        # input_kartu_entry.delete(0, "end")
        # input_kartu_entry.insert(0, str(object_sensor.getStringUid()))
        # input_kartu_entry2.insert(0, str(object_sensor.getStringUidTemp())
        # object_sensor.setBoolUpdateStringUid(False)
        # sensor_stream_text.insert("1.0", object_sensor.serialinst.readline().decode('utf'))

        input_kartu_entry2.delete(0, "end")
        input_kartu_entry2.insert(0, object_sensor.getStringUidTemp())
        sensor_stream_text.insert("1.0", object_sensor.getStringUidTemp())

        # # check semua thread
        # for thread in threading.enumerate():
        #     print(thread.name)

        time.sleep(1)


# threading_ui = threading.Thread(target=updateUI)
# threading_ui.start()

window.mainloop()
