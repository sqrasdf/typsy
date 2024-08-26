# words = []
# with open("english_words_3000.txt") as file:
#     for line in file.readlines():
#         words.append(line.strip())

import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()

res = cur.execute("SELECT date, wpm, accuracy FROM user_data WHERE user_id = ?;", (7, )).fetchall()
print(res)
print(type(res))

# res = cur.execute("SELECT ROUND(wpm, 0), accuracy FROM user_data WHERE user_id = ?;", (7, )).fetchall()
# for row in res:
#     print(row)

# username = cur.execute("SELECT username FROM users WHERE id = ?;", (7, )).fetchone()[0]
# print(username)

# max_wpm, avg_accuracy = cur.execute("SELECT MAX(wpm), AVG(accuracy) FROM user_data WHERE user_id = ?;", (7, )).fetchall()[0]
# print(max_wpm)
# print(avg_accuracy)

# res = cur.execute("SELECT * FROM user_data;").fetchall()
# for item in res:
#     print(" ".join([str(i) for i in item]))


# cur.execute("CREATE TABLE user_data (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, wpm FLOAT, accuracy FLOAT, date DATETIME);")

# cur.execute("DELETE FROM users;")
# con.commit()

# user_id, hash = cur.execute("SELECT id, password_hash FROM users WHERE username = ?;", ("sqr", )).fetchone()
# print(user_id)
# print(hash)
# print(type(user_id))

# res = cur.execute("SELECT * FROM users;").fetchall()
# print(res)

# cur.execute("INSERT INTO users VALUES (NULL, 'sqr3', 'a@gmail.com', 'a', 'a_hash');")
# con.commit()

# cur.execute("DROP TABLE users;")
# cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT UNIQUE NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL, password_hash TEXT NOT NULL);")

# res = cur.execute("SELECT word FROM words WHERE id = 10").fetchone()[0]
# res2 = cur.execute("SELECT word FROM words WHERE id < 10").fetchall()[0][0]
# print(res)
# print(res2)


