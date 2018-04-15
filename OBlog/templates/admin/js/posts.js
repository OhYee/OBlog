$(document).ready(function () {
    $("ul li#admin-sidebar-3").toggleClass('active');
    vue.loading = true;

    var data = [];
    for (var key in jsonData) {
        var item = jsonData[key];
        item.published = item.published == 'true' ? "已发布✔" : "未发布❌";
        item.exist = true;
        data.push(item);
    }
    vue.posts = data;
    vue.loading = false;
});

var vue = new Vue({
    el: '#app',
    data: {
        posts: [],
        loading: true,
        alert: {
            class: "",
            title: "",
            content: ""
        }
    },
    methods: {
        submit: function (idx) {
            queryStr = 'url=' + encodeURIComponent(this.posts[idx].url);

            postData('/api/posts/delete/', queryStr, (data) => {
                console.log(data);
                if (data['status'] == 0) {
                    this.alert = {
                        class: "alert-success",
                        title: "恭喜",
                        content: "删除成功"
                    };
                    this.posts[idx].exist = false;
                    this.$set(this.posts, idx, this, posts[idx]);
                } else if (data['status'] == 1) {
                    this.alert = {
                        class: "alert-warning",
                        title: "注意",
                        content: "删除失败"
                    };
                } else {
                    this.alert = {
                        class: "alert-warning",
                        title: "警告",
                        content: "服务器返回未知信息"
                    };
                }
                window.location.href = "#alert";
            }, 'delete' + idx);
        },
        close: function () {
            this.alert = {
                class: "",
                title: "",
                content: ""
            };
        }
    },
    watch: {},
});