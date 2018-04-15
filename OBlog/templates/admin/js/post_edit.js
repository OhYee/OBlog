var type = "add";

$(document).ready(function () {
    $("ul li#admin-sidebar-3").toggleClass('active');
    var nowTime = (new Date).Format();
    vue.time.value = vue.updatetime.value = nowTime;
    vue.view.value = '0';



    if (jsonData) {
        type = "update";
        console.log(jsonData)
        var attribList = ['url', 'title', 'time', 'updatetime', 'view', 'tags'];
        attribList.forEach(item => {
            vue[item].value = jsonData[item];
        });
        vue.raw = jsonData['raw'];
        vue.abstruct = jsonData['abstruct'];
        vue.published = jsonData['published'] == 'true' ? true : false;
        vue.oldurl = vue.url.value;
    }
});

var vue = new Vue({
    el: '#app',
    data: {
        oldurl: "",
        url: {
            value: "",
            class: "",
            hint: "",
            icon: "",
        },
        title: {
            value: "",
            class: "",
            hint: "",
            icon: "",
        },
        time: {
            value: "",
            class: "",
            hint: "",
            icon: "",
        },
        updatetime: {
            value: "",
            class: "",
            hint: "",
            icon: "",
        },
        view: {
            value: "",
            class: "",
            hint: "",
            icon: "",
        },
        tags: {
            value: "",
            class: "",
            hint: "",
            icon: "",
        },
        abstruct: "",
        raw: "",
        published: true,
        loading: false,
        alert: {
            class: "",
            title: "",
            content: "",
        }
    },
    methods: {
        submit: function () {
            queryStr = '';
            queryList = ['url', 'title', 'time', 'updatetime', 'view', 'tags'];
            queryList.forEach(item => queryStr += item + '=' + encodeURIComponent(this[item].value) + '&');
            queryStr += 'abstruct=' + encodeURIComponent(this.abstruct) + '&';
            queryStr += 'raw=' + encodeURIComponent(this.raw) + '&';
            queryStr += 'published=' + encodeURIComponent(this.published) + '&';

            if (type == 'update')
                queryStr += 'oldurl=' + encodeURIComponent(this.oldurl) + '&';

            console.log(queryStr);

            postData('/api/posts/' + type + '/', queryStr, (data) => {
                console.log(data);
                if (data['status'] == 0) {
                    if (type == 'add') {
                        this.alert = {
                            class: "alert-success",
                            title: "恭喜！",
                            content: "发布成功",
                        }
                        type = 'update';
                        this.oldurl = this.url.value;
                    } else {
                        this.alert = {
                            class: "alert-success",
                            title: "恭喜！",
                            content: "修改成功",
                        }
                    }
                } else if (data['status'] == 1) {
                    this.alert = {
                        class: "alert-warning",
                        title: "注意！",
                        content: "格式存在问题",
                    }
                } else if (data['status'] == 2) {
                    this.alert = {
                        class: "alert-warning",
                        title: "注意！",
                        content: "已存在同样链接的文章",
                    }
                } else {
                    this.alert = {
                        class: "alert-danger",
                        title: "警告！",
                        content: "服务器返回未知信息",
                    }
                }
                window.location.href = "#alert";
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
        'url.value': function () {
            waitUntilLast('url', () => {
                pattern = /^[\w\-\.,@?^=%&:~\+#]+(?:\/[\w\-\.,@?^=%&:~\+#]+)*$/;
                if (pattern.exec(this.url.value)) {
                    if (this.oldurl == this.url.value) {
                        this.url.class = "has-success";
                        this.url.hint = '连接可用';
                        this.url.icon = "glyphicon-ok";
                    } else {
                        this.url.class = "has-warning";
                        this.url.hint = "链接合法，正在查询是否可用";
                        this.url.icon = "glyphicon-refresh";
                        postData('/api/posts/exist/', encodeURI('url=' + this.url.value), data => {
                            if (data['status'] == '0') {
                                this.url.class = "has-success";
                                this.url.hint = '连接可用';
                                this.url.icon = "glyphicon-ok";
                            } else if (data['status'] == '1') {
                                this.url.class = "has-error";
                                this.url.hint = '该链接文章已存在';
                                this.url.icon = "glyphicon-remove";
                            } else {
                                this.url.class = "has-error";
                                this.url.hint = '服务器错误';
                                this.url.icon = "glyphicon-remove";
                            }
                        }, 'urlExists');
                    }
                } else {
                    this.url.class = "has-error";
                    this.url.hint = "链接格式错误";
                    this.url.icon = "glyphicon-remove";
                }
            }, 1000);
        },
        'time.value': function () {
            pattern = /^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$/
            if (pattern.exec(this.time.value)) {
                this.time.class = "has-success";
                this.time.hint = "";
                this.time.icon = "glyphicon-ok";
            } else {
                this.time.class = "has-error";
                this.time.hint = "时间格式错误（xxxx-xx-xx xx:xx:xx）"
                this.time.icon = "glyphicon-remove";
            }
        },
        'updatetime.value': function () {
            pattern = /^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$/
            if (pattern.exec(this.updatetime.value)) {
                this.updatetime.class = "has-success";
                this.updatetime.hint = "";
                this.updatetime.icon = "glyphicon-ok";
            } else {
                this.updatetime.class = "has-error";
                this.updatetime.hint = "时间格式错误（xxxx-xx-xx xx:xx:xx）"
                this.updatetime.icon = "glyphicon-remove";
            }
        },
        'view.value': function () {
            //^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$/,
            //^[0-9]+$/,
            //^[\w\-\.,@?^=%&:~\+#]+(?:\/[\w\-\.,@?^=%&:~\+#]+)*$/
            waitUntilLast('view', () => {
                pattern = /^[0-9]+$/;
                if (pattern.exec(this.view.value)) {
                    this.view.class = "has-success";
                    this.view.hint = "";
                    this.view.icon = "glyphicon-ok";
                } else {
                    this.view.class = "has-error";
                    this.view.hint = "请输入非负整数";
                    this.view.icon = "glyphicon-remove";
                }
            }, 1000);
        },
        'tags.value': function () {
            waitUntilLast('tags', () => {
                this.tags.value = this.tags.value.replace('，', ',')
                this.tags.class = "has-success";
                this.tags.icon = "glyphicon-ok";
                var tagsList = Array.from(new Set(this.tags.value.split(',')));
                console.log(tagsList);
                this.tags.value = tagsList.join(',');
                this.tags.hint = '<span class="badge">' + tagsList.join('</span>&nbsp;<span class="badge">') + "</span>";
            }, 1000);
        }
    }
});