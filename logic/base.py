import sqlite3
import datetime
import os

from config import settings


class ToDoItem:

    def __init__(self, title, content, pub_date=None):
        self.title = title
        self.content = content
        if pub_date:
            self._pub_date = pub_date
        else:
            self._pub_date = datetime.datetime.now().date()

        self.db = os.path.join(settings.BASE_DIR, settings.DB_NAME)

    def __str__(self):
        line = '=' * 32
        response = (
            line +
            f"\n\t{self.title}\n\n\t{self.content}\n\n\t{self.pub_date}\n" +
            line
        )
        return response

    def __repr__(self):
        return f'<ToDoItem: {self.title}>'

    @property
    def pub_date(self):
        return self._pub_date

    @pub_date.setter
    def pub_date(self, value):
        raise ValueError('Pub date has no been changed')

    def save(self):
        try:
            conn, c = self._open_db()
            purchases = (self.title, self.content, self.pub_date)
            c.execute("INSERT INTO todo VALUES (?,?,?)", purchases)
        except sqlite3.OperationalError:
            c.execute(
                "CREATE TABLE todo"
                "(title text primary key not null unique,"
                "content text not null,date text not null)"
            )

            c.execute("INSERT INTO todo VALUES (?,?,?)", purchases)
        except sqlite3.IntegrityError:
            raise ValueError('Task with the same title already exists')

        conn.commit()
        conn.close()

    def delete(self):
        if not os.path.isfile(self.db):
            raise ValueError('You need to create a DB')

        conn, c = self._open_db()
        c.execute("SELECT * FROM todo WHERE title=?", (self.title, ))
        if not c.fetchone():
            raise ValueError("You don't save this item")

        c.execute("DELETE FROM todo WHERE title=?", (self.title, ))
        conn.commit()
        conn.close()

    def _open_db(self):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        return conn, c


class ToDoList:
    def __init__(self):
        self.db = os.path.join(settings.BASE_DIR, settings.DB_NAME)
        self.todo_list = []

        self._set_todo_list()

    def __str__(self):
        print_all = ''
        for item in self.todo_list:
            print_all += f'\t> {item.title} ({item.pub_date})\n'

        return print_all

    def __repr__(self):
        return f'<ToDoList: {self.todo_list}>'

    def get(self, title):
        for item in self.todo_list:
            if item.title == title:
                return item

        raise ValueError('No such item exists')

    def add(self, title, content):
        new_item = ToDoItem(title, content)
        new_item.save()
        self.todo_list.append(new_item)

    def delete(self, title):
        if title == 'all' or title == '':
            conn, c = self._open_db()
            c.execute("DELETE FROM todo")
            conn.commit()
            conn.close()
            self.todo_list.clear()
            return

        for item in self.todo_list:
            if item.title == title:
                item.delete()
                self.todo_list.remove(item)
                break
        else:
            raise ValueError('No such item exists for delete')

    def _set_todo_list(self):
        try:
            conn, c = self._open_db()
            c.execute("SELECT * FROM todo ORDER BY date")
        except sqlite3.OperationalError:
            c.execute(
                "CREATE TABLE todo"
                "(title text primary key not null unique,"
                "content text not null,date text not null)"
            )
            c.execute("SELECT * FROM todo ORDER BY date")

        for item in c.fetchall():
            self.todo_list.append(ToDoItem(item[0], item[1], item[2]))

        conn.close()

    def _open_db(self):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        return conn, c
