#проверяет существование записи в таблице (проверяет, есть ли такой vk_id в таблице)
def check_for_id(vk_id, cursor, conn):
    cursor.execute('SELECT EXISTS(SELECT vk_id FROM MAIN_TABLE WHERE vk_id = '+str(vk_id)+')')
    res = cursor.fetchall()[0][0]
    conn.commit()
    if res>0: return 1
    return 0

#проверяет существование ТЕМЫ в таблице (проверяет, есть ли такой vk_id в таблице)
#1 - есть, 0 - нет
def check_theme_for_id(id, cursor, conn):
    cursor.execute('SELECT EXISTS(SELECT id FROM THEMES WHERE id = '+str(id)+')')
    res = cursor.fetchall()[0][0]
    conn.commit()
    if res>0: return 1
    return 0

#проверяет есть ли пользователь с vk_id в организации с org_id
#1 - есть, 0 - нет
def check_org_for_id(vk_id, cursor, conn, org_id):
    cursor.execute('SELECT EXISTS(SELECT vk_id FROM ORG_{} WHERE vk_id = {})'.format(org_id, vk_id))
    res = cursor.fetchall()[0][0]
    #conn.commit()
    if res>0: return 1
    return 0
#добавляет пользователя в БД
#vk_id, revuild_vk_id - числовой тип, stop_themes - массив, FIO - строка

###mailing_groups ЗАПОЛНЯЕТСЯ АДМИНАМИ ВРУЧНУЮ!! Это группы, которым данный человек может рассылать соощения.
def add_user(conn, vk_id, rebuild_vk_id, stop_themes, FIO, first_name, group_num, status, link):
    conn.cursor().execute('INSERT INTO MAIN_TABLE VALUES({}, {}, "{}", "{}", "{}", "{}", "[]", {}, "{}")'.format(vk_id, rebuild_vk_id, str(stop_themes), FIO, first_name, group_num, status, link))
    conn.commit()

def del_user(conn, vk_id):
    conn.cursor().execute('DELETE FROM MAIN_TABLE WHERE vk_id = '+str(vk_id))
    conn.commit()

def edit_lang(conn, vk_id, new_lang):
    p = conn.cursor().execute("SELECT lang from LG_TABLE WHERE vk_id ="+str(vk_id)).fetchone()
    conn.cursor().execute('UPDATE LG_TABLE SET lang="'+str(new_lang)+'" WHERE vk_id='+str(vk_id))
    conn.commit()

##проверка в таблице LG_TABLE
def check_for_id_lg(vk_id, cursor, conn):
    cursor.execute('SELECT EXISTS(SELECT vk_id FROM LG_TABLE WHERE vk_id = '+str(vk_id)+')')
    res = cursor.fetchall()[0][0]
    #conn.commit()
    if res>0: return 1
    return 0

##1 если пользователь ранее писал боту
##0 если пользователь не писал боту ранее
def set_lang(vk_id, cursor, conn):
    if check_for_id_lg(vk_id, cursor, conn)==1: return 1
    conn.cursor().execute('INSERT INTO LG_TABLE VALUES({}, "{}")'.format(vk_id, 'RU'))
    conn.commit()
    return 0

def get_lang(conn, vk_id):
    p = conn.cursor().execute("SELECT lang from LG_TABLE WHERE vk_id ="+str(vk_id)).fetchone()
    #conn.commit()
    return str(p[0])

#получает массив тем, которые пользователь запретил отправлять себе в рассылке
def get_stop_themes(vk_id, cursor, conn):
    p = conn.cursor().execute("SELECT stop_themes from MAIN_TABLE WHERE vk_id ="+str(vk_id)).fetchone()
    if p[0]=='[]': return []
    res = [int(v) for v in p[0][1:-1:].split(', ')]
    return res

#получает массив групп, которым пользователь может рассылать сообщения
def get_mailing_groups(vk_id, cursor, conn):
    p = conn.cursor().execute("SELECT mailing_groups from MAIN_TABLE WHERE vk_id ="+str(vk_id)).fetchone()
    if p[0]=='[]': return []
    return p[0][1:-1:].replace("'", '').split(', ')

#проверяет, есть ли среди тем пользователя тема с id = theme_num
#1 - есть
#0 - нет
def check_stop_theme(vk_id, cursor, conn, theme_num):
    th = get_stop_themes(vk_id, cursor, conn)
    if theme_num in th: return 1
    return 0

def del_stop_theme(vk_id, cursor, conn, theme_num):
    th = get_stop_themes(vk_id, cursor, conn)
    th.remove(theme_num)
    th_s = '"{'+str(th)[1:-1:]+'}"'
    conn.cursor().execute('UPDATE MAIN_TABLE SET stop_themes='+th_s+' WHERE vk_id='+str(vk_id))
    conn.commit()

def add_stop_theme(vk_id, cursor, conn, theme_num):
    th = get_stop_themes(vk_id, cursor, conn)
    th.append(theme_num)
    th_s = '"{'+str(th)[1:-1:]+'}"'
    conn.cursor().execute('UPDATE MAIN_TABLE SET stop_themes='+th_s+' WHERE vk_id='+str(vk_id))
    conn.commit()

def command_for_add_mailing_groups():
    pass
    #UPDATE MAIN_TABLE SET mailing_groups="{'Б20-101', 'Б20-102'}" WHERE vk_id = 12345

#возвращает массив, описывающий темы (табличкой)
def get_themes_list(vk_id, cursor, conn):
    cursor.execute('SELECT * FROM THEMES')
    res = cursor.fetchall()
    lst = dict()
    for i in res:
        lst[i[0]]={'id':i[0], 'RU':i[1], 'EN':i[2]}
    return lst

#добавляет пользователя с id vk_id в организацию с id org_id, status - статус
#если БД не существует, возвращает 13
def add_to_org_user(vk_id, cursor, conn, org_id, status = 0):
    cursor.execute('SELECT EXISTS(SELECT org_id FROM ORGANISATIONS WHERE org_id = '+str(org_id)+')')
    res = cursor.fetchall()[0][0]
    conn.commit()
    if res<=0:
        return 13
    comm = 'INSERT INTO ORG_{} VALUES ({}, {})'.format(org_id, vk_id, status)
    conn.cursor().execute(comm)
    conn.commit()

#Добавляет в таблицу новую организацию. Возвращает её id
def new_org_append(vk_id, cursor, conn, name, type, group_num='none'):
    cnt = conn.cursor().execute('SELECT COUNT(*) FROM ORGANISATIONS').fetchone()[0]
    #conn.commit()
    conn.cursor().execute('INSERT INTO ORGANISATIONS VALUES({}, "{}", {}, "{}", {})'.format(cnt, name, type, group_num, vk_id))
    conn.commit()
    return cnt

#создает новую организацию. возвращает её id
def new_org(vk_id, cursor, conn, org_name, type, group_num='none'):
    org_id = new_org_append(vk_id, cursor, conn, org_name, type, group_num)
    command = 'CREATE TABLE ORG_{org_num} ("vk_id"	INTEGER, "status"	INTEGER, PRIMARY KEY("vk_id"));'.format(org_num = org_id, org_name = org_name)
    conn.cursor().execute(command)
    conn.commit()
    add_to_org_user(vk_id, cursor, conn, org_id, status = 2)
    return org_id

def kick_user_from_org(vk_id, cursor, conn, org_id):
    conn.cursor().execute('DELETE FROM ORG_{} WHERE vk_id = {}'.format(org_id, vk_id))
    conn.commit()
