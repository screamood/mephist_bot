from requests_html import HTMLSession
import hashlib, vk_api, time, sqlite3, db_meth, importlib, re, threading
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

################################################################################
#        ПЕРЕМЕННЫЕ                                                            #
################################################################################

com_que_user = dict()
token = '59614a7c9bf58618cf708276bd80190d3111d42f02d9d10f3a50f289db8ac20d803bd913d863e62c05fef'
group_id = 202788672
cur_time = lambda: int(round(time.time() * 1000))
command = dict(from_user=dict(), from_chat=dict(), from_chat_not_adm=dict())

################################################################################
#        ПЕРЕМЕННЫЕ                                                            #
################################################################################

#выполняет авторизацию на home mephi
def auth_in_home_mephi(llogin, ppassword):
    url = 'https://auth.mephi.ru/login'

    session = HTMLSession()
    r = session.get(url)

    data = {
         'username': llogin,
         'password': ppassword,
         'lt': r.html.find('input')[2].attrs['value'],
         'authenticity_token': r.html.find('input')[1].attrs['value']
    }

    r = session.post(url, data=data)

    return session

#выполняет поиск по сообщениям текстом text_for_find
def get_msg_search_page(text_for_find, session):
    r = session.get('https://home.mephi.ru/talks/search?utf8=%E2%9C%93&query='+text_for_find+'&button=')
    #page_save(r)
    return r.text

#сохраняет результат после get-запроса (r - результат запроса)
def page_save(r, filename = 'test.html'):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(r.text)

##Поочередно выполняет сообщения из очереди команд от пользователя вк с id peer_id
def check_msg_user(peer_id, cursor, FOR_CONTROL):
    while True:
        if len(com_que_user[peer_id])!=0:
            by_user(com_que_user[peer_id][0], cursor, FOR_CONTROL)
            del com_que_user[peer_id][0]

#обработка сообщения от пользователя
def by_user(event, cursor, FOR_CONTROL):
    com = event.message.text.lower()
    from_id, peer_id = event.message.from_id, event.message.peer_id
    for k in command['from_user']:
        if com.startswith(k):
            #if vh.is_allowed_msg_from_group(from_id)['is_allowed']==0:
            #    vh.send_to(peer_id, vh.get_nick(from_id)+', Вы не разрешили мне отправлять Вам личные сообщения. Чтобы разрешить, напишите мне что-нибудь в лс.')
            #    return
            command['from_user'][k](event, cursor, FOR_CONTROL)
            return

def get_FIO_from_id(meph_id, session):
    r = session.get('https://home.mephi.ru/users/'+str(meph_id))
    text = r.text

###############################################
###############################################
###############MAIN############################
###############MAIN############################
###############MAIN############################
###############################################
###############################################
if __name__ == "__main__":
    session = auth_in_home_mephi("fid003", "kek3211")
    #get_msg_search_page('Поляков', session)

    vk_session = vk_api.VkApi(token=token)
    longpoll = vk_api.bot_longpoll.VkBotLongPoll(vk_session, group_id)
    vk = vk_session.get_api()

    conn = sqlite3.connect("test1.db", check_same_thread = False)
    cursor = conn.cursor()

    modules = open('data/modules_names.txt', 'r')
    for name_module in modules:
        name = re.sub("\s*\n\s*", ' ', name_module.strip())
        try:
            comm = importlib.import_module(name).meths
            for names in comm:
                sets = comm[names]
                command['from_user'][names]=sets[0]

        except ModuleNotFoundError:
            print('Модуль "'+name+'" не был найден.')

    FOR_CONTROL = dict()
    FOR_CONTROL['conn'] = conn
    FOR_CONTROL['vk_session'] = vk_session
    FOR_CONTROL['cur_time'] = cur_time
    FOR_CONTROL['session'] = session
    FOR_CONTROL['get_msg_search_page'] = get_msg_search_page

    for event in longpoll.listen():
        if event.type== VkBotEventType.MESSAGE_NEW:
            peer_id = event.message.peer_id
            if event.from_user:
                if event.message.from_id<0: continue
                if peer_id not in com_que_user:
                    com_que_user[peer_id]=[]
                    threading.Thread(target=check_msg_user, args=(peer_id, conn.cursor(), FOR_CONTROL,)).start()
                com_que_user[peer_id].append(event)
