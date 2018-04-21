var vue = new Vue({
    el: '#app',
    data: {
        password: "",
        message: {
            helpBlock: "",
            groupClass: ""
        },
        loading: true,
    },
    methods: {
        submit: function () {
            queryStr = "password=" + encodeURIComponent(this.password);
            console.log(queryStr)
            postData('/api/admin/login/', queryStr, (data) => {
                if (data['status'] == '0') {
                    location.reload();
                } else if (data['status'] == '1') {
                    this.message = {
                        groupClass: 'has-error',
                        helpBlock: '登陆失败'
                    }
                } else {
                    console.log("服务器返回未知信息", data);
                }
            }, "login")
        }
    },
    watch: {
        password: function () {
            console.log(123);
            this.message = {
                helpBlock: "",
                groupClass: ""
            };
        }
    }
});