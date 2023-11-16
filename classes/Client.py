from classes.Db import Db

KEY_ID_CLIENT = 0
KEY_NIP = 1
KEY_DOMAIN = 2

class Client: 
    id_client = 0
    NIP = ""
    domain = ""
    
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def get_clients(last, limit):
        db = Db(DB_PATH)
        db.connect()
        cur = db.cursor()
        cur.execute("SELECT * FROM client WHERE id_client > ? LIMIT ?", (last, limit))
        res = cur.fetchall()
        db.close()
        clients = list()
        for client in res:
            cl = Client()
            cl.id_client = client[KEY_ID_CLIENT]
            cl.NIP = client[KEY_NIP]
            cl.domain = client[KEY_DOMAIN]
            clients.append(cl)
        return clients
