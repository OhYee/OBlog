$(document).ready(function() {
    $("ul li#admin-sidebar-4").toggleClass('active');
    vue.loading = true;
    var data = [];
    for (var key in jsonData) {
        var item = jsonData[key];
        item.show == 'true' ? true : false;
        item.exist = true;
        item.class = "";
        item.hint = "";
        data.push(item);
    }
    vue.goods = data.sort((a, b) => parseInt(a.gid) - parseInt(b.gid));
    vue.add.time = (new Date).Format("yyyy-MM-dd");
    vue.loading = false;
});

var vue = new Vue({
    el: '#app',
    data: {
        add: {
            name: "",
            abstruct: "",
            time: "",
            show: true,
            img: "",
            value1: "",
            class: "",
            hint: "",
        },
        goods: {},
        loading: true,
    },
    methods: {
        submit: function(type, idx) {
            console.log(type, idx)
            queryStr = '';
            if (type == 'add') {
                keyList = ['name', 'abstruct', 'time', 'img', 'value1', 'show']
                keyList.forEach(key => {
                    queryStr += key + '=' + encodeURIComponent(this.add[key]) + '&';
                });
            } else if (type == "update") {
                keyList = ['gid', 'name', 'abstruct', 'time', 'img', 'value1', 'show']
                keyList.forEach(key => {
                    queryStr += key + '=' + encodeURIComponent(this.goods[idx][key]) + '&';
                });
            } else {
                return;
            }
            console.log(queryStr);
            postData('/api/goods/' + type + '/', queryStr, (data) => {
                console.log(data);
                if (data['status'] == 0) {
                    if (type == 'add') {
                        var temp = this.add;
                        this.add = {
                            name: "",
                            abstruct: "",
                            time: (new Date).Format("yyyy-MM-dd"),
                            show: true,
                            img: "",
                            value1: "",
                            class: "has-success",
                            hint: "商品新建成功",
                        };
                        temp.exist = true;
                        this.goods.push(temp);
                    } else {
                        this.goods[idx].class = "has-success";
                        this.goods[idx].hint = "商品修改成功";
                        this.$set(this.goods, idx, this.goods[idx]);
                    }
                    this.goods.sort((a, b) => parseInt(a.idx) - parseInt(b.idx));
                } else if (data['status'] == 1) {
                    if (type == 'add') {
                        this.add.class = "has-warning";
                        this.add.hint = "商品新建失败";
                    } else {
                        this.goods[idx].class = "has-warning";
                        this.goods[idx].hint = "商品修改失败"
                        this.$set(this.goods, idx, this.goods[idx]);
                    }
                } else {
                    if (type == 'add') {
                        this.add.class = "has-danger";
                        this.add.hint = "服务器返回未知信息";
                    } else {
                        this.goods[idx].class = "has-danger";
                        this.goods[idx].hint = "服务器返回未知信息";
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
                if (this.goods[idx].class != "") {
                    this.goods[idx].hint = "";
                    this.goods[idx].class = "";
                    this.$set(this.goods, idx, this.goods[idx]);
                }
            }
        }
    }
});