from flask import render_template, request, session, redirect, url_for, send_from_directory, flash
from OBlog import app

from OBlog.back.getData.Posts import getPost, getAllPosts, getPublishedPosts
from OBlog.back.getData.Tags import getRawTags
from OBlog.back.search import search_AllPosts, search_PublishedPosts, search_Tags
from OBlog.back.getData.Discuss import getDiscussOfUrl, getAllDiscussOfUrl, getAllDiscuss, getDiscussOfID

import json

import time

@app.route('/api/posts/')
def api_posts():
    print(time.time())
    res = json.dumps(getPublishedPosts())
    print(time.time())
    return res


@app.route('/api/allposts/')
def api_allposts():
    print(time.time())
    res = json.dumps(getAllPosts())
    print(time.time())
    return res


@app.route('/api/post/<path:url>')
def api_post(url):
    return json.dumps(getPost(url))


@app.route('/api/tags/')
def api_tags():
    return json.dumps(getRawTags())


@app.route('/api/test/')
def api_test():
    return json.dumps([1, 2, 3, 4, 5])


@app.route('/api/search_tags/<searchwords>')
def api_search_tags(searchwords):
    return json.dumps(search_Tags(searchwords))


@app.route('/api/search_posts/<searchwords>')
def api_search_posts(searchwords):
    print(time.time())
    res = json.dumps(search_PublishedPosts(searchwords))
    print(time.time())
    return res


@app.route('/api/search_allposts/<searchwords>')
def api_search_allposts(searchwords):
    print(time.time())
    res = json.dumps(search_AllPosts(searchwords))
    print(time.time())
    return res


@app.route('/api/discuss/<path:url>')
def api_discuss_of_url(url):
    return json.dumps(getDiscussOfUrl(url))


@app.route('/api/alldiscuss/<path:url>')
def api_all_discuss_of_url(url):
    return json.dumps(getAllDiscussOfUrl(url))


@app.route('/api/alldiscuss/')
def api_all_discuss():
    return json.dumps(getAllDiscuss())


@app.route('/api/discussid/<_id>')
def api_discuss_of_id(_id):
    return json.dumps(getDiscussOfID(_id))
