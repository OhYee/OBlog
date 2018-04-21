import json
from flask import request
from . import searchApiBP
from .main import searchPosts,searchTags


@searchApiBP.route('/get/', methods=['POST'])
def search():
    postRequest = request.form.to_dict()
    searchwords = postRequest['searchwords']
    res = {
        'posts':searchPosts(searchwords),
        'tags':searchTags(searchwords)
    }
    return json.dumps(res)


@searchApiBP.route('/get/post/', methods=['POST'])
def searchPost():
    postRequest = request.form.to_dict()
    res = searchPublishedPost(postRequest['searchwords'])
    return json.dumps(res)
