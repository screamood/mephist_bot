import db_meth, enru, re

def get_lang(event, cursor, FOR_CONTROL):
    return db_meth.get_lang(FOR_CONTROL['conn'], event.message.from_id)

def new_organisations(event, cursor, FOR_CONTROL):
    from_id = event.message.from_id

    if db_meth.check_for_id(from_id, cursor, FOR_CONTROL['conn'])==0:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_new_org_th2'][get_lang(event, cursor, FOR_CONTROL)]})
        return

    text = event.message.text[8::]
    args = text.split(' ')

    del[args[0]]
    if not ((len(args)==2) or (len(args)==3)):
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_new_org'][get_lang(event, cursor, FOR_CONTROL)]})
        return
    if not args[1].isdigit():
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_new_org'][get_lang(event, cursor, FOR_CONTROL)]})
        return
    args[1] = int(args[1])
    if len(args)==2:
        if args[1]==0:
            FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_new_org'][get_lang(event, cursor, FOR_CONTROL)]})
            return
    if len(args)==3:
        if args[1]==1 or args[2].isdigit():
            FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_new_org'][get_lang(event, cursor, FOR_CONTROL)]})
            return

    #проверка что организации, привязанной к такой группе больше нет
    if len(args)==3:
        cursor.execute('SELECT EXISTS(SELECT org_id FROM ORGANISATIONS WHERE num_group = "'+str(args[2])+'")')
        res = cursor.fetchall()[0][0]
        if res>0:
            FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_new_org_th3'][get_lang(event, cursor, FOR_CONTROL)]})
            return

    if len(args)==3: org_id = db_meth.new_org(from_id, cursor, FOR_CONTROL['conn'], args[0], args[1], args[2])
    else: org_id = db_meth.new_org(from_id, cursor, FOR_CONTROL['conn'], args[0], args[1])

    if len(args)==3:
        cursor.execute('SELECT * FROM MAIN_TABLE')
        users = cursor.fetchall()
        for i in users:
            if i[0]==from_id: continue
            if i[5]==args[2]:
                db_meth.add_to_org_user(i[0], cursor, FOR_CONTROL['conn'], org_id)

    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['org_crd'][get_lang(event, cursor, FOR_CONTROL)].format(org_name = args[0], org_id = org_id)})

def delete_org(event, cursor, FOR_CONTROL):
    from_id = event.message.from_id
    text = event.message.text[9::]
    if not text.isdigit():
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_del_org_th1'][get_lang(event, cursor, FOR_CONTROL)]})
        return
    org_num = int(text)
    cursor.execute('SELECT EXISTS(SELECT org_id FROM ORGANISATIONS WHERE org_id = '+str(org_num)+')')
    t = cursor.fetchall()[0][0]
    if t<=0:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_del_org_th2'][get_lang(event, cursor, FOR_CONTROL)]})
        return
    cursor.execute('SELECT creator FROM ORGANISATIONS WHERE org_id = '+str(org_num))
    if from_id!=cursor.fetchall()[0][0]:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_del_org_th3'][get_lang(event, cursor, FOR_CONTROL)]})
        return
    name = cursor.execute('SELECT name FROM ORGANISATIONS WHERE org_id = '+str(org_num)).fetchall()[0][0]
    cursor.execute('DROP TABLE ORG_{}'.format(org_num))
    FOR_CONTROL['conn'].commit()
    cursor.execute('DELETE FROM ORGANISATIONS WHERE org_id = {}'.format(org_num))
    FOR_CONTROL['conn'].commit()
    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['succ_del_org_th'][get_lang(event, cursor, FOR_CONTROL)].format(org_name = name)})

