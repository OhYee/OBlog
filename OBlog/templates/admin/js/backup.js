var vue = new Vue({
    el: '#app',
    data: {
        buttons: [
            { class: '', hint: '导出标签', type: 'exportTags' },
            { class: '', hint: '导入标签', type: 'importTags' },
            { class: '', hint: '导入文章', type: 'importPosts' },
            { class: '', hint: '导出文章', type: 'exportPosts' },
        ],
        alert: {
            class: "",
            title: "",
            content: "",
        },
        loading: true,
    },
    methods: {
        close: function () {
            this.alert = {
                class: "",
                title: "",
                content: ""
            };
        },
        submit: function (type, idx) {
            console.log(type, idx)
            this.$set(this.buttons, idx, {
                class: 'info',
                hint: 'loading...',
                type: type
            });
            getData('/api/backup/' + type + '/', data => {
                console.log(data);
                var hint = '';
                if (type == "exportTags")
                    hint = "导出标签"
                else if (type == "importTags")
                    hint = "导入标签"
                else if (type == "importPosts")
                    hint = "导入文章"
                else
                    hint = "导出文章"
                this.$set(this.buttons, idx, {
                    class: '',
                    hint: hint,
                    type: type
                });
                if (data['status']) {
                    this.alert = {
                        class: "alert-success",
                        title: "成功",
                        content: data['hint']
                    };
                }else{
                    this.alert = {
                        class: "alert-danger",
                        title: "错误",
                        content: "服务器返回未知信息"
                    };
                }
            }, type);
        }
    },
    watch: {

    },
});