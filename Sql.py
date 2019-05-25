# 查找用户名是否存在
def do_query_user(name):
    sql = "select * from user where name = '%s'" % name
    return sql

# 插入用户
def do_insert_user(name,pwd):
    sql = "insert into user (name,passwd) values('%s','%s')" % (name,pwd)
    return sql

# 匹配用户名和密码
def do_find_user(name,pwd):
    sql = "select * from user where name = '%s' and passwd = '%s'" % (name,pwd)
    return sql

# 根据书名查找
def do_query_by_bookName(book_name):
    sql = "select * from books where book_name='%s'" % book_name
    return sql

# 根据作者查找
def do_query_by_author(author):
    sql = "select * from books where author_name = '%s'" % author
    return sql

def do_query_id(author,name):
    sql = "select id from books where author_name='%s' and book_name='%s'"%(author,name)
    return sql

def do_section(id):  #阅读
    id = "B" + str(id[0][0])
    sql = "select book_section from %s"%id
    return sql

def do_read(section,id):
    id = "B"+str(id)
    sql = "select section_path from %s where book_section = '%s'"%(id,section)
    return sql

def do_download(id):
    id = int(id)
    sql = "select book_path from books where id = %d"%id
    return sql

