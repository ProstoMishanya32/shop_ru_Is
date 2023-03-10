import sqlite3

def dict_factory(cursor, row):
    save_dict = {}
    for idx, col in enumerate(cursor.description):
        save_dict[col[0]] = row[idx]
    return save_dict

def update_format_args(sql, parameters: dict):
    sql = f"{sql} WHERE "
    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])
    return sql, list(parameters.values())

def update_format(sql, parameters: dict):
    if "XXX" not in sql: sql += " XXX "

    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)

    return sql, list(parameters.values())


class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cur = self.connection.cursor()

    def start_bot(self, colorama):
        #БД с пользователями
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS
        users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        lang TEXT)""")

        # БД c категориями
        self.cur.execute(""" 
        CREATE TABLE IF NOT EXISTS 
        category(
        increment INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        category_name TEXT)""")

        # БД c товарами
        self.cur.execute(""" 
        CREATE TABLE  IF NOT EXISTS 
        items(
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT,
        item_price INTEGER,
        item_description TEXT,
        item_photo TEXT,
        category_id INTEGER,
        discount_len_item INTEGER,
        discount INTEGER)""")

        #Данные о покупках
        self.cur.execute("""
        CREATE TABLE  IF NOT EXISTS 
        purchases(
        increment INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        user_name TEXT,
        purchase_price INTEGER,
        purchase_item_id INTEGER,
        purchase_item_name TEXT,
        purchase_date TEXT)""")

        self.connection.commit()
        print(colorama.Fore.RED + "--- Базы данных подключены ---")




    def registation_user(self, user_id, username, lang):
        try:
            self.cur.execute(f"INSERT INTO users(user_id, username, lang) VALUES (?, ?, ?)", (user_id, username, lang))
        except sqlite3.IntegrityError:
            self.cur.execute("UPDATE users SET (lang, username) = (?, ?) WHERE user_id = ?", (lang, username, user_id))
        self.connection.commit()

    def check_user(self, user_id):
        member = self.cur.execute(f"SELECT user_id, lang FROM users WHERE user_id = ?", (user_id,)).fetchone()
        if member == None:
            return False
        else:
            try:
                return member[1]
            except:
                return member['lang']

    def get_all_info(self, category):
        self.cur.row_factory = dict_factory
        sql = f"SELECT * FROM {category}"
        return self.cur.execute(sql).fetchall()

    # Добавление категории
    def add_category(self, category_id, category_name):
        self.cur.row_factory = dict_factory
        self.cur.execute("INSERT INTO category (category_id, category_name) VALUES (?, ?)", [category_id, category_name])
        self.connection.commit()

    def get_item(self, **kwargs):
        self.cur.row_factory = dict_factory
        sql = f"SELECT * FROM items"
        sql, parameters = update_format_args(sql, kwargs)
        return self.cur.execute(sql, parameters).fetchone()

    def get_all_item(self, **kwargs):
        self.cur.row_factory = dict_factory
        sql = f"SELECT * FROM items"
        sql, parameters = update_format_args(sql, kwargs)
        return self.cur.execute(sql, parameters).fetchall()




    def get_category(self, **kwargs):
        self.cur.row_factory = dict_factory
        sql = f"SELECT * FROM category"
        sql, parameters = update_format_args(sql, kwargs)
        return self.cur.execute(sql, parameters).fetchone()

    def update_items(self, position_id, **kwargs):
        self.cur.row_factory = dict_factory
        sql = f"UPDATE items SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(position_id)
        self.cur.execute(sql + "WHERE item_id = ?", parameters)
        self.connection.commit()

    def update_category(self,  category_id, **kwargs):
        self.cur.row_factory = dict_factory
        sql = f"UPDATE category SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(category_id)
        self.cur.execute(sql + "WHERE category_id = ?", parameters)
        self.connection.commit()

    def delete_category(self, **kwargs):
        self.cur.row_factory = dict_factory
        sql = "DELETE FROM category"
        sql, parameters = update_format_args(sql, kwargs)
        self.cur.execute(sql, parameters)
        self.connection.commit()

    def delete_items(self, **kwargs):
        self.cur.row_factory = dict_factory
        sql = "DELETE FROM items"
        sql, parameters = update_format_args(sql, kwargs)
        self.cur.execute(sql, parameters)
        self.connection.commit()



    def clear_add_items(self):
        self.cur.row_factory = dict_factory
        sql = "DELETE FROM items"
        self.cur.execute(sql)
        self.connection.commit()

    def clear_all_category(self):
        self.cur.row_factory = dict_factory
        sql = "DELETE FROM category"
        self.cur.execute(sql)
        self.connection.commit()

    def add_items(self, item_name, item_price, item_description, item_photo, category_id):
            self.cur.row_factory = dict_factory
            self.cur.execute("INSERT INTO items"
                        "(item_name, item_price, item_description, item_photo, category_id) VALUES (?, ?, ?, ?, ?)",
                        [item_name, item_price, item_description,
                         item_photo, category_id])
            self.connection.commit()
            item_id = self.cur.execute('SELECT item_id FROM items').fetchall()
            return item_id[-1]['item_id']

    def add_discout(self, discout, len_item, item_id):
            self.cur.row_factory = dict_factory
            self.cur.execute("UPDATE items SET (discount_len_item, discount) = (?, ?) WHERE item_id = ?", (len_item, discout, item_id))
            self.connection.commit()


    def get_discout(self, item_id):
        self.cur.row_factory = dict_factory
        data = self.cur.execute("SELECT discount_len_item, discount FROM items  WHERE item_id = ?",  (item_id,)).fetchone()
        return data

    def get_users(self):
        self.cur.row_factory = dict_factory
        data = self.cur.execute("SELECT * FROM users").fetchall()
        return data


    def off_discount(self, item_id):
        self.cur.row_factory = dict_factory
        self.cur.execute("UPDATE items SET (discount_len_item, discount) = (?, ?) WHERE item_id = ?",(None, None, item_id))
        self.connection.commit()
