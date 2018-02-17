import os
import re
import json
Hexo_source_post_dir = r"D:\OneDrive\OneDrive - eclass inc\Workspace\Code\Blog\source\_posts"


def listFiles(root, relative=''):
    res = []
    List = os.listdir(root + relative)

    for file in List:
        filename = root + relative + '/' + file
        if os.path.isdir(filename):
            res += listFiles(root, relative + '/' + file)
        elif os.path.isfile(filename):
            res.append(relative + '/' + file)
        else:
            print("error at ", file)
    return res


if __name__ == '__main__':
    List = listFiles(Hexo_source_post_dir)
    posts = []
    idx = 0
    for path in List:
        print(path)
        f = open(Hexo_source_post_dir + path, 'r', encoding='utf-8')
        text = f.read()

        res = re.match(r'^---\n(.*?)\n---\n(.*)$', text, flags=re.S)
        raw = res.group(2)
        title = re.findall(r'.*title: (.+?)\n', res.group(1))[0]
        time = re.findall(r'^date: (.+?)$', res.group(1), re.M)[0]

        taglist = re.findall(r'^[ ]*-[ ]+(.+?)[ ]*$', res.group(1),  re.M)
        taglist += re.findall(r'^categories:[ ]+(.+?)[ ]*$',
                              res.group(1),  re.M)
        taglist += re.findall(r'^tags:[ ]+(.+?)[ ]*$', res.group(1),  re.M)
        tags = ','.join(taglist)
        taglist = set(taglist)


        post = {
            "url": path[1:-3],
            "title": title,
            "time": time,
            "tags": tags,
            "raw": raw,
        }

        posts.append(post)
        # print(post)
        # break
        # idx += 1
        # if idx >= 20:
        #     break

    f.close()
    f = open('./posts.json', 'w', encoding='utf-8')
    
    # f.write(str(posts))
    f.write(json.dumps(posts))
    f.close()
