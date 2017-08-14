import sqlite3


def get_config():
    conn = sqlite3.connect("music.sqlite3")
    conn.execute("INSERT INTO config (key,value) VALUES ('lyric_x', '100');")
    conn.commit()
    cursor = conn.execute("SELECT key, value FROM config")
    for r in cursor:
        print(r)
    conn.close()


get_config()