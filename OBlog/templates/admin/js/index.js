$(document).ready(() => {
    vue.loading = true;
    var data = [];
    for (var key in jsonData) {
        var item = jsonData[key];
        if (key == 'pages' || key == 'friends')
            continue;
        data.class = "";
        data.hint = "";
        data.needClear = false;
        data.push(item);
    }
    vue.siteConfig = data;
    vue.loading = false;
});

var vue = new Vue({
    el: '#app',
    data: {
        siteConfig: [],
        loading: true,
    },
    methods: {
        submit: function(idx) {
            queryStr = "";
            keyList = ['sid', 'value']
            keyList.forEach(key => {
                queryStr += key + '=' + this.siteConfig[idx][key] + '&';
            });

            console.log(queryStr)
            postData('/api/admin/update/', encodeURI(queryStr), (data) => {
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
        clear: function(idx) {
            if (this.siteConfig[idx].needClear == true) {
                this.siteConfig[idx].class = '';
                this.siteConfig[idx].hint = '';
                this.siteConfig[idx].needClear = false;
                this.$set(this.siteConfig, idx, this.siteConfig[idx]);
            }
        }
    }
});