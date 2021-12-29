import sqlite3
from sqlite3 import Error
import requests 
import time
from datetime import date, datetime
import threading
from unidecode import unidecode

# Common gold type
goldType = {
        'Kim Thần Tài', 
        'AVPL / DOJI ĐN buôn', 
        'Lộc Phát Tài', 
        'DOJI HCM lẻ', 
        'Nữ trang 99.99', 
        'AVPL / DOJI HN lẻ', 
        'Nguyên liệu 99.99', 
        'Nữ trang 99', 
        'Hưng Thịnh Vượng', 
        'AVPL / DOJI CT lẻ', 
        'SJC', 
        'Nguyên liêu 9999 - HN', 
        'Vàng SJC 1L', 
        'AVPL / DOJI HCM buôn', 
        'AVPL / DOJI HN buôn', 
        'AVPL / DOJI HCM lẻ', 
        'Kim Ngân Tài', 
        'AVPL / DOJI CT buôn', 
        'DOJI Cần Thơ buôn', 
        'SJC*', 
        'Kim Ngưu', 
        'Nhẫn H.T.V', 
        'Nữ trang 10k', 
        'Nữ trang 18k', 
        'Kim Hợi', 
        'Nữ trang 99.9', 
        'Vàng SJC', 
        'DOJI ĐN buôn', 
        'Nguyên liệu 99.9', 
        'Vàng nhẫn SJC 99,99 1 chỉ, 2 chỉ, 5 chỉ', 
        'Vàng nữ trang 99%', 
        'DOJI ĐN lẻ', 
        'Nữ trang 14k', 
        'Nữ trang 68', 
        'Vàng nữ trang 99,99%', 
        'DOJI HN lẻ', 
        'DOJI HCM buôn', 
        'Nguyên liệu 9999', 
        'AVPL / DOJI ĐN lẻ', 
        'Vàng nữ trang 75%', 
        'DOJI Hải Phòng lẻ', 
        'Vàng nữ trang 58,3%', 
        'Nguyên liêu 999 - HN', 
        'DOJI Cần Thơ lẻ', 
        'Nữ Trang 14k', 
        'Vàng nữ trang 41,7%', 
        'Quy đổi (nghìn/lượng)', 
        'DOJI HN buôn', 
        'Nữ trang 16k', 
        'Vàng nhẫn SJC 99,99 0,5 chỉ', 
        'Nguyên liệu 999', 
        'USD/VND (Liên NH)', 
        'Kim Tuất', 
        'Nữ Trang 18k', 
        'DOJI Hải Phòng buôn'
    }

class Db():
    def __init__(self):
        # Init database
        self.conn = None
        try:
            self.conn = sqlite3.connect("./Database/user.db", check_same_thread = False)
            self.Create_Table()
        except Error as e:
            print("SQL Connection Error!")
        
        # Start multi-thread
        # Request the API from server
        rt = threading.Thread(target = self.refreshDB)
        rt.start()

    def Create_Table(self):
        # Init database
        sql_query_user = """ CREATE TABLE IF NOT EXISTS Users (
                                        user_id integer PRIMARY KEY,
                                        username text NOT NULL,
                                        password text NOT NULL
                                    ); """
        self.__Query(sql_query_user)

    def __Query(self, query):
        # Connecting database
        if self.conn is not None:
            try:
                c = self.conn.cursor()
                c.execute(query)
                self.conn.commit()
                return c.fetchall()
            except Error as e:
                print("Query SQL Error!")
                raise e;
    
    def updateJson(self, date):
        api = requests.get(f"https://tygia.com/json.php?gold=1&date={date}")
            
        # Fix BOM Header
        if api.text[0] == u'\ufeff':
            api.encoding = 'utf-8-sig'
            
        # Pass data from json to self.data
        self.data = api.json();

        # Filter unnecessary information
        tmp = []
        try:
            for value in self.data['golds'][0]['value']:
                tmp2 = {}
                if value['type'] in goldType:
                    tmp2.update({'type' : value['type']})
                    tmp2.update({'brand': value['brand']})
                    tmp2.update({'buy'  : "{:,.0f} VNĐ".format(float(value['buy'][:-3].replace(",", "")) * 1000)})
                    tmp2.update({'sell' : "{:,.0f} VNĐ".format(float(value['sell'][:-3].replace(",", "")) * 1000)})
                    tmp2.update({'update': value['updated']})
                    tmp2.update({'day'  : value['day']})
                    tmp.append(tmp2)
        except:
            tmp = []

        self.data = tmp

    def refreshDB(self, date = "NOW"):
        # Request API every 3600s
        while True:
            self.updateJson(date)
            # Sleep
            time.sleep(3600)

    def Login(self, username, password):
        # Query user from database
        cursor = self.conn.cursor()
        cursor.execute("SELECT user_id FROM Users WHERE username=:username AND password=:password", { 'username': username ,'password': password })
        result = cursor.fetchone()
       
        if result is None:
            # If not seen
            return {'valid_users': False}
        else:
            # If seen
            return {'user_id' : result[0] , 'valid_users': True}

    def Register(self, username, password):
        # Query user name from database
        cursor = self.conn.cursor()
        result = None
        cursor.execute("SELECT username FROM Users WHERE username=:username", {'username': username })
        result = cursor.fetchone()

        if result is not None:
            # If not match (haven't register)
            return {'avai' : False, 'success': True}
        try:
            # Insert new user into database
            cursor.execute("INSERT INTO Users (username, password) VALUES (:username,:password)", { 'username': username ,'password': password })
            self.conn.commit()
            return {'avai' : True, 'success': True}
        except Exception as msg:
            # Otherwise...
            return {'avai' : False, 'success': False}

    def GetType(self, search, getDate):
        Res = []

        todayDate = str(date.today()).replace("-", "")

        if todayDate < getDate:
            return Res

        # Make sure dont get empty data
        if self.data == []:
            self.updateJson(getDate)
            if self.data == []:
                return Res

        if getDate == "NOW" or self.data[0]["day"] == getDate:
            pass
        else:
            print(f"refresh database {getDate} {self.data[0]['update']}")
            self.updateJson(getDate)

        # Return matching type from API
        for value in self.data:
            tmp1 = unidecode(search.lower())
            tmp2 = unidecode(value['type'].lower())

            if tmp1 in tmp2:
                Res.append(value)

        return Res