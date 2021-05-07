#проверяет существование записи в таблице (проверяет, есть ли такой vk_id в таблице)
def check_for_id(vk_id, cursor, conn):
    cursor.execute('SELECT EXISTS(SELECT vk_id FROM MAIN_TABLE WHERE vk_id = '+str(vk_id)+')')
    res = cursor.fetchall()[0][0]
    conn.commit()
    if res>0: return 1
    return 0

#добавляет пользователя в БД
#vk_id, revuild_vk_id - числовой тип, stop_themes - массив, FIO - строка

###mailing_groups ЗАПОЛНЯЕТСЯ АДМИНАМИ ВРУЧНУЮ!! Это группы, которым данный человек может рассылать соощения.
def add_user(conn, vk_id, rebuild_vk_id, stop_themes, FIO, first_name, group_num, status, lang):
    conn.cursor().execute('INSERT INTO MAIN_TABLE VALUES({}, {}, "{}", "{}", "{}", "{}", "[]", {}, "{}")'.format(vk_id, rebuild_vk_id, str(stop_themes), FIO, first_name, group_num, status, lang))
    conn.commit()

def del_user(conn, vk_id):
    conn.cursor().execute('DELETE FROM MAIN_TABLE WHERE vk_id = '+str(vk_id))
    conn.commit()

def edit_lang(conn, vk_id, new_lang):
    p = conn.cursor().execute("SELECT lang from MAIN_TABLE WHERE vk_id ="+str(vk_id)).fetchone()
    conn.cursor().execute('UPDATE MAIN_TABLE SET lang="'+str(new_lang)+'" WHERE vk_id='+str(vk_id))
    conn.commit()


def get_lang(conn, vk_id):
    p = conn.cursor().execute("SELECT lang from MAIN_TABLE WHERE vk_id ="+str(vk_id)).fetchone()
    conn.commit()
    return str(p[0])
