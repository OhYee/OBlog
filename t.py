import json
import sqlite3


def query_db(sqlstr, one=False):
    conn = sqlite3.connect('sql.db')
    cur = conn.execute(sqlstr)
    t = cur.fetchall()
    print(t)
    rv = [dict((cur.description[idx][0], value.replace(r"$double-quote;", r'"') if value else "")
               for idx, value in enumerate(row)) for row in t]

    res = (rv[0] if rv else None) if one else rv
    print(res)
    return res

f = open('./friends.json', 'w')
f.write(json.dumps(query_db("select * from friends;")))
f.close()
