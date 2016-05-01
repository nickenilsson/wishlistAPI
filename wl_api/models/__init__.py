import collections


class TransformedDict(collections.MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys"""


    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        if key not in self.fields:
            raise KeyError("'{0}' is not a valid field for object of type {1}. Allowed fields are: {2}"
                           .format(key, type(self).__name__, self.fields))

        #if type(value) is not self.fields[key]:
        #   raise TypeError('Expected type {0} for field {1}. Got {2}'.format(self.fields[key], key, type(value)))
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key


class User(TransformedDict):
    def __init__(self, *args, **kwargs):
        self.fields = {
            '_id',
            'name',
            'email',
            'image_url',
            'facebook_id',
            'last_modified',
            'wishlists'
        }
        super(User, self).__init__(*args, **kwargs)


class WishList(TransformedDict):
    def __init__(self, *args, **kwargs):
        self.fields = {
            '_id',
            '_author_id',
            'image_url',
            'description',
            'name',
            'last_modified',
            'articles'
        }
        super(WishList, self).__init__(*args, **kwargs)


class Article(TransformedDict):

    def __init__(self, *args, **kwargs):
        self.fields = {
            '_id',
            'name',
            'last_modified',
            'description',
            'image_url',
            'status'
        }
        super(Article, self).__init__(*args, **kwargs)
