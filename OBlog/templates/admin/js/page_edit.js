$(document).ready(function () {
    $("ul li#admin-sidebar-2").toggleClass('active');
    vue.refresh();
});


var vue = new Vue({
    el: '#app',
    data: {
        path: "",
        content: "",
        pathClass: "",
        hint: "",
        pageList: [],
        loading: false
    },
    methods: {
        submit: function (type) {
            queryStr = '';

            queryStr += 'path' + '=' + encodeURIComponent(this.path) + '.html&';
            if (type == 'update')
                queryStr += 'content' + '=' + encodeURIComponent(this.content) + '&';

            postData('/api/pages/edit/' + type + '/', queryStr, (data) => {
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
        refresh: function () {
            getData('/api/pages/edit/getlist/', data => {
                this.pageList = data;
            }, 'getList');
        },
        setfilename: function (path) {
            path = path.split('.')
            if (path.length > 1)
                path.splice(path.length - 1, 1);
            this.path = path.join('.');
        }
    },
    watch: {
        path: function () {
            waitUntilLast('searchPageTemplate', () => {
                vue.loading = true;
                postData('/api/pages/edit/get/', encodeURI('path=' + this.path + '.html'), data => {
                    if (data['status'] == '0') {
                        this.content = data['content'];
                        this.pathClass = "has-warning";
                        this.hint = "文件存在";
                    } else {
                        this.pathClass = "has-error";
                        this.hint = "文件不存在";
                    }
                    vue.loading = false;
                }, 'getTemplate');
            }, 1000);

        },
    }
});