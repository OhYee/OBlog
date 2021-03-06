$(document).ready(function () {
    $("ul li#admin-sidebar-5").toggleClass('active');
    vue.loading = true;
    var data = [];
    jsonData.forEach(item => {
        item.newenglish = item.english;
        item.hint = "";
        item.blockClass = "";
        item.match = true;
        data.push(item)
    });
    vue.tags = data;
    vue.loading = false;
});

var vue = new Vue({
    el: '#app',
    data: {
        tags: {},
        loading: true,
        searchtext: "",
    },
    methods: {
        submit: function (idx) {
            queryStr = '';
            keyList = ['chinese', 'english', 'newenglish', 'class', 'img'];
            keyList.forEach(key => {
                console.log(idx, key, this.tags[idx])
                queryStr += key + '=' + encodeURIComponent(this.tags[idx][key]) + '&';
            });
            console.log(queryStr);
            postData('/api/tags/update/', queryStr, (data) => {
                console.log(data);
                if (data['status'] == '0') {
                    this.tags[idx].blockClass = "has-success";
                    this.tags[idx].hint = "修改成功";
                    this.tags[idx].english = this.tags[idx].newenglish;

                } else if (data['status'] == '1') {
                    this.tags[idx].blockClass = "has-warning";
                    this.tags[idx].hint = "修改失败，请检查格式";
                } else if (data['status'] == '2') {
                    this.tags[idx].blockClass = "has-warning";
                    this.tags[idx].hint = "修改失败，映射关系冲突";
                } else {
                    this.tags[idx].blockClass = "has-error";
                    this.tags[idx].hint = "服务器返回未知信息";
                }
                this.$set(this.tags, idx, this.tags[idx]);
            }, 'submit' + idx);
        },
        clear: function (idx) {
            this.tags[idx].hint = "";
            this.tags[idx].blockClass = "";
            this.$set(this.tags, idx, this.tags[idx]);
        },
        listReverse: function () {
            this.tags.reverse();
        }
    },
    watch: {
        searchtext: function () {
            waitUntilLast('searchtext', () => {
                searchItem(this.tags, this.searchtext);
            }, 500);
        }
    },
});