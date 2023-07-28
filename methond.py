import requests
import wbi
import qrcode
import requests
import time
import io


class Method:
    def __init__(self,headers):
        self.sub_key = None
        self.img_key = None
        self.cookies = None
        self.headers = headers

    # 获取并显示二维码
    def get_qr_key(self):
        # 给出二维码
        res = requests.get('https://passport.bilibili.com/x/passport-login/web/qrcode/generate', headers=self.headers)
        # 生成二维码
        print(res.json())
        qr = qrcode.QRCode()
        qr.add_data(res.json()['data']['url'])
        f = io.StringIO()
        qr.print_ascii(out=f)
        f.seek(0)
        print(f.read())
        return res.json()['data']['qrcode_key']

    # 完成登录
    def login(self):
        key = self.get_qr_key()
        kw = {'qrcode_key': key}
        input('press enter to ensure scan successful')
        res = requests.get('https://passport.bilibili.com/x/passport-login/web/qrcode/poll', params=kw,
                           headers=self.headers)
        if res.json()['data']['code'] != 0:
            print('some thing wrong')
            time.sleep(10)
            return self.login()
        else:
            return res

    # 获取cookie
    def get_cookie(self):
        cookies = dict()
        for k, v in self.login().cookies.items():
            cookies[k] = v
        self.cookies = cookies

    def get_wbi(self):
        self.img_key, self.sub_key = wbi.getWbiKeys(self.cookies)

    def get_index_recommend(self, fresh_type=3, version=0, ps=10, fresh_idx=1, fresh_idx_1h=1):
        kw = {'fresh_type': fresh_type, 'version': version, 'ps': ps, "fresh_idx": fresh_idx,
              'fresh_idx_1h': fresh_idx_1h}
        return requests.get('https://api.bilibili.com/x/web-interface/index/top/rcmd', cookies=self.cookies,
                            headers=self.headers,
                            params=kw)

    def get_related_recommend(self, bvid: str):
        kw = {"bvid": bvid}
        return requests.get('https://api.bilibili.com/x/web-interface/archive/related', cookies=self.cookies,
                            headers=self.headers,
                            params=kw)

    def get_video_comments(self, oid: int, sort: int = 1, nohot=0, ps=20, pn=1):
        kw = {'type': 1, 'oid': oid, 'sort': sort, 'nohot': nohot, 'ps': ps, 'pn': pn}
        return requests.get('https://api.bilibili.com/x/v2/reply', cookies=self.cookies, headers=self.headers,
                            params=kw)


