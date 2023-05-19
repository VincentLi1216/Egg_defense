import json

# player_data = {"account": "Vincent", "pw":"aaabbc123", "coin":300, "characters":["bee", "bird", "cat", "dog"], "level":2}
# 資料庫設定
db_settings = {
    "host": "server.gems.com.tw",
    "port": 3306,
    "user": "vincent",
    "password": "qwerty1324",
    "db": "Egg_Defense",
    "charset": "utf8"
}

def connection_test():
    try:
        import pymysql

        try:
            # 建立Connection物件
            conn = pymysql.connect(**db_settings)
            # 建立Cursor物件
            with conn.cursor() as cursor:
                return True
            # 資料表相關操作
        except Exception as ex:
            return False

    except:
        return False


def update_data(data):
    if(connection_test()):
        pass #update the sql data
    else:
        with open("local_data.json", "w", encoding='utf-8') as f:
          json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=False)


def get_data():
    if(connection_test()):
        pass #get from the sql data
    else:
        with open('local_data.json') as f:
            return json.load(f)



if __name__ == "__main__":
    print(connection_test())
    print(get_data())

