/* 加载完成后自动执行 */
$(document).ready(function() {
    // 移动端侧边栏
    // $(".button-collapse").sideNav();

    // 代码高亮
    $('pre codeblock').each(function(i, block) {
        hljs.highlightBlock(block);
    });

    autoHeight();
    //showMessage();

    initUnfold($('.unfold-wrap'));
    initFold();
});

$(document).resize(autoHeight());

// 代码高亮配置
hljs.configure({
    useBR: false
});


/* 自适应高度 */
function autoHeight() {
    $("main").attr("style", "min-height:" + (document.documentElement.clientHeight - $("header").height() - $("footer").height() - 40) + "px;");
}

window.onload = function() {
    autoHeight();
};
window.onresize = function() {
    autoHeight();
};

/* Get访问 */
var _getRequestIndex = {};

function getData(url, solve, id) {
    if (_getRequestIndex[id])
        _getRequestIndex[id] = _getRequestIndex[id] + 1;
    else
        _getRequestIndex[id] = 0;

    var responseIndex = _getRequestIndex[id];

    fetch(url, {
        method: 'get',
        credentials: 'include',
        headers: {
            "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
    }).then(
        response => response.json()
    ).then(
        data => {
            if (_getRequestIndex[id] == responseIndex) {
                delete _getRequestIndex[id];
                return solve(data);
            } else {
                console.log("throw data");
            }
        }
    ).catch(e => console.log("getData error:", e));
}

/* Post访问 */
var _postRequestIndex = {};

function postData(url, data, solve, id,
    headers = { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" }) {
    if (_postRequestIndex[id])
        _postRequestIndex[id] = _postRequestIndex[id] + 1;
    else
        _postRequestIndex[id] = 0;

    var responseIndex = _postRequestIndex[id];
    fetch(url, {
        method: 'post',
        credentials: 'include',
        headers: headers,
        body: data
    }).then(
        response => response.json()
    ).then(
        data => {
            if (_postRequestIndex[id] == responseIndex) {
                delete _postRequestIndex[id];
                return solve(data);
            } else {
                console.log("throw data");
            }
        }
    ).catch(e => console.log('postData error:', e));
}

/* 忽略打字过程中的查询 */
var _timer = {}

function waitUntilLast(id, fun, time) {
    if (_timer[id]) {
        clearTimeout(_timer[id]);
        delete _timer[id];
    }
    return _timer[id] = setTimeout(() => {
        fun();
        delete _timer[id];
    }, time)
}


/* 按照首字母排序，英语在前，汉语在后 */
function sortTagsByPinYin(tags) {
    if (!String.prototype.localeCompare)
        return tags.sort();

    var letters = "*abcdefghjklmnopqrstwxyz".split('');
    var zh = "阿八嚓哒妸发旮哈讥咔垃痳拏噢妑七呥扨它穵夕丫帀".split('');

    var newTags = [];
    $.each(letters, function(i) {
        var curr1 = [],
            curr2 = [];
        var thisChar = this;
        $.each(tags, function() {
            if (this.chinese && this.chinese.length > 0) {
                var firstChar = this.chinese[0].toLowerCase()
                if (firstChar >= 'a' && firstChar <= 'z') {
                    if (firstChar == thisChar) {
                        curr1.push(this);
                    }
                } else if ((!zh[i - 1] || zh[i - 1].localeCompare(this.chinese, 'zh') <= 0) && this.chinese.localeCompare(zh[i], 'zh') == -1) {
                    curr2.push(this);
                }
            }
        });
        curr1.sort();
        curr2.sort((a, b) => a.chinese.localeCompare(b.chinese, 'zh'));
        newTags.push({
            char: thisChar[0],
            tags: curr1.concat(curr2)
        });
    });
    return newTags;
}

/* toJSON */
function toJSON(text) {
    text = text.replace(/\\/g, "\\\\").replace(/\\b/g, "\\b").replace(/\f/g, "\\f").replace(/\n/g, "\\n").replace(/\r/g, "\\r").replace(/\t/g, "\\t");
    console.log(text)
    return JSON.parse(text)
}



function showMessage() {
    $("body").prepend("<div id='attitionMessage' class='center pink darken-3 white-text'><a class='white-text right' href='javascript:removeMessage();'><i class='material-icons left'>close</i></a>博客从Hexo迁移到<a class='blue-text text-lighten-2' href='https://github.com/OhYee/OBlog'>自己写的系统</a>，若有问题，请反馈到<a class='blue-text text-lighten-2' href='mailto:oyohyee@oyohyee.com'>oyohyee@oyohyee.com</a>，<a class='blue-text text-lighten-2' href='/discuss'>评论区</a>、<a  class='blue-text text-lighten-2' href='https://github.com/OhYee/OBlog/issues'>GitHub</a><br>如果无法正常渲染，访问老站<a class='blue-text text-lighten-2' href='http://blog.oyohyee.com/'>http://blog.oyohyee.com</a></div>");
}

function removeMessage() {
    $('#attitionMessage').remove();
}

// 初始化查看全部
function initUnfold(e) {
    e.css('maxHeight', "");
    if (e.children('.content').height() > e.height()) {
        var tips = $(e).attr('tips');
        if (!tips) tips = '显示更多';
        $(e).append('<div class="unfold-field"><div class="unflod-field_mask"></div><div class="unfold-field_text"><span>' + tips + '</span></div></div>')
        e.children('.unfold-field').css("display", "block");
    }
    e.css('visibility', "visible");

    e.children('.unfold-field').click(() => {
        e.css('maxHeight', "100%");
        e.children('.unfold-field').remove();
    });
}

// 初始化折叠
function initFold() {
    $(document).on('click', '.fold_hider', function() {
        $('>.fold', this.parentNode).slideToggle();
        $('>:first', this).toggleClass('fold_open');
    });
    //默认情况下折叠
    $("div.fold").css("display", "none");
}

// 统计
var _hmt = _hmt || [];
(function() {
    var hm = document.createElement("script");
    hm.src = "https://hm.baidu.com/hm.js?c3c4a93be88257973d97af02f735ed4e";
    var s = document.getElementsByTagName("script")[0];
    s.parentNode.insertBefore(hm, s);
})();

// 自动推送
(function() {
    var bp = document.createElement('script');
    var curProtocol = window.location.protocol.split(':')[0];
    if (curProtocol === 'https') {
        bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';
    } else {
        bp.src = 'http://push.zhanzhang.baidu.com/push.js';
    }
    var s = document.getElementsByTagName("script")[0];
    s.parentNode.insertBefore(bp, s);
})();



/* 按照文章数排序 */
var sortTagsByNumber = tags => tags.sort((a, b) => parseInt(b.cnt) - parseInt(a.cnt));

/* 格式化输出时间 */
Date.prototype.Format = function(fmt = "yyyy-MM-dd HH:mm:ss") {
    var o = {
        "M+": this.getMonth() + 1,
        "d+": this.getDate(),
        "H+": this.getHours(),
        "m+": this.getMinutes(),
        "s+": this.getSeconds(),
        "q+": Math.floor((this.getMonth() + 3) / 3),
        "S": this.getMilliseconds()
    };
    var year = this.getFullYear();
    var yearstr = year + '';
    yearstr = yearstr.length >= 4 ? yearstr : '0000'.substr(0, 4 - yearstr.length) + yearstr;

    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (yearstr + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}

/* Vue 组件 */
Vue.component('alert', {
    template: '<div class="alert alert-dismissible" role="alert" v-if="alert.class" :class="alert.class"><button type="button" class="close" aria-label="Close" @click="close"><span aria-hidden="true">&times;</span></button><strong v-text="alert.title"></strong>&nbsp;<span v-text="alert.content"></span></div>',
    props: ['alert'],
    methods: {
        close: function() {
            this.$emit('close')
        }
    }
})