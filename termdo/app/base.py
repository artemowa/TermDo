import sqlite3
import datetime
import os

from config import settings    # with BASE_DIR and DB_NAME
from app import exceptions   # this app errors


class OpenDbMixin:
    '''
    Mixin that opens the database
    '''
    def open_db(self):
        '''
        Return tuple with coonect and cursor objects. The value of the
        self.db is taken as the database file name
        '''
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        return conn, c


class ToDoItem(OpenDbMixin):
    '''
    ToDo list item
    '''

    def __init__(self, title, pub_date=None):
        '''
        Create item with given title. By default pub_date is now. self.db
        attribute is the DB file path
        '''
        self.title = title
        if pub_date:
            self._pub_date = pub_date
        else:
            self._pub_date = datetime.datetime.now().date()

        self.db = os.path.join(settings.BASE_DIR, settings.DB_NAME)

    def __repr__(self):
        return f'<ToDoItem: {self.title}>'

    @property
    def pub_date(self):
        '''
        Immutable property
        '''
        return self._pub_date

    @pub_date.setter
    def pub_date(self, value):
        raise ValueError('Pub date has no been changed')

    def change(self, new_title):
        '''
        Change the title of the item
        '''
        if not os.path.isfile(self.db):
            # if DB file has not been created
            raise exceptions.ChangeNotCreatedDbError

        conn, c = self.open_db()
        c.execute("UPDATE todo SET title=? WHERE title=?",
                  (new_title, self.title))
        conn.commit()
        conn.close()
        self.title = new_title

    def save(self):
        '''
        Save item in DB. Create DB table if it was not created.
        If item with the same title already exists, raise
        exceptions.SaveExistingItemError error
        '''
        try:
            conn, c = self.open_db()
            purchases = (self.title, self.pub_date)
            c.execute("INSERT INTO todo VALUES (?,?)", purchases)
        except sqlite3.OperationalError:
            # if DB table has not been created
            c.execute(
                "CREATE TABLE todo"
                "(title text not null,date text not null)"
            )

            c.execute("INSERT INTO todo VALUES (?,?)", purchases)
        except sqlite3.IntegrityError:
            # if item with this title already exists
            raise exceptions.SaveExistingItemError

        conn.commit()
        conn.close()

    def delete(self):
        '''
        Delete item from DB. Raise exceptions.DeleteNotCreatedDbError
        if DB file has not been created. Raise
        exceptions.DeleteNotSavedItemError if item has not been saved.
        '''
        if not os.path.isfile(self.db):
            # if DB file has not been created
            raise exceptions.DeleteNotCreatedDbError

        conn, c = self.open_db()
        c.execute("SELECT * FROM todo WHERE title=?", (self.title, ))
        if not c.fetchone():
            # if item has not been saved
            raise exceptions.DeleteNotSavedItemError

        c.execute("DELETE FROM todo WHERE title=?", (self.title, ))
        conn.commit()
        conn.close()


class ToDoList(OpenDbMixin):

    def __init__(self):
        self.db = os.path.join(settings.BASE_DIR, settings.DB_NAME)
        self.todo_list = []

        self._set_todo_list()

    def __str__(self):
        print_all = ''
        for index, item in enumerate(self.todo_list):
            print_all += f'\t{index+1}. {item.title} ({item.pub_date})\n'

        return print_all

    def __repr__(self):
        return f'<ToDoList: {self.todo_list}>'

    def __getitem__(self, index):
        return self.todo_list[index]

    def change(self, identifier, new_title):
        try:
            item = self.todo_list[identifier-1]
            item.title = new_title
        except IndexError:
            raise exceptions.ChangeDoesNotExists

    def add(self, title):
        new_item = ToDoItem(title)
        new_item.save()
        self.todo_list.append(new_item)

    def delete(self, identifier):
        try:
            item = self.todo_list[identifier-1]
            item.delete()
            self.todo_list.remove(item)
        except IndexError:
            raise exceptions.DeleteDoesNotExists

    def clear(self):
        conn, c = self.open_db()
        c.execute("DELETE FROM todo")
        self.todo_list.clear()
        conn.commit()
        conn.close()

    def _set_todo_list(self):
        try:
            conn, c = self.open_db()
            c.execute("SELECT * FROM todo ORDER BY date")
        except sqlite3.OperationalError:
            c.execute(
                "CREATE TABLE todo"
                "(title text primary key not null,date text not null)"
            )
            c.execute("SELECT * FROM todo ORDER BY date")

        for item in c.fetchall():
            self.todo_list.append(ToDoItem(item[0], item[1]))

        conn.close()

