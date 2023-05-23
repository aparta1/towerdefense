import sqlite3
# 1. Verbindung zur Datenbank erzeugen

connection = sqlite3.connect('ITA21a_Senso')

# 2. Datensatz-Cursor erzeugen

cursor = connection.cursor()

# 3. SQL erstellen (Datenbanktabelle erzeugen)

sql = """

CREATE TABLE if not exists level(

    level_id INTEGER PRIMARY KEY AUTOINCREMENT,

    sequence VARCHAR(255),

    duration_ms INT
)

"""

cursor.execute(sql)


sql = ("""INSERT INTO level(sequence) VALUES
      ("0,1"),
      ("1,0,2"),
      ("2,0,2,1"),
      ("0,2,1,2,1"),
      ("1,0,2,1,2,0"),
      ("0,2,0,1,2,1,2"),
      ("2,0,1,1,2,0,2,1"),
      ("1,2,0,2,2,1,2,0,2"),
      ("2,0,2,1,0,2,0,2,1,2"),
      ("2,0,2,1,0,1,2,0,1,1,2")""")
cursor.execute(sql)
cursor.execute("SELECT * FROM level")

sql = """

CREATE TABLE if not exists highscore(

    highscore_id INTEGER PRIMARY KEY AUTOINCREMENT,

    name VARCHAR(255),

    date DATETIME,

    level_id INT,

    FOREIGN KEY(level_id)

    REFERENCES level(level_id)

)"""
cursor.execute(sql)



cursor.execute(sql)
cursor.execute("SELECT name FROM highscore")
connection.commit()
connection.close()