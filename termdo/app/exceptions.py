class TermDoException(Exception):
    pass


class DeleteError(TermDoException):
    pass


class ChangeError(TermDoException):
    pass


class SaveError(TermDoException):
    pass


class DeleteNotCreatedDbError(DeleteError):
    def __init__(self):
        self.args = ('You need to create a DB', )


class DeleteNotSavedItemError(DeleteError):
    def __init__(self):
        self.args = ("You don't save this item", )


class DeleteDoesNotExists(DeleteError):
    def __init__(self):
        self.args = ('No such item exists for delete', )


class ChangeDoesNotExists(ChangeError):
    def __init__(self):
        self.args = ('Element with such id does not exists', )


class ChangeNotCreatedDbError(ChangeError):
    def __init__(self):
        self.args = ('You need to create a DB')


class SaveExistingItemError(SaveError):
    def __init__(self):
        self.args = ('Item with the same title already exists', )

