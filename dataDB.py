import json, pymysql

player_data = {"name": "Vincent", "account":"sunnus.tw@gmail.com", "pw":"aaabbc123", "coin":300, "characters":["bee", "bird", "cat", "dog"], "level":2}

with open("local_data.json", "w", encoding='utf-8') as f:
  # json.dump(dict_, f) # 写为一行
  json.dump(player_data, f, indent=2, sort_keys=True, ensure_ascii=False) # 写为多行

# 資料庫設定
db_settings = {
    "host": "server.gems.com.tw",
    "port": 3306,
    "user": "vincent",
    "password": "qwerty1324",
    "db": "Egg_Defense",
    "charset": "utf8"
}
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)
    # 建立Cursor物件
    with conn.cursor() as cursor:
        pass
      #資料表相關操作
except Exception as ex:
    print(ex)
