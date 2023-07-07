import serial.tools.list_ports
import tkinter
import tkinter.messagebox
import threading
import time
import mysql
import mysql.connector
from mysql.connector import MySQLConnection
from enum import Enum

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

def startReadSensor():
    object_sensor.readSensor()

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

    tkinter.messagebox.showinfo("Perhatian", "Mode berganti ke: "+clicked.get())

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

sensor_start_button_frame = tkinter.LabelFrame(frame1, text="Start Sensor")
sensor_start_button_frame.grid(row=0, column=2)
sensor_start_button = tkinter.Button(sensor_start_button_frame, text="Start Sensor", command=startReadSensor)
sensor_start_button.grid(row=0, column=0)



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

################################Database#####################################
class DBManagement:
    __host = "localhost"
    __port = 3307
    __username = "root"
    __password = "root"
    __database = "database_sensor"
    __mysql_connection: MySQLConnection = None

    def connectDB(self):
        if self.__mysql_connection is None:
            try:
                self.__mysql_connection = mysql.connector.connect(host=self.__host, username=self.__username,
                                                                  password=self.__password)
                print("Sukses koneksi mysql.")
            except mysql.connector.Error as err:
                print("Error koneksi mysql => " + str(err))
        else:
            print("Mysql sudah terkoneksi")

    def createDatabase(self):
        if self.__mysql_connection is None:
            print("Koneksi ke mysql belum tersambung.")
        else:
            mycursor = self.__mysql_connection.cursor(buffered=True)
            query2 = "SHOW DATABASES LIKE '%" + self.__database + "%'"
            mycursor.execute(query2)
            if mycursor.fetchall() == "[]":
                try:
                    query_create_db = "CREATE DATABASE " + self.__database
                    mycursor.execute(query_create_db)
                    print("Database baru telah dibuat.")
                except mysql.connector.Error as err:
                    print("Error membuat database. : " + str(err))
            else:
                print("database telah ada.")
        self.changeDB(self.__database)

    def changeDB(self, db_name):
        self.__mysql_connection.database = db_name

    def createTable(self, table_name):
        # query = "SHOW TABLES LIKE '%"+table_name+"%'"
        # self.__mysql_connection.cursor().execute(query)

        TABLES = {}
        TABLES[table_name] = (
                "CREATE TABLE `" + table_name + "`("
                                                "`id` int(11) NOT NULL AUTO_INCREMENT,"
                                                "`rfid_number` text,"
                                                "`name` varchar(20),"
                                                "`status` int(1) DEFAULT 1,"
                                                "`date_created` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                                                "PRIMARY KEY (`id`))"
        )

        # self.changeDB(self.__database)
        mycursor = self.__mysql_connection.cursor(buffered=True)
        if not self.__mysql_connection is None:
            query_check_tabel = "SHOW TABLES like '%" + table_name + "%'"
            mycursor.execute(query_check_tabel)
            try:
                # print(str(TABLES[table_name]))
                mycursor.execute(TABLES[table_name])
                print("Tabel baru telah dibuat.")
            except mysql.connector.Error as err:
                print("error: " + str(err))

    def closeDB(self):
        if not self.__mysql_connection == 0:
            self.__mysql_connection.close()

    def regisSensor(self, rfid_number, name):
        __table_name = "rfid_table"
        query_insert = '''INSERT INTO ''' + __table_name + ''' (rfid_number, name) VALUES (%s, %s)'''

        query_insert_percobaan = '''INSERT INTO rfid_table (rfid_number, name) VALUES ("2131312", "yudha")'''

        value = (str(rfid_number), str(name))

        query_check_rfid_duplicate = '''SELECT rfid_number FROM rfid_table WHERE rfid_number =''' + "'" + rfid_number + "'"
        cursor = self.__mysql_connection.cursor(buffered=True)
        cursor.execute(query_check_rfid_duplicate)

        if cursor.fetchall():
            return "Duplikasi Kartu, kartu sebelumnya sudah terdaftar."
        else:
            try:
                mycursor = self.__mysql_connection.cursor()
                mycursor.execute(query_insert, value)
                self.__mysql_connection.commit()
            except mysql.connector.Error as err:
                print(str(err))
            return "Kartu berhasil disimpan."

    def scanKartu(self, rfid_number):
        mycursor = self.__mysql_connection.cursor(buffered=True)
        # query = '''SELECT rfid_number FROM rfid_table WHERE rfid_number LIKE''' + "'%" + rfid_number + "%'"
        query = '''SELECT * FROM rfid_table WHERE rfid_number LIKE''' + "'%" + rfid_number + "%'"
        mycursor.execute(query)
        try:
            # print("Dari DB:"+str(mycursor.fetchall()[0][1]))
            return "Selamat Datang."
        except:
            return "Kartu belum teregister"

        # if not mycursor.fetchall().count(10) == 0:
        #     return "Selamat Datang"
        # else:
        #     return "Kartu belum teregister."

    def updateSensor(self):
        return

    def getAllRFID(self):
        mycursor = self.__mysql_connection.cursor(buffered=True)
        query_get_all = "SELECT rfid_number FROM rfid_table"
        mycursor.execute(query_get_all)
        print(str(mycursor.fetchall()))


