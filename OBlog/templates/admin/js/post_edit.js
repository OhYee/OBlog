$(document).ready(function() {
    $("ul li#admin-sidebar-2").toggleClass('active');
    var nowTime = (new Date).Format();
    vue.time.value = vue.updatetime.value = nowTime;
    vue.view.value = '0';
});


var vue = new Vue({
    el: '#app',
    data: {
        oldrl: "",
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
        content: "",
        loading: false
    },
    methods: {
        submit: function(type) {
            queryStr = '';

            queryStr += 'path' + '=' + this.path + '.html&';
            if (type == 'update')
                queryStr += 'content' + '=' + this.content + '&';

            postData('/api/pages/edit/' + type + '/', encodeURI(queryStr), (data) => {
                if (data['status'] == 0) {
                    this.pathClass = "has-success";
                    this.hint = "编辑成功";
                    this.refresh();
                } else if (data['status'] == 1) {
                    this.pathClass = "has-error";
                    this.hint = "编辑失败";
                } else {
                    this.pathClass = "has-error";
                    this.hint = "服务器错误";
                }
            });
        },
        refresh: function() {
            getData('/api/pages/edit/getlist/', data => {
                this.pageList = data;
            }, 'getList');
        },
        setfilename: function(path) {
            path = path.split('.')
            if (path.length > 1)
                path.splice(path.length - 1, 1);
            this.path = path.join('.');
        }
    },
    watch: {
        'url.value': function() {
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
                        postData('/api/posts/edit/exist/', encodeURI('url=' + this.url.value), data => {
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
        'time.value': function() {
            pattern = /^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$/
            if (pattern.exec(this.time.value)) {
                this.time.class = "has-success";
                this.time.hint = "";
                this.time.icon = "glyphicon-ok";
            } else {
                this.time.class = "has-error";
                this.time.hint = "时间格式错误"
                this.time.icon = "glyphicon-remove";
            }
        },
        'updatetime.value': function() {
            pattern = /^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$/
            if (pattern.exec(this.updatetime.value)) {
                this.updatetime.class = "has-success";
                this.updatetime.hint = "";
                this.updatetime.icon = "glyphicon-ok";
            } else {
                this.updatetime.class = "has-error";
                this.updatetime.hint = "时间格式错误"
                this.updatetime.icon = "glyphicon-remove";
            }
        },
        'view.value': function() {
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
        }
    }
});