import psycopg

class Core:
    def __init__(self, user, password, hostname, port, db_name):
        self.conn = psycopg.connect(f"postgres://{user}:{password}@{hostname}:{port}/{db_name}")

class Model:
    def __init__(self):
        pass
