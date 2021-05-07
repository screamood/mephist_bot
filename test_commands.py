import db_meth

def test_command(event, cursor, FOR_CONTROL):
    FOR_CONTROL['vk_session'].method('messages.send', {'random_id':FOR_CONTROL['cur_time'](), 'peer_id':event.message.from_id, 'message':'Привет, пидорас!'})

meths={
'/привет':[test_command]
}
