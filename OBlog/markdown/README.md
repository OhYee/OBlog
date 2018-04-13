# 重复造轮子 —— Python Markdown2HTML

- 支持多重奇怪格式列表
- 代码块（需要highlight.js），行内代码
- 带文字对齐的表格
- 任务列表（多选框）
- 以及基本的 Markdown 的语法

本意是用来将博客从 Hexo 移植到自己写的 Python 博客上
因此会有一些不是 Markdown 的操作，比如 Hexo 的 `{% raw %}{% endraw %}`  

有问题欢迎issue以及pull request
然而我大胆预言一波没人看


部分参考了 [SegmentFault/HyperDown](https://github.com/SegmentFault/HyperDown)
(其实因为看一半觉得太累就自己瞎写了)
----
# 思路
通过分割成行，分析是否有块状标记来选择是否进行块状区域渲染
对于一个块状区域，将其按照指定的函数进行渲染
对于非块状区域，将按照行内 Markdown 语法进行渲染