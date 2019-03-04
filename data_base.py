import sqlite3

class Data_base(object):
    # utworzenie połączenia z bazą przechowywaną na dysku
    def __init__(self):

        self.con = sqlite3.connect('test.db')
        # dostęp do kolumn przez indeksy i przez nazwy
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
    def creating_table(self):
        self.cur.executescript("""
            DROP TABLE IF EXISTS VERTEX;
            CREATE TABLE IF NOT EXISTS VERTEX (
                id INTEGER PRIMARY KEY ASC,
                x  INTEGER NOT NULL,
                y  INTEGER NOT NULL
                ) """ )

        self.cur.executescript("""
            DROP TABLE IF EXISTS EDGES;
            CREATE TABLE IF NOT EXISTS EDGES (
                id INTEGER PRIMARY KEY ASC,
                V1 INTEGER NOT NULL,
                V2 INTEGER NOT NULL
                )""")
    def add_vertex(self,x,y):
        # wstawiamy jeden rekord danych
        self.cur.execute('INSERT INTO VERTEX VALUES(NULL, ?, ?);', (x,y))
        self.con.commit()

        # wykonuje zapytanie SQL, które pobierze id klasy "1A" z tabeli "klasa".

    def adding_edge(self,V1,V2):
        # wstawiam wiele rekordów
        self.cur.execute('INSERT INTO EDGES VALUES(NULL, ?, ?);', (V1, V2))
        self.con.commit()
        # zatwierdzamy zmiany w bazie
    def read_data(self):
        """Funkcja pobiera i wyświetla dane z bazy."""
        self.cur.execute(
            """
            SELECT EDGES.id,V1,V2 FROM EDGES,VERTEX
            WHERE EDGES.id=VERTEX.id
            """)
        edges = self.cur.fetchall()
        for e in edges:
            print(e['id'], e['V1'], e['V2'])
        return edges