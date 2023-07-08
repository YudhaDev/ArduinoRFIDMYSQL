import tkinter
from Sensor import Sensor
from db_management import DBManagement


class WindowUpdateKartu:
    __nilai_blokir = 0
    __options = ["Buka blokir", "Blokir"]
    __this_window: tkinter = None
    __clicked = None

    def __init__(self, main_window):
        self.__main_window = main_window

    def bacaSensor(self):
        serial_sensor = Sensor()
        serial_sensor.initSerialSensor()
        serial_sensor.readSensor()

    def updatekartu(self):
        db_object = DBManagement()
        db_object.connectDB()
        db_object.changeDB("database_sensor")
        db_object.updateKartu(self.__nilai_blokir)

    def __callback(self, *args):
        print("Masuk callback.")
        match str(self.__clicked.get()):
            case "Buka blokir":
                self.__nilai_blokir = 1
                # print("Nilai clicked: "+str(self.__clicked.get()))
                return
            case "Blokir":
                # print("Nilai clicked: "+str(self.__clicked.get()))
                self.__nilai_blokir = 0
                return

    def openBukaBlokirKartuWindow(self):
        self.__this_window = tkinter.Toplevel(self.__main_window)
        uid_kartu_label_frame_window2 = tkinter.LabelFrame(self.__this_window,
                                                           text="Masukan UID Kartu yang akan di proses")
        uid_kartu_label_frame_window2.grid(row=0, column=0)
        uid_kartu_label_frame_window2.pack()
        uid_kartu_label_window2 = tkinter.Label(uid_kartu_label_frame_window2, text="UID Kartu")
        uid_kartu_label_window2.grid(row=0, column=0)
        uid_kartu_entry_window2 = tkinter.Entry(uid_kartu_label_frame_window2)
        uid_kartu_entry_window2.grid(row=1, column=0)

        if self.__clicked is None:
            print("masuk 1")
            self.__clicked = tkinter.StringVar()
            self.__clicked.set(self.__options[0])
            self.__clicked.trace("w", self.__callback)

        else:
            print("masuk 2")
            self.__clicked.trace("w", self.__callback(self.__clicked.get()))

        dropdown_window2 = tkinter.OptionMenu(uid_kartu_label_window2, self.__clicked, *self.__options)
        dropdown_window2.grid(row=0, column=1)
        button_window2 = tkinter.Button(uid_kartu_label_frame_window2, text="Proses Kartu", command=self.updatekartu)
        button_window2.grid(row=2, column=0)
        self.__this_window.mainloop()
