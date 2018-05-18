var url = "{{ comments_url }}";

var vue = new Vue({
    el: '#vue_comments',
    data: {
        comments: [],
        loading: true,
        sortType: '逆序排序',
        email: "",
        sendemail: true,
        raw: "",
        alert: {
            class: "",
            title: "",
            content: ""
        }
    },
    methods: {
        makeSortType: function (_sortType) {
            console.log(_sortType)

            this.sortType = _sortType;
            this.makeSort();
        },
        makeSort: function () {
            this.comments = this.comments.sort((a, b) => {
                var ret;
                if (this.sortType == "顺序排序") {
                    ret = parseInt(a.id) - parseInt(b.id);
                } else {
                    ret = parseInt(b.id) - parseInt(a.id);
                }
                return ret;
            });
            this.loading = false;
            this.$nextTick(function () {
                this.refresh();
            });
        },
        submit: function () {
            var parse = /^[A-Za-z0-9\u4e00-\u9fa5]+@[A-Za-z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
            if (/^[A-Za-z0-9\u4e00-\u9fa5]+@[A-Za-z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/.exec(this.email)) {
                var queryStr = "email=" + encodeURIComponent(this.email) + "&sendemail=" + encodeURIComponent(this.sendemail) + "&raw=" + encodeURIComponent(this.raw) + "&url=" + encodeURIComponent(url);
                postData('/api/comments/add/', queryStr, data => {
                    console.log(data);
                    if (data['status'] == '0') {
                        this.alert = {
                            class: "alert-success",
                            title: "成功",
                            content: "评论成功发出"
                        };
                        data['comment'].sendemail = data['comment'].sendemail == 'true' ? true : false;
                        data['comment'].ad = data['comment'].ad == 'true' ? true : false;
                        this.comments.push(data['comment']);
                        this.makeSort();
                        this.$nextTick(function () {
                            this.refresh();
                        });
                    } else if (data['status'] == '1') {
                        this.alert = {
                            class: "alert-warning",
                            title: "注意",
                            content: "邮件格式错误"
                        };
                    } else if (data['status'] == '2') {
                        this.alert = {
                            class: "alert-warning",
                            title: "注意",
                            content: "评论内容必须存在中文(Comments must contain Chinese.)"
                        };
                    } else {
                        this.alert = {
                            class: "alert-danger",
                            title: "警告",
                            content: "服务器返回未知信息"
                        };
                    }
                }, "addComments");
            } else {
                this.alert = {
                    class: "alert-warning",
                    title: "注意",
                    content: "邮件格式错误"
                };
            }
        },
        refresh: function () {
            $("div.fold").css("display", "none");
            $('pre codeblock').each(function (i, block) {
                hljs.highlightBlock(block);
            });
        },
        close: function () {
            this.alert = {
                class: "",
                title: "",
                content: ""
            };
        }
    },
    watch: {
        email: function () {
            if (this.eclass) {
                this.eclass = "";
                this.icon = "";
                this.hint = "";
            }
        },
        sortType: function () {
            this.makeSort();
        }
    }
});

$(document).ready(() => {
    vue.loading = true;
    var queryStr = "url=" + encodeURIComponent(url);
    postData("/api/comments/get/", queryStr, data => {
        for (var i = 0; i < data.length; ++i) {
            data[i].sendemail = data[i].sendemail == 'true' ? true : false;
            data[i].ad = data[i].ad == 'true' ? true : false;
        }
        vue.comments = data;
        vue.makeSort();
        vue.$nextTick(function () {
            vue.refresh();
            vue.loading = false;
        });

    }, 'getComments');
});