def invite_to_org(event, cursor, FOR_CONTROL):
    from_id = event.message.from_id
    text = event.message.text[5::]
    args = text.split(' ')
    if len(args)<2:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_inv_th1'][get_lang(event, cursor, FOR_CONTROL)]})
        return
    if not args[0].isdigit():
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_inv_th1'][get_lang(event, cursor, FOR_CONTROL)]})
        return

    org_num = int(args[0])
    id_to = int(re.findall(r'\[id(\d+)\|.*\]', text)[0])

    cursor.execute('SELECT EXISTS(SELECT org_id FROM ORGANISATIONS WHERE org_id = '+str(org_num)+')')
    t = cursor.fetchall()[0][0]
    if t<=0:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_del_org_th2'][get_lang(event, cursor, FOR_CONTROL)]})
        return


    cursor.execute('SELECT creator FROM ORGANISATIONS WHERE org_id = '+str(org_num))
    if from_id!=cursor.fetchall()[0][0]:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_inv_th3'][get_lang(event, cursor, FOR_CONTROL)]})
        return

    if db_meth.check_org_for_id(id_to, cursor, FOR_CONTROL['conn'], org_num)==1:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_inv_th4'][get_lang(event, cursor, FOR_CONTROL)]})
        return

    if db_meth.check_for_id(id_to, cursor, FOR_CONTROL['conn'])==0:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_inv_th2'][get_lang(event, cursor, FOR_CONTROL)]})
        return

    db_meth.add_to_org_user(id_to, cursor, FOR_CONTROL['conn'], org_num)
    name = cursor.execute('SELECT name FROM ORGANISATIONS WHERE org_id = '+str(org_num)).fetchall()[0][0]
    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['ok_inv'][get_lang(event, cursor, FOR_CONTROL)].format(org_name = name)})

def kick_from_org(event, cursor, FOR_CONTROL):
    from_id = event.message.from_id
    text = event.message.text[6::]
    args = text.split(' ')
    if len(args)<2:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_kick_th1'][get_lang(event, cursor, FOR_CONTROL)]})
        return
    if not args[0].isdigit():
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_kick_th1'][get_lang(event, cursor, FOR_CONTROL)]})
        return
    org_num = int(args[0])

    id_to = int(re.findall(r'\[id(\d+)\|.*\]', text)[0])

    cursor.execute('SELECT EXISTS(SELECT org_id FROM ORGANISATIONS WHERE org_id = '+str(org_num)+')')
    t = cursor.fetchall()[0][0]
    if t<=0:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_del_org_th2'][get_lang(event, cursor, FOR_CONTROL)]})
        return

    cursor.execute('SELECT creator FROM ORGANISATIONS WHERE org_id = '+str(org_num))
    if from_id!=cursor.fetchall()[0][0]:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_kick_th2'][get_lang(event, cursor, FOR_CONTROL)]})
        return

    if db_meth.check_org_for_id(id_to, cursor, FOR_CONTROL['conn'], org_num)==0:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_kick_th3'][get_lang(event, cursor, FOR_CONTROL)]})
        return

    if db_meth.check_for_id(id_to, cursor, FOR_CONTROL['conn'])==0:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['eec_kick_th4'][get_lang(event, cursor, FOR_CONTROL)]})
        return

    db_meth.kick_user_from_org(id_to, cursor, FOR_CONTROL['conn'], org_num)
    name = cursor.execute('SELECT name FROM ORGANISATIONS WHERE org_id = '+str(org_num)).fetchall()[0][0]
    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['ok_kick_from_org'][get_lang(event, cursor, FOR_CONTROL)].format(org_name = name)})

def get_selflist_orgs(event, cursor, FOR_CONTROL):
    from_id = event.message.from_id
    cursor.execute('SELECT * FROM ORGANISATIONS')
    lst = cursor.fetchall()
    res = enru.sub[6][get_lang(event, cursor, FOR_CONTROL)]+':\n'
    for i in lst:
        if db_meth.check_org_for_id(from_id, cursor, FOR_CONTROL['conn'], i[0])==1:
            res+='{org_id}. {org_name}\n'.format(org_id = i[0], org_name = i[1])
    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':res})


meths={
'/new_org':[new_organisations],
'/del_org':[delete_org],
'/inv':[invite_to_org],
'/kick':[kick_from_org],
'/org_list':[get_selflist_orgs]
}
