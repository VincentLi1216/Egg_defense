from datetime import datetime
import json
table_name = 'users'

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


def insert_data(data):
    if (connection_test()):
        # update the sql data
        import pymysql
        player_db = pymysql.connect(**db_settings)
        cursor = player_db.cursor()
        try:
            sql = f"INSERT INTO {table_name} (account, timestamp, pw, coin, characters, level) VALUES (%s, %s, %s, %s, %s, %s)"
            lst = (data["account"], data["timestamp"], data["pw"],
                   data["coin"], data["characters"], data["level"])
            cursor.execute(sql, lst)

            player_db.commit()
            data["characters"] = data["characters"].split(",")

            with open("local_data.json", "w", encoding='utf-8') as f:  # update the json file
                json.dump(data, f, indent=2, sort_keys=True,
                          ensure_ascii=False)

            return True  # successed
        except:
            return False  # failed


def update_data(data):
    if (connection_test()):
        # update the sql data
        import pymysql
        player_db = pymysql.connect(**db_settings)
        cursor = player_db.cursor()
        try:
            sql = f'UPDATE {table_name} SET timestamp = NOW(), pw = \'{data["pw"]}\', coin = {data["coin"]}, characters = \'{data["characters"]}\', level = {data["level"]} WHERE account = \'{data["account"]}\''
            cursor.execute(sql)
            player_db.commit()
            data["characters"] = data["characters"].split(",")

            with open("local_data.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=2, sort_keys=True,
                          ensure_ascii=False)

            return True
        except:
            return False


def get_data(name):
    try:
        if (connection_test()):
            # get from the sql data
            import pymysql
            player_db = pymysql.connect(**db_settings)

            cursor = player_db.cursor()
            cursor.execute(
                f"SELECT * FROM {table_name} WHERE account='{name}'")
            # print(column_names)
            column_names = [i[0] for i in cursor.description]
            table_content = cursor.fetchall()

            date = max(table_content, key=lambda x: x[1])

            player_dict = dict(zip(column_names, list(date)))
            player_dict["characters"] = player_dict["characters"].split(",")

            return player_dict

        else:
            with open('local_data.json') as f:
                return json.load(f)
    except:
        return False


def delete_data(account):
    if (connection_test()):
        # update the sql data
        import pymysql
        player_db = pymysql.connect(**db_settings)
        cursor = player_db.cursor()
        try:
            sql = f'DELETE FROM {table_name} WHERE account = \'{account}\''
            cursor.execute(sql)
            player_db.commit()

            return True
        except:
            return False


#
data = {"account": "testlevel1", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "pw": "qwerty",
        "coin": 50, "characters": "cat,bee,mushroom,bird", "level": 1}
#
if __name__ == "__main__":
    print(connection_test())
    print(update_data(data))
    # print(delete_data("test_level1"))
    print(get_data("testlevel1"))