$(document).ready(function () {
    $("ul li#admin-sidebar-7").toggleClass('active');
    vue.loading = true;
    vue.images = jsonData;
    vue.loading = false;
    vue.setPath('/');
});

var vue = new Vue({
    el: '#app',
    data: {
        path: "/",
        pathList: [],
        images: "",
        loading: true,
        nowList: [],
    },
    methods: {
        setPath: function (path) {
            this.path = path;

            this.pathList = this.path.substr(1).split("/")
            this.pathList.pop()
            console.log(this.pathList)

            if (this.pathList[0] == '')
                this.pathList = [];
            this.nowList = this.images;


            console.log(this.pathList)
            var temp = '/'
            for (var i = 0; i < this.pathList.length; ++i) {
                var dirname = this.pathList[i];
                temp += dirname + '/';

                console.log(i, dirname, temp)


                this.pathList[i] = {
                    'dirname': dirname,
                    'path': temp,
                }
                this.nowList = this.nowList['dir'][dirname];
            }

            this.pathList.splice(0, 0, {
                'dirname': 'root',
                'path': '/',
            })
            console.log(this.pathList, this.nowList);
        }
    },
    watch: {

    },
});