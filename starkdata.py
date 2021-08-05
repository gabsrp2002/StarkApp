import sqlite3
from time import strftime, localtime


class StarkData:
    def __init__(self, filename=None):
        """
        Initializes the connection
        """
        assert filename is not None, "You must provide a file name!"

        self.con = sqlite3.connect(filename, isolation_level=None)

        self.con.execute("""CREATE TABLE IF NOT EXISTS products (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            color TEXT NOT NULL,
            size TEXT NOT NULL,
            in_stock INTEGER NOT NULL,
            price REAL NOT NULL DEFAULT 0.00
        )""")
        self.con.execute("""CREATE TABLE IF NOT EXISTS history (
            description TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )""")
        self.con.row_factory = sqlite3.Row

    def search_product(self, product_name):
        """
        Given a product name,
        returns all product (sqlite3.row) that has that name in it.
        """
        result = []

        # Makes the searching name lowercased
        product_name = product_name.lower()
        # Filter all possible products
        rows = self.con.execute(
            "SELECT * FROM products ORDER BY name, color").fetchall()
        for row in rows:
            if product_name in row['name'].lower():
                result.append(row)

        return result

    def add_product(self, product):
        """
        Given a tuple 'product' that represents a product with its name, color,
        size and stocks, inserts it into the table.
        """
        self.con.execute(
            """INSERT INTO products (name, color, size, in_stock, price)
            VALUES (?, ?, ?, ?, ?)""", product)

    def delete_product(self, product_id):
        """
        Deletes a product given its id
        """
        self.con.execute("DELETE FROM products WHERE id = ?", (product_id, ))

    def get_product(self, product_id):
        """
        Given the product id, returns a sqlite3.row representing the product
        Returns None if the product doesn't exist
        """
        return self.con.execute("SELECT * FROM products WHERE id = ?",
                                (product_id, )).fetchone()

    def update_stock(self, product_id, new_stock):
        """
        Updates the product stock.
        """
        self.con.execute("UPDATE products SET in_stock = ? WHERE id = ?",
                         (new_stock, product_id))

    def update_price(self, product_id, new_price):
        """
        Updates the product price
        """
        self.con.execute("UPDATE products SET price = ? WHERE id = ?",
                         (new_price, product_id))

    def add_history(self, description):
        """
        Adds the description to the history
        """
        date = strftime("%Y-%m-%d", localtime())
        time = strftime("%H:%M", localtime())
        self.con.execute(
            """INSERT INTO history (description, date, time)
            VALUES (?, ?, ?)""", (description, date, time))

    def read_history(self, start_date, end_date):
        """
        Returns all history from start_date untill end_date, inclusive
        """
        return self.con.execute(
            """SELECT * FROM history WHERE date >= ? AND date <= ?""",
            (start_date, end_date))

    def close(self):
        """
        Closes the connection
        """
        self.con.close()
