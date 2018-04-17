$(document).ready(function() {
    $("ul li#admin-sidebar-6").toggleClass('active');
    vue.loading = true;
    var data = [];
    jsonData.forEach(item => {
        item.oldname = item.name;
        item.exist = true;
        item.class = "";
        item.hint = "";
        item.needClear = false;
        data.push(item);
    });
    vue.friends = jsonData;
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
        friends: {},
        loading: true,
    },
    methods: {
        submit: function(type, idx) {
            console.log(type, idx)
            queryStr = '';
            if (type == 'add') {
                keyList = ['url', 'name', 'idx']
                keyList.forEach(key => {
                    queryStr += key + '=' + encodeURIComponent(this.add[key]) + '&';
                });
            } else if (type == "update") {
                keyList = ['oldname', 'url', 'name', 'idx', 'show']
                keyList.forEach(key => {
                    queryStr += key + '=' + encodeURIComponent(this.friends[idx][key]) + '&';
                });
            } else if (type == "delete") {
                queryStr = 'name=' + encodeURIComponent(this.friends[idx].oldname);
            } else {
                return;
            }
            console.log(queryStr);
            postData('/api/friends/' + type + '/', queryStr, (data) => {
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
                        this.friends.push(temp);
                        this.friends.sort((a, b) => parseInt(a.idx) - parseInt(b.idx));
                    } else if (type == "update") {
                        this.friends[idx].class = "has-success";
                        this.friends[idx].hint = "页面修改成功";
                        this.friends[idx].needClear = true;
                        this.$set(this.friends, idx, this.friends[idx]);

                        this.friends.sort((a, b) => parseInt(a.idx) - parseInt(b.idx));
                    } else if (type == "delete") {
                        this.friends[idx].exist = false;
                    }
                } else if (data['status'] == 1) {
                    if (type == 'add') {
                        console.log("123")
                        this.add.class = "has-warning";
                        this.add.hint = "页面修改失败";
                    } else {
                        this.friends[idx].class = "has-warning";
                        this.friends[idx].needClear = true;
                        if (type == "update") {
                            this.friends[idx].hint = "页面修改失败";
                        } else if (type == "delete") {
                            this.friends[idx].hint = "页面删除失败";
                        }
                        this.$set(this.friends, idx, this.friends[idx]);
                    }
                } else {
                    if (type == 'add') {
                        this.add.class = "has-danger";
                        this.add.hint = "服务器错误";
                    } else {
                        this.friends[idx].class = "has-danger";
                        this.friends[idx].needClear = true;
                        if (type == "update") {
                            this.friends[idx].hint = "服务器错误";
                        } else if (type == "delete") {
                            this.friends[idx].hint = "服务器错误";
                        }
                        this.friends[idx].hint = "";
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
                if (this.friends[idx].needClear == true) {
                    this.friends[idx].hint = "";
                    this.friends[idx].class = "";
                    this.friends[idx].needClear = false;
                    this.$set(this.friends, idx, this.friends[idx]);
                }
            }
        }
    },
    watch: {},
});