##########################################SERIAL##############################################
class Sensor:
    __string_uid = ""
    __string_uid_temp = ""
    __bool_update_string_uid = False
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

    def reset(self):
        self.__string_uid = ""
        self.__string_uid_temp = ""
        self.__bool_update_string_uid = False


    def readSensor(self):
        check = 0
        while True:
            # print("heyyy" +str(self.__bool_update_string_uid))
            # print("Dari sensor (Temp): "+self.__string_uid_temp)
            # print("Dari sensor : "+self.__string_uid)

            #get sensor terus
            # self.__string_uid_temp = self.serialinst.readline().decode('utf').rstrip('\n')

            if self.serialinst.in_waiting:
                self.__string_uid_temp = self.serialinst.readline().decode('utf').rstrip('\n')

            #Jika mode Scan
            if clicked.get() == str(options[0]):
                print("Masuk Scan.")
            #Jika mode Register
            if clicked.get() == str(options[1]):
                print("Masuk Register.")
            #Jika mode Login
            if clicked.get() == str(options[2]):
                if not self.__string_uid_temp == "":
                    print("masuk pak eko.")
                    print("UID_TEMP "+self.__string_uid_temp)
                    db_object = DBManagement()
                    db_object.connectDB()
                    db_object.changeDB("database_sensor")
                    text = db_object.scanKartu(str(self.__string_uid_temp))
                    # tkinter.messagebox.showinfo("Perhatian", str(text))
                    print(text)
                    time.sleep(2)
                    self.__string_uid_temp = ""
                    db_object.closeDB()


                    # if self.__bool_update_string_uid:
                        # print("Dari sensor: "+str(self.__string_uid_temp))
                        # tkinter.messagebox.showinfo("Perhatian", str(object_database.scanKartu(str(self.__string_uid))))
                        # print("Yudha :" + object_database.scanKartu(self.__string_uid_temp))

                        # # pengecekan duplikasi scan kartu
                        # print("nilai string uid: " + str(self.__string_uid))
                        # print("nilai paket: " + str(packet))
                        # if packet == self.__string_uid:
                        #     check += 1
                        # else:
                        #     check = 1
                        #
                        # if check == 3:
                        #     print("Kartu terblokir!")
                        #
                        # self.__string_uid = packet
                        # self.__bool_update_string_uid = True
                        # print("nilai check:" + str(check))

            print("UID_TEMP SEHABIS "+self.__string_uid_temp)
            # if not self.__string_uid == self.__string_uid_temp:
            #     self.__bool_update_string_uid = True
            # else:
            #     self.__bool_update_string_uid = False

            self.__string_uid = self.__string_uid_temp
            # print(self.__bool_update_string_uid)

#######################################Inisialisasi DB#################################
object_database = DBManagement()
object_database.connectDB()
object_database.createDatabase()
object_database.createTable("rfid_table")
object_database.getAllRFID()
object_database.closeDB()

# Object Sensor
object_sensor = Sensor()
threading_sensor = threading.Thread(target=object_sensor.readSensor)
threading_sensor.start()

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
        time.sleep(0.25)


threading_ui = threading.Thread(target=updateUI)
threading_ui.start()

window.mainloop()
