from flask import current_app
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb

builtin_list = list

def init_app(app):
    pass


class Album(ndb.Model):
    artist = ndb.StringProperty()
    imageUrl = ndb.StringProperty()
    title = ndb.StringProperty()


def from_datastore(entity):
    if not entity:
        return None

    if isinstance(entity, builtin_list):
        entity = entity.pop()

    album = {}
    album['id'] = entity.key.id()
    album['artist'] = entity.artist
    album['imageUrl'] = entity.imageUrl
    album['title'] = entity.title
    return album


def list(limit=10, cursor=None):
    if cursor:
        cursor = Cursor(urlsafe=cursor)

    query = Album.query().order(Album.title)
    entities, cursor, more = query.fetch_page(limit, start_cursor=cursor)
    entities = builtin_list(map(from_datastore, entities))
    return entities, cursor.urlsafe() if len(entities) == limit else None


def read(id):
    album_key = ndb.Key('Album', int(id))
    results = album_key.get()
    return from_datastore(results)


def update(data, id=None):
    if id:
        key = ndb.Key('Album', int(id))
        album = key.get()
    else:
        album = Album()

    album.artist = data['artist']
    album.imageUrl = data['imageUrl']
    album.title = data['title']
    album.put()
    return from_datastore(album)

create = update


def delete(id):
    key = ndb.Key('Album', int(id))
    key.delete()
