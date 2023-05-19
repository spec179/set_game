import sqlite3
import traceback

COLUMNS = {'users': ('login', 'password', 'count'), 'test_users': ('login', 'password', 'count')}


class Database:
    def __init__(self, name):
        self.name = name

    def column_names(self):
        return ', '.join(COLUMNS[self.name])

    @staticmethod
    def _question_marks(num):
        return ', '.join(['?'] * num)

    def get(self, json: dict):
        conn = sqlite3.connect(f"{self.name}.sqlite")
        cur = conn.cursor()
        column = list(json.keys())[0]
        res = cur.execute(f"SELECT {self.column_names()} FROM users WHERE {column}=(?)", json[column])
        selected = res.fetchone()
        if selected is not None:
            selected = {COLUMNS[i]: selected[i] for i in range(len(COLUMNS[self.name]))}
        conn.close()
        return selected

    def insert(self, json: dict):
        conn = sqlite3.connect(f"{self.name}.sqlite")
        cur = conn.cursor()
        columns_num = len(list(json.keys()))
        try:
            cur.execute(f"INSERT INTO {self.name} VALUES({Database._question_marks(columns_num)})",
                        (json[x] for x in COLUMNS[self.name]))
            conn.commit()
        except sqlite3.Error as e:
            conn.close()
            return {"ok": False, "error": {"type": str(e.__class__), "traceback": traceback.format_exception(e)}}
        else:
            conn.close()
            return {"ok": True}

    def update(self, json_a: dict, json_b: dict):
        conn = sqlite3.connect(f"{self.name}.sqlite")
        cur = conn.cursor()
        key_a, key_b = list(json_a.keys())[0], list(json_b.keys())[0]
        try:
            if json_b[key_b] == '$inc':
                json_b[key_b] = self.get(json_a)[key_b] + 1
            cur.execute(f"UPDATE {self.name} SET {key_b} = (?) WHERE {key_a} = (?)", (json_b[key_b], json_a[key_a]))
            conn.commit()
        except sqlite3.Error as e:
            conn.close()
            return {"ok": False, "error": {"type": str(e.__class__),
                                           "traceback": traceback.format_exception(e, type(e), )}}
        else:
            conn.close()
            return {"ok": True}
