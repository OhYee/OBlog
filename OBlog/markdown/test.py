from markdown import renderMarkdown 

if __name__ == "__main__":
    raw = r'''
`123`
`#include <cstdio>`

![图片](/123/123_123/123_/123.jpg)

[链接1](/123_444)

https://www.123.com/

http://www.123.com/

<http://www.123.com>


**加粗**
_斜体_
__加粗__
# 一级标题
## 二级标题
### 三级标题

[ ] 123
[x] 123
\[x] 123
[] 123

```cpp
#include <cstdio>
int main(){
    printf("123");
    return 0;
}
```


    - 1
            1.xxxxx
- 2
    2.xxxx
    - 2.1
    - 2.2
        - 2.2.1
            2.2.1.xxxxxx
       - 2.2.2
    - 2.3
    - 2.4
    **2.xxxxx**
- 3

   1. 1
2. 2
3. 3
  1. 1.1
      1.1.sxxxx
  2. 2.2
4. 4

|first col|second col|third col|
|:--|:--:|--:|
|1,1|1,2|1,3|
|2,1|**2,2**|2,3|

> 引用
>> 引用引用
>> 引用引用
>>> 引用引用引用
> 引用
> `code`
> **引用内的加粗**

<input type='text'/>

&lt;

'''

if __name__=='__main__':
    markdown = renderMarkdown(raw,showlog=True,allowHtml=True)
    print(markdown)
    f = open("./md.html", "w",encoding='utf-8')
    f.write(markdown)
    f.close()