import db_meth, enru
from bs4 import BeautifulSoup

def get_lang(event, cursor, FOR_CONTROL):
    return db_meth.get_lang(FOR_CONTROL['conn'], event.message.from_id)

#удаляет символы с a по b включительно
def rep(s, a, b):
    return s[0:a]+s[b+1::]

def get_today_plan(event, cursor, FOR_CONTROL):
    from_id = event.message.from_id
    link = cursor.execute('SELECT link FROM MAIN_TABLE WHERE vk_id = '+str(from_id)).fetchall()[0][0]
    r = FOR_CONTROL['session'].get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    soup = soup.find('div', {'id':'students_wrapper'}).find('div', {'class':'list-group'}).find_all('div', {'class':'list-group-item'})

    res = enru.sub[9][get_lang(event, cursor, FOR_CONTROL)]+':\n'
    for now in soup:
        #time = now.find('div', {'class':'lesson-time'}).text
        #type = now.find('div', {'class':'label label-default label-lesson'}).text

        test = now.text.replace('\n', ' ')

        l = []
        r = []
        bol = 0
        for i in range(len(test)-1):
            if test[i] == ' ' and test[i+1] ==' ' and bol==0:
                l.append(i)
                bol = 1
            if test[i] == ' ' and test[i+1]!=' ' and bol==1:
                r.append(i)
                bol = 0
        if len(l)>len(r):
            del l[len(l)-1]
        l.reverse()
        r.reverse()
        for i in range(len(l)):
            test = rep(test, l[i]+1, r[i])
        if test[0]==' ': test = test[1::]
        res+=(test+'\n')

    ########
    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':from_id, 'message':res})

meths={
'/plan':[get_today_plan]
}
