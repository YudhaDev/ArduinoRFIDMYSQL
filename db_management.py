from mysql.connector import MySQLConnection
import mysql


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
        mycursor = self.__mysql_connection.cursor()
        # query = '''SELECT rfid_number FROM rfid_table WHERE rfid_number LIKE''' + "'%" + rfid_number + "%'"
        query = '''SELECT * FROM rfid_table WHERE rfid_number LIKE''' + "'%" + rfid_number + "%'"

        try:
            mycursor.execute(query)
            try:
                print("Dari DB:" + str(mycursor.fetchall()[0][1]))
                return "Selamat Datang."
            except:
                return "Kartu belum teregister"
        except mysql.connector.Error as err:
            print(err)

        # if not mycursor.fetchall().count(10) == 0:
        #     return "Selamat Datang"
        # else:
        #     return "Kartu belum teregister."

    def updateKartu(self, nilai_blokir):
        try:
            rfid_number = "90 EF 81 20"
            mycursor = self.__mysql_connection.cursor()
            # query = '''SELECT * FROM rfid_table WHERE rfid_number LIKE''' + "'%" + rfid_number + "%'"
            query_update = '''UPDATE `rfid_table` SET `status` = ''' + str(nilai_blokir) + ''' WHERE `rfid_number` LIKE''' + "'%" + rfid_number + "%'"
            mycursor.execute(query_update)
            self.__mysql_connection.commit()
            print("Berhasil update kartu.")
        except mysql.connector.Error as err:
            print(str(err))

    def getAllRFID(self):
        mycursor = self.__mysql_connection.cursor(buffered=True)
        query_get_all = "SELECT rfid_number FROM rfid_table"
        mycursor.execute(query_get_all)
        print(str(mycursor.fetchall()))
