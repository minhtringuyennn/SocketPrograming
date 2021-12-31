# import Python Library
import sqlite3
import requests, threading, time
from sqlite3 import Error
from datetime import date, datetime
from unidecode import unidecode

# Common gold type
goldType = [
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
    ]

# Handle server database
class Db():
    def __init__(self):
        # Init server
        self.connectionUserDatabase = None
        self.userLoginList = []
        self.todayDate = str(date.today()).replace("-", "") # Get today date (Eg. 20213112)

        # Connect database
        try:
            self.connectionUserDatabase = sqlite3.connect("./Database/user.db", check_same_thread = False)
            self.createTable()
        except Error as e:
            print("SQL Connection Error!")
        
        # Start multi-thread
        # Request the API from server
        threadRefreshDB = threading.Thread(target = self.refreshDB)
        threadRefreshDB.start()

    # Init database
    def createTable(self):
        # Query to init database
        query = """ CREATE TABLE IF NOT EXISTS Users (
                                        user_id integer PRIMARY KEY,
                                        username text NOT NULL,
                                        password text NOT NULL
                                    ); """
        # Commit query
        self.QueryUserDatabase(query)

    # Commit query
    def QueryUserDatabase(self, query):
        if self.connectionUserDatabase is not None:
            try:
                c = self.connectionUserDatabase.cursor()
                c.execute(query)
                self.connectionUserDatabase.commit()
                return c.fetchall()
            except Error as err:
                print("Query SQL Error!")
                raise err;

    # Request JSON from the Internet
    def updateJson(self, date):
        api = requests.get(f"https://tygia.com/json.php?gold=1&date={date}")

        # Fix BOM Header
        if api.text[0] == u'\ufeff':
            api.encoding = 'utf-8-sig'

        # Pass data from json to self.data
        self.data = api.json();

        # Filter unnecessary information
        tmp = [] # Python list [dict1, dict2]
        try:
            # Get each value from gold list
            for value in self.data['golds'][0]['value']:
                tmp2 = {} # Python dictionary { ["property1"]: value1, ["property2"]: value2 }
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

        # Return all gold data
        self.data = tmp

    # Request API every 3600s
    def refreshDB(self, date = "NOW"):
        while True:
            print(f"Updated database at {datetime.now()}")
            self.updateJson(date)
            time.sleep(1800) # Sleep 1800s (30 mins)

    # Query for login
    def Login(self, username, password):
        # Query to get user record from database
        cursor = self.connectionUserDatabase.cursor()
        cursor.execute("SELECT user_id FROM Users WHERE username=:username AND password=:password", { 'username': username ,'password': password })
        result = cursor.fetchone()

        if result is None:
            # If havent seen in database
            return {'user_id' : -1 , 'valid_users': False}
        else:
            # If seen
            # Havent login
            if not result[0] in self.userLoginList:
                self.userLoginList.append(result[0])
                return {'user_id' : result[0] , 'valid_users': True}
            # Have login already
            else:
                return {'user_id' : result[0] , 'valid_users': False}

    # Query for register
    def Register(self, username, password):
        # Query user name from database
        cursor = self.connectionUserDatabase.cursor()
        cursor.execute("SELECT username FROM Users WHERE username=:username", {'username': username })
        result = cursor.fetchone()

        if result is not None:
            # If havent seen in database (haven't register)
            return {'avai' : False, 'success': True}
        try:
            # Insert new user into database
            cursor.execute("INSERT INTO Users (username, password) VALUES (:username,:password)", { 'username': username ,'password': password })
            self.connectionUserDatabase.commit()
            return {'avai' : True, 'success': True}
        except Exception as msg:
            # Can't add user to databse
            return {'avai' : False, 'success': False}

    # Logout user from database
    def Logout(self, userid):
        try:
            self.userLoginList.remove(userid)
            return {'success': True}
        except:
            return {'success': False}

    # Handle client request
    def GetType(self, search, getDate):
        # Init result
        # res == None
        Res = []

        # Return none if getDate > todayDate
        if getDate > self.todayDate:
            return Res

        # Make sure we dont get empty data
        # Case last query dont have data
        if self.data == []:
            # Try update again
            self.updateJson(getDate)
            
            # Still cannt get data
            if self.data == []:
                return Res

        # Only reupdate if needed
        if getDate == "NOW" or self.data[0]["day"] == getDate:
            pass
        else:
            self.updateJson(getDate)

        # Return matching type from API
        for value in self.data:
            tmp1 = unidecode(search.lower()) # Convert query to lowercase (EG: Kim Ngưu --> kim ngưu)
            tmp2 = unidecode(value['type'].lower()) # Convert Vietnamese string (EG: kim ngưu --> kim nguu)

            if tmp1 in tmp2:
                Res.append(value)

        # Return data
        return Res