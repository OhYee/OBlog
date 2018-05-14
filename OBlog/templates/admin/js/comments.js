$(document).ready(function () {
    $("ul li#admin-sidebar-8").toggleClass('active');
    vue.loading = true;
    jsonData.forEach(item => {
        item.class = "";
        item.hint = "修改";
        item.ad = item.ad == 'true' ? true : false;
        item.show = item.show == 'true' ? true : false;
        item.sendemail = item.sendemail == 'true' ? true : false;
        item.match = true;
    });
    vue.comments = jsonData;
    vue.loading = false;
});



var vue = new Vue({
    el: '#app',
    data: {
        comments: [],
        loading: true,
        searchtext: "",
    },
    methods: {
        submit: function (idx) {
            this.comments[idx].class = "info";
            this.comments[idx].hint = "loading...";
            this.$set(this.comments, idx, this.comments[idx]);

            var queryStr = ""
            var keyList = ['id', 'sendemail', 'ad', 'show'];
            keyList.forEach(item => {
                queryStr += item + '=' + encodeURIComponent(this.comments[idx][item]) + '&';
            });
            console.log(queryStr);

            postData('/api/comments/update/', queryStr, data => {
                console.log(data);
                if (data['status'] == '0') {
                    this.comments[idx].class = "success";
                    this.comments[idx].hint = "成功";
                } else if (data['status'] == '1') {
                    this.comments[idx].class = "warning";
                    this.comments[idx].hint = "失败";
                } else {
                    this.comments[idx].class = "danger";
                    this.comments[idx].hint = "服务器错误";
                }
                this.$set(this.comments, idx, this.comments[idx]);

                setTimeout(() => {
                    this.comments[idx].class = "";
                    this.comments[idx].hint = "修改";
                    this.$set(this.comments, idx, this.comments[idx]);
                }, 10000);
            }, 'update' + idx);


        },
        listReverse: function () {
            this.comments.reverse();
        }
    },
    watch: {
        searchtext: function () {
            waitUntilLast('searchtext', () => {
                searchItem(this.comments, this.searchtext);
            }, 500);
        }
    },
});