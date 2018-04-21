$(document).ready(function() {
    $("ul li#admin-sidebar-7").toggleClass('active');
    vue.loading = true;
    parseJson(jsonData);
    vue.images = jsonData;
    vue.loading = false;
    vue.setPath('/');
});


function parseJson(data, dirname = '/') {
    for (var i = 0; i < data['file'].length; ++i) {
        var filename = data['file'][i];
        var relativePath = dirname + filename;
        var src = "/static/img" + relativePath;
        var absolutePath = window.location.host + src;
        data['file'][i] = {
            'dirname': dirname,
            'name': filename,
            'absolutePath': absolutePath,
            'relativePath': relativePath,
            'src': src,
            'exist': true
        };
    }
    for (var item in data['dir']) {
        parseJson(data['dir'][item], dirname + item + '/');
    }
}

var vue = new Vue({
    el: '#app',
    data: {
        path: "/",
        pathList: [],
        images: "",
        loading: true,
        nowList: [],
        alert: {
            class: "",
            content: "",
        }
    },
    methods: {
        submit: function(type, idx) {
            nowFile = this.nowList['file'][idx]
            var queryStr = "";
            var header = {}
            if (type == 'upload') {
                var formData = new FormData();
                formData.append('path', this.path);
                formData.append('file', $("input#updateFile")[0].files[0]);
                queryStr = formData;
                headers = {};
            } else if (type == 'rename') {
                queryStr = 'oldfilename=' + encodeURIComponent(nowFile.relativePath) + '&' + 'filename=' + encodeURIComponent(nowFile.dirname + nowFile.name);
                headers = { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" };
            } else {
                queryStr = 'filename=' + encodeURIComponent(nowFile.relativePath);
                headers = { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" };
            }
            console.log(queryStr)
            postData('/api/images/' + type + '/', queryStr, data => {
                console.log(data);
                if (data['status'] == '0') {
                    if (type == 'upload') {
                        this.alert = {
                            class: "alert-success",
                            title: "上传成功",
                            content: "文件名:" + data['filename']
                        };

                        var filename = data['filename'];
                        var relativePath = this.path + filename;
                        var src = "/static/img" + relativePath;
                        var absolutePath = window.location.host + src;

                        this.nowList['file'].push({
                            'dirname': this.path,
                            'name': filename,
                            'absolutePath': absolutePath,
                            'relativePath': relativePath,
                            'src': src,
                            'exist': true
                        });
                    } else if (type == "rename") {
                        this.alert = {
                            class: "alert-success",
                            title: "重命名成功",
                            content: "文件名:" + nowFile['name']
                        };

                        var filename = nowFile['name'];
                        var relativePath = this.path + filename;
                        var src = "/static/img" + relativePath;
                        var absolutePath = window.location.host + src;

                        this.nowList['file'][idx] = {
                            'dirname': this.path,
                            'name': filename,
                            'absolutePath': absolutePath,
                            'relativePath': relativePath,
                            'src': src,
                            'exist': true
                        };
                    } else {
                        this.alert = {
                            class: "alert-success",
                            title: "删除成功",
                            content: ""
                        };
                        this.nowList['file'][idx]['exist'] = false;
                    }
                } else if (data['status'] == '1') {
                    if (type == 'upload') {
                        this.alert = {
                            class: "alert-warning",
                            title: "上传失败",
                            content: "文件已存在或文件名不合法"
                        };
                    } else if (type == "rename") {
                        this.alert = {
                            class: "alert-warning",
                            title: "重命名失败",
                            content: "文件已存在或文件名不合法"
                        };
                    } else {
                        this.alert = {
                            class: "alert-warning",
                            title: "删除失败",
                            content: ""
                        };
                    }
                } else {
                    this.alert = {
                        class: "alert-error",
                        title: "警告",
                        content: "服务器返回未知信息"
                    };
                }
                this.$set(this.nowList, idx, this.nowList[idx]);
                this.$nextTick(window.location.href = "#alert");
            }, type + idx, headers);
        },
        setPath: function(path) {
            this.loading = true;
            this.path = path;
            this.pathList = this.path.substr(1).split("/")
            this.pathList.pop()
            if (this.pathList[0] == '')
                this.pathList = [];
            this.nowList = this.images;
            var temp = '/'
            for (var i = 0; i < this.pathList.length; ++i) {
                var dirname = this.pathList[i];
                temp += dirname + '/';
                this.pathList[i] = {
                    'dirname': dirname,
                    'path': temp,
                }
                this.nowList = this.nowList['dir'][dirname];
            }
            this.pathList.splice(0, 0, {
                'dirname': 'root',
                'path': '/',
            });
            this.$nextTick(function () {
                this.loading = false;
            });
        },
        close: function() {
            this.alert = {
                class: "",
                title: "",
                content: ""
            };
        }
    },
    watch: {

    },
});