import db_meth, hashlib, enru
from bs4 import BeautifulSoup

#Метод преобразовывающий vk id
def rebuild_vk_id(vk_id):
    vk_id*=3
    vk_id = str(vk_id)+'113'
    vk_id = vk_id[::-1]
    return str(vk_id)

#возвращает sha256 хеш строки str (передаешь ПЕРЕВЕРНУТЫЙ id  (для безопасности СОЗДАТЬ ОТДЕЛЬНУЮ ФУНКЦИЮ) - получаешь код для ввода)
def encrypt_str(str):
    return '1'+hashlib.sha256(str.encode()).hexdigest()
    #return "Добрый день.\  ##для тестирования на Самарченко
#\nГармонические колебания."

def get_lang(event, cursor, FOR_CONTROL):
    return db_meth.get_lang(FOR_CONTROL['conn'], event.message.from_id)

def reg(event, cursor, FOR_CONTROL):
    from_id = event.message.from_id
    res = db_meth.check_for_id(from_id, cursor, FOR_CONTROL['conn'])
    if res != 0:
        ans = enru.sub[0][get_lang(event, cursor, FOR_CONTROL)]
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':ans})
        return

    check(event, cursor, FOR_CONTROL, from_id)

def reg_abitur(event, cursor, FOR_CONTROL):
    idd = event.message.from_id

    res = db_meth.check_for_id(idd, cursor, FOR_CONTROL['conn'])
    if res != 0:
        ans = enru.sub[0][get_lang(event, cursor, FOR_CONTROL)]
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':idd, 'message':ans})
        return

    db_meth.add_user(FOR_CONTROL['conn'], idd, rebuild_vk_id(int(idd)), [], 'Абитуриент', 'Абитуриент', '0', 0, 'none')
    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':idd, 'message':enru.sub[1][get_lang(event, cursor, FOR_CONTROL)]})


def check(event, cursor, FOR_CONTROL, idd):
    hash_id = encrypt_str(rebuild_vk_id(idd))
    txt = enru.sub['txt_r'][get_lang(event, cursor, FOR_CONTROL)]
    txt_oj = enru.sub['for_ch'][get_lang(event, cursor, FOR_CONTROL)]
    msg_ = enru.sub['warn_reg'][get_lang(event, cursor, FOR_CONTROL)]
    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':idd, 'message':txt})
    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':idd, 'message':hash_id})
    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':idd, 'message':txt_oj})
    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':idd, 'message':msg_})

def reg_ok(event, cursor, FOR_CONTROL):
    idd = event.message.from_id

    res = db_meth.check_for_id(idd, cursor, FOR_CONTROL['conn'])
    if res != 0:
        ans = enru.sub[0][get_lang(event, cursor, FOR_CONTROL)]
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':idd, 'message':ans})
        return

    str_for_find = encrypt_str(rebuild_vk_id(idd))
    pg = FOR_CONTROL['get_msg_search_page'](str_for_find, FOR_CONTROL['session'])
    soup = BeautifulSoup(pg, "html.parser")

    if 'Сообщения на найдены' in pg:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':idd, 'message':enru.sub['err_reg'][get_lang(event, cursor, FOR_CONTROL)]})
        return

    first_msg = soup.find('div', {'class':'panel panel-post panel-default'}).find('div', {'class':'media-body'}).find('p').text ##код по идее

    if str_for_find not in first_msg:
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':idd, 'message':enru.sub['err_reg'][get_lang(event, cursor, FOR_CONTROL)]})
        return

    author_fio = soup.find('div', {'class':'panel panel-post panel-default'}).find('div', {'class':'media-body'}).find('li').text  ##имя автора по идее
    author_link = 'https://home.mephi.ru/'+soup.find('div', {'class':'panel panel-post panel-default'}).find('div', {'class':'user-avatar user-small'}).find('a').get('href')


    link = 'https://home.mephi.ru'+str(soup.find('div', {'class':'panel panel-post panel-default'}).find('div', {'class':'media-left'}).find('a').get('href'))
    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':idd, 'message':enru.sub['ok_es'][get_lang(event, cursor, FOR_CONTROL)].format(author_fio)})
    t = author_fio.split(' ')
    first_name = t[1]

    r = FOR_CONTROL['session'].get(link)

    status=1

    soup = BeautifulSoup(r.text, "html.parser")

    test = soup.find_all('h3', {'class':'light'})
    for i in test:
        if i.text=='Должности':
            status = 2
            break

    group_num = soup.find('div', {'class':'btn-group'}).find('a', {'class':'btn btn-primary btn-outline'}).text[:-14:]
    db_meth.add_user(FOR_CONTROL['conn'], idd, rebuild_vk_id(int(idd)), [], author_fio, first_name, group_num, status, link)
    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':idd, 'message':enru.sub[2][get_lang(event, cursor, FOR_CONTROL)]})

def reg_cancel(event, cursor, FOR_CONTROL):
    from_id = event.message.from_id
    res = db_meth.check_for_id(from_id, cursor, FOR_CONTROL['conn'])
    if res == 0:
        ans = enru.sub['for_canc'][get_lang(event, cursor, FOR_CONTROL)]
        FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':ans})
        return
    db_meth.del_user(FOR_CONTROL['conn'], from_id)
    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['ok_del'][get_lang(event, cursor, FOR_CONTROL)]})

def change_lang(event, cursor, FOR_CONTROL):
    from_id = event.message.from_id
    l = ['RU', 'EN']
    now = db_meth.get_lang(FOR_CONTROL['conn'], from_id)
    new = l[(l.index(now)+1)%len(l)]
    db_meth.edit_lang(FOR_CONTROL['conn'], from_id, new)
    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':enru.sub['ch_lg'][get_lang(event, cursor, FOR_CONTROL)]})



meths={
'/reg':[reg],
'/ok_reg':[reg_ok],
'/canc_reg':[reg_cancel],
'/app_reg':[reg_abitur],
'/lang':[change_lang]
}
