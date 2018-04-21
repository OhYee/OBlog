$(document).ready(function() {
    $("ul li#admin-sidebar-2").toggleClass('active');
    vue.loading = true;
    var data = [];
    for (var key in jsonData) {
        var item = jsonData[key];
        item.oldurl = item.url;
        item.show = item.show == 'true' ? true : false;
        item.exist = true;
        item.class = "";
        item.hint = "";
        item.needClear = false;
        data.push(item);
    }
    vue.pages = data.sort((a, b) => parseInt(a.idx) - parseInt(b.idx));
    vue.loading = false;
});

var vue = new Vue({
    el: '#app',
    data: {
        add: {
            url: "",
            title: "",
            idx: "",
            class: "",
            hint: "",
        },
        pages: {},
        loading: true,
    },
    methods: {
        submit: function(type, idx) {
            console.log(type, idx)
            queryStr = '';
            if (type == 'add') {
                keyList = ['url', 'title', 'idx']
                keyList.forEach(key => {
                    queryStr += key + '=' + encodeURIComponent(this.add[key]) + '&';
                });
            } else if (type == "update") {
                keyList = ['oldurl', 'url', 'title', 'idx', 'show']
                keyList.forEach(key => {
                    queryStr += key + '=' + encodeURIComponent(this.pages[idx][key]) + '&';
                });
            } else if (type == "delete") {
                queryStr = 'url=' + encodeURIComponent(this.pages[idx].oldurl);
            } else {
                return;
            }
            console.log(queryStr);
            postData('/api/pages/' + type + '/', queryStr, (data) => {
                console.log(data);
                if (data['status'] == 0) {
                    if (type == 'add') {
                        var temp = this.add;
                        this.add = {
                            url: "",
                            title: "",
                            idx: "",
                            hint: "页面增加成功",
                            class: "has-success",
                        }
                        temp.exist = true;
                        temp.oldurl = temp.url;
                        this.pages.push(temp);
                        this.pages.sort((a, b) => parseInt(a.idx) - parseInt(b.idx));
                    } else if (type == "update") {
                        this.pages[idx].class = "has-success";
                        this.pages[idx].hint = "页面修改成功";
                        this.pages[idx].needClear = true;
                        this.$set(this.pages, idx, this.pages[idx]);

                        this.pages.sort((a, b) => parseInt(a.idx) - parseInt(b.idx));
                    } else if (type == "delete") {
                        this.pages[idx].exist = false;
                    }
                } else if (data['status'] == 1) {
                    if (type == 'add') {
                        console.log("123")
                        this.add.class = "has-warning";
                        this.add.hint = "页面修改失败";
                    } else {
                        this.pages[idx].class = "has-warning";
                        this.pages[idx].needClear = true;
                        if (type == "update") {
                            this.pages[idx].hint = "页面修改失败";
                        } else if (type == "delete") {
                            this.pages[idx].hint = "页面删除失败";
                        }
                        this.$set(this.pages, idx, this.pages[idx]);
                    }
                } else {
                    if (type == 'add') {
                        this.add.class = "has-danger";
                        this.add.hint = "服务器错误";
                    } else {
                        this.pages[idx].class = "has-danger";
                        this.pages[idx].needClear = true;
                        if (type == "update") {
                            this.pages[idx].hint = "服务器错误";
                        } else if (type == "delete") {
                            this.pages[idx].hint = "服务器错误";
                        }
                        this.pages[idx].hint = "";
                    }
                }
            }, 'submit' + type + idx);
        },
        clear: function(idx) {
            console.log("clear", idx)
            if (idx == -1) {
                this.add.hint = "";
                this.add.class = "";
            } else {
                if (this.pages[idx].needClear == true) {
                    this.pages[idx].hint = "";
                    this.pages[idx].class = "";
                    this.pages[idx].needClear = false;
                    this.$set(this.pages, idx, this.pages[idx]);
                }
            }
        }
    },
    watch: {},
});