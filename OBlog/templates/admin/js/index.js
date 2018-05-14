$(document).ready(() => {
    vue.loading = true;
    var data = [];
    for (var key in jsonData) {
        var item = jsonData[key];
        if (key == 'pages' || key == 'friends')
            continue;
        item.class = "";
        item.hint = "";
        item.needClear = false;
        item.match = true;
        data.push(item);
    }
    data.sort((a, b) => parseInt(a.idx) - parseInt(b.idx))
    vue.siteConfig = data;
    vue.loading = false;
});

var vue = new Vue({
    el: '#app',
    data: {
        siteConfig: [],
        loading: true,
        searchtext: "",
    },
    methods: {
        submit: function (idx) {
            queryStr = "";
            keyList = ['sid', 'value']
            keyList.forEach(key => {
                queryStr += key + '=' + encodeURIComponent(this.siteConfig[idx][key]) + '&';
            });

            console.log(queryStr)
            postData('/api/admin/update/', queryStr, (data) => {
                if (data['status'] == '0') {
                    this.siteConfig[idx].class = 'has-success';
                    this.siteConfig[idx].hint = '修改成功';
                } else if (data['status'] == '1') {
                    this.siteConfig[idx].class = 'has-waring';
                    this.siteConfig[idx].hint = '修改失败';
                } else {
                    this.siteConfig[idx].class = 'has-error';
                    this.siteConfig[idx].hint = '服务器返回未知信息';
                }
                this.siteConfig[idx].needClear = true;
                this.$set(this.siteConfig, idx, this.siteConfig[idx]);
                console.log('ok');
            }, "update" + idx.toString())
        },
        clear: function (idx) {
            if (this.siteConfig[idx].needClear == true) {
                this.siteConfig[idx].class = '';
                this.siteConfig[idx].hint = '';
                this.siteConfig[idx].needClear = false;
                this.$set(this.siteConfig, idx, this.siteConfig[idx]);
            }
        },
        listReverse: function () {
            this.siteConfig.reverse();
        }
    },
    watch: {
        searchtext: function () {
            waitUntilLast('searchtext', () => {
                searchItem(this.siteConfig, this.searchtext);
            }, 500);
        }
    }
});