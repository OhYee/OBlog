from .. import database as db
from ..getData.Site import getConfig

import hashlib


def update(_set):
    password = getConfig()['Password']
    if password != _set['Password']:
        _set['Password'] = hashlib.md5(_set['Password'].encode()).hexdigest()
    for name in _set:
        db.update_db("SiteConfig", {"value": _set[name]}, {"name": name})
