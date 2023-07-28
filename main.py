import random
import time
import methond
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/54.0.2840.99 Safari/537.36"}


def get_comments():
    # with open('keyword.json', 'r', encoding='UTF-8') as f:
    #     keywords = json.loads(f.read())
    with open('repeat.json', 'r', encoding='UTF-8') as f:
        repeat_msg = dict(json.loads(f.read()))
    web = methond.Method(headers)
    web.get_cookie()
    # print(web.get_index_recommend(fresh_idx=1).json())

    res = list()

    for i in range(100):
        print('正在爬取第{}页'.format(i))
        rec = web.get_index_recommend(fresh_idx=i).json()
        time.sleep(random.randrange(2, 10) / 10)
        for n in rec['data']['item']:
            print('正在爬取{}'.format(n['title']))
            video = {
                'uname': n['owner']['name'],
                'title': n['title'],
                'id': n['id'],
                'bvid': n['bvid'],
                'comment': []
            }
            if web.get_video_comments(oid=n['id']).json()['data']['replies'] is not None:
                for rep in web.get_video_comments(oid=n['id']).json()['data']['replies']:

                    comment = {
                        'uname': rep['member']['uname'],
                        'sex': rep['member']['sex'],
                        'like': rep['like'],
                        'level': rep['member']['level_info']['current_level'],
                        'message': rep['content']['message'],
                        'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(rep['ctime']))
                    }
                    repeat_msg[rep['content']['message']] = repeat_msg.get(rep['content']['message'], 0) + 1
                    if 'location' in rep['reply_control'].keys():
                        comment['location'] = rep['reply_control']['location']
                    else:
                        comment['location'] = None
                    video['comment'].append(comment)
            res.append(video)
    print(res)
    with open('data.json', 'w', encoding='UTF-8') as f:
        # current = json.loads(f.read())
        f.write(json.dumps(res, ensure_ascii=False, indent=4, sort_keys=False))
    with open('repeat.json', 'w', encoding='UTF-8') as f:
        f.write(json.dumps(sorted(repeat_msg.items(), key=lambda item: item[1], reverse=True), ensure_ascii=False,
                           indent=4))
        # print(n['title'], ':', n['id'])
        # rep = web.get_video_comments(oid=n['id']).json()['data']['replies'][0]
        # print(json.dumps(rep,indent=4,ensure_ascii=False,sort_keys=False))
        # for rep in web.get_video_comments(oid=n['id']).json()['data']['replies']:
        #     print(rep['member']["uname"], ' ', rep['member']['sex'], ' ', ':', rep["content"]["message"], ';like', rep['like'],rep["reply_control"]["location"])

# TODO 搜素视频并获取评论

if __name__ == '__main__':
    get_comments()
