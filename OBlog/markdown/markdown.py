import time
import hashlib
import re

SHOWLOG = False


def LOG(title, text):
    if SHOWLOG == True:
        print('##########\n' + title + '\n' + str(text) + '\n')
    pass


class Markdown:
    __holders = {}
    __uniqid = 0
    __id = 0
    __lineGrammarList = []
    __blockGrammarList = []

    def __init__(self):
        self.__lineGrammarList = [
            # code
            [r'(?<!\\)`(.+?)`',
                r'<code>\1</code>'],
            # image
            [r'(?<!\\)\!\[(.*?)\]\((.*?)\)',
                r'<a href="\2" alt="\1" data-lightbox="\1-\2" data-title="\1"><img class="img-responsive" src="\2" alt="\1"></a>'],
            # link
            [r'(?<!\\)\[(.*?)\]\((.*?)\)',
                r'<a href="\2">\1</a>'],
            # auto link
            [r'<{0,1}((?:ht|f)t(?:p|ps)://[\w\-\.\_,@?^=%&:~\+#\/]+)>{0,1}',
                r'<a href="\1">\1</a>'],
            # strong
            [r'(?<!\\)[_\*]{2}(.*?)[_\*]{2}',
                r'<strong>\1</strong>'],
            # em
            [r'(?<!\\)[_\*](.*?)[_\*]',
                r'<em>\1</em>'],
            # title
            [r'(?<!\\)(?<!#)(#+) (.*)\s*$',
                lambda res: r'<h' + str(len(res[1])) + r'>' + res[2] + '</h' + str(len(res[1])) + '>'],
            # checkbox
            [r'(?<!\\)\[([xX ])\] (.*?)$',
                lambda res: r'<input type="checkbox" disabled="disabled"' + (r' checked="checked"' if res[1] != ' ' else '') + r'>' + res[2]],
            [r'^-{3,}$', '<hr>'],
            # escape
            #[r'(?:\\(.))',
            #    r'\1'],
        ]

        self.__blockGrammarList = [
            [r'^[ ]*```(.*?)$', r'(?=^|[ ]+)```$',
             self.__parseCodeBlock, True],
            [r'^>+ .*$', r'', self.__parseQuoteBlock, False],
            [r'^\|(?:.*?\|)+$', r'', self.__parseTableBlock, False],
            [r'^[ ]*[\-\*] .*?$', r'^$', self.__parseULBlock, True],
            [r'^[ ]*[0-9]+\. .*?$', r'^$', self.__parseOLBlock, True],
            [r'\{\% raw \%\}', r'\{\% endraw \%\}',
                self.__parseRawTagBlock, True],
            [r'\{\% fold .*\%\}', r'\{\% endfold \%\}',
                self.__parseFoldBlock, True],
            [r'\{\% cq \%\}', r'\{\% endcq \%\}',
                self.__parseCenterQuoteBlock, True],
            [r'\{\% blockquote \%\}', r'\{\% endblockquote \%\}',
                self.__parseCenterQuoteBlock, True],
        ]

    def makeHtml(self, text, allowHtml):
        '''
        将markdown转换成html
        '''
        self.__holders = {}
        self.__uniqid = hashlib.md5(str(time.time()).encode()).hexdigest()
        self.__id = 0

        if allowHtml == False:
            text = self.__escapeHtml(text)

        text = self.__initText(text)
        html = self.__parse(text)

        return html

    def __initText(self, text):
        '''
        转义\t \r
        '''
        text = text.replace('\t', '    ')
        text = text.replace('\r', '')
        return text

    def __parse(self, text):
        lines = text.split('\n')
        html = self.__parseBlock(lines)
        return html

    def __parseBlock(self, lines):
        '''
        渲染块区域
        '''
        LOG("BLOCK", lines)
        typeid = -1
        beginPos = 0
        html = ''
        for row in range(len(lines)):
            # print(row, lines[row])
            if typeid != -1:
                # in block
                if self.__blockGrammarList[typeid][3] == True:
                    if re.match(self.__blockGrammarList[typeid][1], lines[row]) != None:
                        # end block
                        html += self.__blockGrammarList[typeid][2](
                            lines[beginPos:row + 1]) + r'<br>'
                        typeid = -1
                        continue
                else:
                    if re.match(self.__blockGrammarList[typeid][0], lines[row]) == None:
                        # out of block
                        html += self.__blockGrammarList[typeid][2](
                            lines[beginPos:row]) + r'<br>'
                        typeid = -1

            if typeid == -1:
                # not in block
                for blockid in range(len(self.__blockGrammarList)):
                    if re.match(self.__blockGrammarList[blockid][0], lines[row]) != None:
                        # begin block
                        typeid = blockid
                        beginPos = row
                        break
                if typeid == -1:
                    # render this line
                    html += self.__parseInline(lines[row]) + r'<br>'

            # print("\t",typeid)

        if typeid != -1:
            # no end block
            html += self.__blockGrammarList[typeid][2](
                lines[beginPos:len(lines)]) + r'<br>'

        # 去除多余的换行符
        if html[-4:] == r'<br>':
            html = html[0: -4]

        return html

    def __parseRawTagBlock(self, lines):
        return self.__parseRawBlock(lines[1:-1])

    def __parseRawBlock(self, lines):
        '''
        不转义
        '''
        html = ''
        for line in lines:
            html += line + '\n'
        return html

    def __parseCodeBlock(self, lines):
        '''
        代码块转义
        '''
        res = re.match(r'^[ ]*```[ ]*(.+?)(?: .*)*$', lines[0])

        language = ' class="%s"' % res.group(1) if res else ''
        html = r'<pre class="codeblock"><codeblock' + language + '>' +\
            self.__parseRawBlock(
                self.__escapeHtml(
                    self.__deleteSpace(lines[1:-1])
                )
            ) + r'</codeblock></pre>'
        return html

    def __deleteSpace(self, lines):
        '''
        删除相同数目的空格，保证最前面的前面没有空格
        '''
        Minpos = 9999999999
        for line in lines:
            Minpos = min(Minpos, max(0, self.__findFirstChar(line)))
            # __findFirstChar() 可能会返回-1（空行）,把最小值限定为0

        lines = [line[Minpos:] for line in lines]
        return lines

    def __parseQuoteBlock(self, lines):
        '''
        引用块转义
        '''
        newlines = [re.sub(r'^[ ]+(.*?)$', r'\1', line[1:]) for line in lines]
        # print(lines, "\n", newlines)
        html = r'<blockquote>' + self.__parseBlock(newlines) + r'</blockquote>'
        return html

    def __parseCenterQuoteBlock(self, lines):
        '''
        引用块转义
        '''
        # print(lines, "\n", newlines)
        html = r'<blockquote class="center">' + \
            self.__parseBlock(lines[1:-1]) + r'</blockquote>'
        return html

    def __parseFoldBlock(self, lines):
        res = re.match(r'\{\% fold (.*?) \%\}[ ]*(.*)$', lines[0])
        matchList = res.groups() if res else ['', '']
        text = res.group(1) if matchList[0] != '' else '点击显/隐区域'
        if matchList[1] != '':
            lines.insert(1, matchList[1])

        html = '<div class="fold_parent"><div class="fold_hider"><div class="fold_close hider_title">' + \
            text + '</div></div><div class="fold">\n' + \
            self.__parseBlock(lines[1:-1]) + '\n</div></div>'
        return html

    def __findFirstChar(self, line):
        pos = -1
        for i in range(len(line)):
            if line[i] != ' ':
                pos = i
                break
        return pos

    def __parseListBlock(self, lines, ListType, RE1, RE2):
        # 删除空行
        for i in range(lines.count(r'')):
            lines.remove(r'')

        TagBegin = '<' + ListType + ' class="browser-default">'
        TagEnd = '</' + ListType + '>'

        List = ['    ' for i in lines]
        minpos = 9999999

        # 删除多余的空格
        for idx, line in enumerate(lines):
            pos = self.__findFirstChar(line)
            if re.match(RE1, line) != None and pos < minpos:
                minpos = pos
            List[idx] = line[min(pos, minpos):]
            # print(idx, '"' + line + '"', pos, minpos, '"' + List[idx] + '"')
        LOG("List", List)
        LOG("minpos", minpos)

        beginpos = -1
        html = r''
        hasli = False
        for idx, line in enumerate(List):
            if re.match(RE2, line) != None:
                LOG("match", line)
                if beginpos != -1:
                    html += r'<li>' + \
                        self.__parseBlock(
                            List[beginpos: idx]) + r'</li>'
                beginpos = idx
                List[idx] = re.sub(RE2, r'\1', line)
                hasli = True
                LOG("New beginpos", beginpos)
            elif line[0] != ' ':
                LOG("don't match", line)
                if beginpos != -1:
                    html += r'<li>' + \
                        self.__parseBlock(
                            List[beginpos: idx]) + r'</li>'
                    beginpos = -1
                html += self.__parseInline(line) + '<br>'
        # 结束最后一个li
        if beginpos != -1:
            html += r'<li>' + \
                self.__parseBlock(
                    List[beginpos: len(List)]) + r'</li>'

        # 增加标签
        if True or hasli:
            html = TagBegin + html + TagEnd

        return html

    def __parseULBlock(self, lines):
        html = self.__parseListBlock(
            lines, 'ul', r'^[ ]*[\-\*] (.*?)$', r'^[\-\*] (.*?)$')
        # print(lines, '\n', html)
        return html

    def __parseOLBlock(self, lines):
        return self.__parseListBlock(lines, 'ol', r'^[ ]*[0-9]+\. (.*?)$', r'^[0-9]+\. (.*?)$')

    def __parseTableBlock(self, lines):
        '''
        表格块转义
        '''

        Table = [list(line.split('|'))[1:-1] for line in lines]
        col = len(Table[0])
        row = len(lines)

        hasAlign = False
        align = ['' for i in range(col)]

        for r in range(row):
            while len(Table[r]) < col:
                Table[r].append('')

        LOG("parseTableBlock", Table)

        if row > 1:
            for i in range(col):
                if re.match("^\:\-+$", Table[1][i]) != None:
                    align[i] = ' class="left" '
                    hasAlign = True
                    continue
                if re.match("^\:\-+\:$", Table[1][i]) != None:
                    align[i] = ' class="center" '
                    hasAlign = True
                    continue
                if re.match("^\-+\:$", Table[1][i]) != None:
                    align[i] = ' class="right" '
                    hasAlign = True
                    continue
            if hasAlign == True:
                Table.remove(Table[1])
                row -= 1

        # print(row, col)
        # print(align)
        # for i in range(row):
        #     print(Table[i])

        html = r''
        for i in range(row):
            html += r'<tr>'

            for j in range(col):
                html += r'<td' + align[j] + r'>' + \
                    self.__parseInline(Table[i][j]) + r'</td>'

            html += r'</tr>'

        html = r'<table class="responsive-table highlight striped">' + html + r'</table>'
        return html

    def __makeHolder(self, text):
        '''
        防止被重复转义
        '''
        key = '|\r' + str(self.__uniqid) + str(self.__id) + '\r|'
        self.__id += 1
        self.__holders[key] = text

        return key

    def __releaseHolder(self, text):
        '''
        转义回去
        '''
        for key in self.__holders.keys():
            text = text.replace(key, self.__holders[key])
        self.__holders = {}
        LOG("release", text.replace('\r', '\\r'))
        return text

    def __escapeHtml(self, text):
        if type(text) == list:
            for i in range(len(text)):
                text[i] = text[i].replace(
                    '<', '&lt;').replace('>', '&gt;')
        elif type(text) == str:
            text = text.replace('<', '&lt;').replace('>', '&gt;')
        return text

    def __encodeHtmlChars(self, text, space=True):
        '''
        转义HTML的特殊字符
        '''
        text = text.replace('&', "&amp;")
        text = text.replace('"', "&quot;")
        # text = text.replace('<', "&lt;")
        # text = text.replace('>', "&gt;")
        if space == True:
            text = text.replace(' ', "&nbsp;")
        return text

    def __formatText(self, _format, _matches):
        '''
        将对应的语句按照指定格式输出
        '''
        LOG("formatText", (_format, _matches.groups()))
        _text = ""
        res = [self.__escapeHtml(self.__encodeHtmlChars(match))
               for match in _matches.groups()]
        res.insert(0, "")
        if type(_format) == str:
            _text = _format
            result = re.findall(r'\\([0-9]+)', _text)
            for i in set(result):
                _text = _text.replace('\\' + i, res[int(i)])
        else:
            _text = _format(res)
        return _text

    def __parseInline(self, text):
        '''
        渲染每一行
        '''
        LOG("parseInline", text)
        for grammar in self.__lineGrammarList:
            text = re.sub(grammar[0], lambda matches:
                          self.__makeHolder(
                self.__formatText(grammar[1], matches)
            ), text, flags=re.M)
        text = re.sub(r'\\(.)', r'\1', text)

        LOG("beforeRelease", text.replace('\r', '\\r'))
        text = self.__releaseHolder(text)
        # 删除前面多余的空格
        text = text[self.__findFirstChar(text):]
        return text


def renderMarkdown(raw, showlog=False, allowHtml=True):
    global SHOWLOG
    SHOWLOG = showlog
    return Markdown().makeHtml(raw, allowHtml)
