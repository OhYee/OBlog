import sqlite3

def query_db(conn, sqlstr, one=False):
    cur = conn.execute(sqlstr)
    t = cur.fetchall()
    rv = [dict((cur.description[idx][0], value.replace(r"$double-quote;", r'"')
                if type(value)==str else "")
                for idx, value in enumerate(row)) for row in t]

    res = (rv[0] if rv else None) if one else rv
    return res

def raw_query_db(conn,sqlstr, one=False):
    cur = conn.execute(sqlstr)
    res = cur.fetchall()
    res = (res[0] if res else None) if one else res
    return res


conn = sqlite3.connect('../database.db')

res = raw_query_db(conn,'select chinese from tags;')
res = [item[0] for item in res]

for item in res:
    res1=raw_query_db(conn,"select count(url) from posts where tags like '{0},%%' or tags like '%%,{0},%%' or tags like '%%,{0}';".format(item),one=True)
    res2=raw_query_db(conn,"select cnt from tags where chinese='"+item+"';",one=True)
    if str(res1[0])!=str(res2[0]):
        print(item,res1[0],res2[0])

 
