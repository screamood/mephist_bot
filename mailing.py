import db_meth, enru

def get_lang(event, cursor, FOR_CONTROL):
    return db_meth.get_lang(FOR_CONTROL['conn'], event.message.from_id)

def add_stop_theme(event, cursor, FOR_CONTROL):
    from_id = event.message.from_id
    text = event.message.text[16::]
    if not text.isdigit():
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_add_st_th1'][get_lang(event, cursor, FOR_CONTROL)]})
        return
    num_theme = int(text)
    if db_meth.check_theme_for_id(num_theme, cursor, FOR_CONTROL['conn'])==0:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_add_st_th2'][get_lang(event, cursor, FOR_CONTROL)]})
        return
    db_meth.add_stop_theme(from_id, cursor, FOR_CONTROL['conn'], num_theme)
    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['succ_add_st_th'][get_lang(event, cursor, FOR_CONTROL)]})

def del_stop_theme(event, cursor, FOR_CONTROL):
    from_id = event.message.from_id
    text = event.message.text[16::]
    if not text.isdigit():
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_del_st_th1'][get_lang(event, cursor, FOR_CONTROL)]})
        return
    num_theme = int(text)
    if db_meth.check_stop_theme(from_id, cursor, FOR_CONTROL['conn'], num_theme)==0:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_del_st_th2'][get_lang(event, cursor, FOR_CONTROL)]})
        return
    db_meth.del_stop_theme(from_id, cursor, FOR_CONTROL['conn'], num_theme)
    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['succ_del_st_th'][get_lang(event, cursor, FOR_CONTROL)]})

def themes_list(event, cursor, FOR_CONTROL):
    from_id = event.message.from_id
    lst = db_meth.get_themes_list(from_id, cursor, FOR_CONTROL['conn'])
    res = enru.sub[3][get_lang(event, cursor, FOR_CONTROL)]+':\n'

    if len(lst)==0:
        lst+=enru.sub[5][get_lang(event, cursor, FOR_CONTROL)]

    for i in lst:
        res+='{id}. {name}\n'.format(id = lst[i]['id'], name = lst[i][get_lang(event, cursor, FOR_CONTROL)])
    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':res})

def get_self_blist(event, cursor, FOR_CONTROL):
    from_id = event.message.from_id
    lst = db_meth.get_themes_list(from_id, cursor, FOR_CONTROL['conn'])
    mys = db_meth.get_stop_themes(from_id, cursor, FOR_CONTROL['conn'])
    res = enru.sub[4][get_lang(event, cursor, FOR_CONTROL)]+':\n'

    if len(mys)==0:
        res+=enru.sub[5][get_lang(event, cursor, FOR_CONTROL)]

    print('mys:---------')
    print(mys)
    print('-------------')
    for i in mys:
        res+='{id}. {name}\n'.format(id = lst[i]['id'], name = lst[i][get_lang(event, cursor, FOR_CONTROL)])
    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':res})

def mailing_msg(event, cursor, FOR_CONTROL):
    from_id = event.message.from_id
    text = event.message.text[6::]

    if db_meth.check_for_id(from_id, cursor, FOR_CONTROL['conn'])==0:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_mail_th4'][get_lang(event, cursor, FOR_CONTROL)]})
        return

    if not(',' in text):
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_mail_th1'][get_lang(event, cursor, FOR_CONTROL)]})
        return

    msg = text.split(',')[1]
    r = text.split(',')[0].split(' ')
    if len(r)<2:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_mail_th1'][get_lang(event, cursor, FOR_CONTROL)]})
        return
    if not(r[0].isdigit() or r[0]=='*'):
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_mail_th1'][get_lang(event, cursor, FOR_CONTROL)]})
        return

    org_id = r[0]

    if org_id!='*':
        cursor.execute('SELECT EXISTS(SELECT org_id FROM ORGANISATIONS WHERE org_id = '+str(org_id)+')')
        t = cursor.fetchall()[0][0]
        if t<=0:
            FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_del_org_th2'][get_lang(event, cursor, FOR_CONTROL)]})
            return
        if int(FOR_CONTROL['conn'].cursor().execute('SELECT status FROM ORG_{} WHERE vk_id = {}'.format(org_id, from_id)).fetchone()[0])<1:
            FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_mail_th2'][get_lang(event, cursor, FOR_CONTROL)]})
            return

    del(r[0])
    for i in r:
        if not i.isdigit():
            FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_mail_th1'][get_lang(event, cursor, FOR_CONTROL)]})
            return
        if db_meth.check_theme_for_id(int(i), cursor, FOR_CONTROL['conn'])==0:
            FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_mail_th3'][get_lang(event, cursor, FOR_CONTROL)]})
            return

    comm = 'SELECT * FROM ORG_{}'.format(org_id)
    if org_id == '*': comm = 'SELECT * FROM MAIN_TABLE WHERE status==1'
    cursor.execute(comm)
    lst = cursor.fetchall()

    if org_id!='*': org_name = FOR_CONTROL['conn'].cursor().execute('SELECT name FROM ORGANISATIONS WHERE org_id = {}'.format(org_id)).fetchone()[0]
    else: org_name = 'empty'
    list_for_mail = []
    for i in lst:
        now_id = i[0]
        if now_id==from_id: continue
        s = 1
        for k in r:
            if int(k) in db_meth.get_stop_themes(now_id, cursor, FOR_CONTROL['conn']):
                s = 0
                break
        if s==0:
            continue
        list_for_mail.append(now_id)

    t = 8
    if org_id == '*': t-=1

    name_author = FOR_CONTROL['conn'].cursor().execute('SELECT FIO FROM MAIN_TABLE WHERE vk_id = {}'.format(from_id)).fetchone()[0]
    for i in list_for_mail:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':i, 'message':enru.sub[t][get_lang(event, cursor, FOR_CONTROL)].format(from_id = from_id, from_name=name_author, text = msg, org_name = org_name)})

    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub[10][get_lang(event, cursor, FOR_CONTROL)]})


meths={
'/add_stop_theme':[add_stop_theme],
'/del_stop_theme':[del_stop_theme],
'/themes_list':[themes_list],
'/my_blist':[get_self_blist],
'/mail':[mailing_msg]
}
