from flask import g


def getSite():
    if not hasattr(g, 'getSite'):
        from .blueprint.admin.main import getSiteConfigDict
        res = getSiteConfigDict()
        from .blueprint.pages.main import getPagesDict
        res['pages'] = getPagesDict()
        from .blueprint.friends.main import getFriends
        res['friends'] = getFriends()
        g.getSite = res
    return g.getSite

