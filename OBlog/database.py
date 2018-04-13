from flask import g,current_app


def where2str(_where):
    wherestr = ''
    for k in _where:
        wherestr += str(k) + '="' + \
            str(_where[k]).replace(r'"', r"$double-quote;") + '" and '
    wherestr = wherestr[0:-4]
    return wherestr


def insert2str(_insert):
    _str1 = ''
    _str2 = ''
    for k in _insert:
        _str1 += str(k) + ','
        _str2 += '"' + str(_insert[k]).replace(r'"', r"$double-quote;") + '",'
    return (_str1[0:-1], _str2[0:-1])


def set2str(_set):
    setstr = ''
    for k in _set:
        setstr += str(k) + '="' + \
            str(_set[k]).replace(r'"', r"$double-quote;") + '",'
    setstr = setstr[0:-1]
    return setstr


def raw_query_db(sqlstr, one=False):
    current_app.logger.debug('raw_query_db %s'% sqlstr)
    cur = g.db.execute(sqlstr)
    res = cur.fetchall()
    # print(res)
    res = (res[0] if res else None) if one else res
    return res


def query_db(sqlstr, one=False):
    current_app.logger.debug('query_db %s'% sqlstr)
    cur = g.db.execute(sqlstr)
    rv = [dict((cur.description[idx][0], value.replace(r"$double-quote;", r'"'))
               for idx, value in enumerate(row)) for row in cur.fetchall()]

    res = (rv[0] if rv else None) if one else rv
    # print(res)
    return res




def commit_db(sqlstr):
    current_app.logger.debug('commit_db %s'% sqlstr)
    g.db.execute(sqlstr)
    g.db.commit()


def insert_db(_datebase, _map):
    _tuple = insert2str(_map)
    insertstr = 'insert into %s (%s) values(%s);' % (
        _datebase, _tuple[0], _tuple[1])

    commit_db(insertstr)


def exist_db(_datebase, _where):
    wherestr = where2str(_where)
    existstr = 'select * from %s where %s;' % (_datebase, wherestr)
    return query_db(existstr, one=True) != None


def update_db(_datebase, _set, _where):
    setstr = set2str(_set)
    wherestr = where2str(_where)

    updatestr = 'update %s set %s where %s;' % (_datebase, setstr, wherestr)

    commit_db(updatestr)


def delete_db(_datebase, _where):
    wherestr = where2str(_where)

    deletestr = 'delete from %s where %s;' % (_datebase, wherestr)

    commit_db(deletestr)