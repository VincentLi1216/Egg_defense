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
        #update the sql data
        import pymysql
        player_db = pymysql.connect(**db_settings)
        cursor = player_db.cursor()

        sql = "INSERT INTO new_table (account, timestamp, pw, coin, characters, level) VALUES (%s, %s, %s, %s, %s, %s)"
        lst = (data["account"], data["timestamp"], data["pw"], data["coin"], data["characters"], data["level"])
        cursor.execute(sql, lst)

        player_db.commit()

    data["characters"] = data["characters"].split(",")

    with open("local_data.json", "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=False)

def get_data(name):
    if(connection_test()):
        # get from the sql data
        import pymysql
        player_db = pymysql.connect(**db_settings)
        cursor = player_db.cursor()
        cursor.execute(f"SELECT * FROM new_table WHERE account='{name}'")

        column_names = [i[0] for i in cursor.description]
        table_content = cursor.fetchall()

        date = max(table_content, key=lambda x: x[1])
        player_dict = dict(zip(column_names, list(date)))
        player_dict["characters"] = player_dict["characters"].split(",")

        return player_dict

    else:
        with open('local_data.json') as f:
            return json.load(f)


from datetime import datetime
#
data = {"account": "test_5", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "pw": "qwerty",
        "coin": 50, "characters": "cat,bee,rino,fox,turtle,turkey", "level": 2}
#
if __name__ == "__main__":
    print(connection_test())
    update_data(data)
    print(get_data("test"))

