import shutil
import random
import re
import time
import requests
import os

PATTERN_BODY = re.compile(r'(?<=<h1 title=").*(?=" class="video-title">)')
anime_title = re.compile(r'(?<= "name": ").*(?=")')
title_part = re.compile(
    r'(?<={"cid").*?(?=vid":"","weblink":"","dimension":{)')
anime_tile_part = re.compile(r'(?<=","vid":"","longTitle":).*?(?=,"badge":)')

def get_tile(str1):
    resp = requests.get(
        url=f'https://www.bilibili.com/video/av' + str1 + '?p=' + '',
        # 地址
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.97 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,image/webp,image/apng,*/*;'
                      'q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        },
        # 请求头
    )
    time.sleep(random.randint(1, 3))
    return str(PATTERN_BODY.findall(resp.text)[0])


def get_anime_tile(str1):
    str1 = str1.replace('s_', 'ss')
    resp = requests.get(
        url=f'https://www.bilibili.com/bangumi/play/' + str1, 
        # 地址
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.97 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,image/webp,image/apng,*/*;'
                      'q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        },
        # 请求头
    )
    time.sleep(random.randint(1, 3))
    return str(anime_title.findall(resp.text)[0])


def dir_rename():
    path = './download'
    list1 = os.listdir(path)
    for i in list1:
        if 's_' in i:
            os.rename(path+'/'+i, path+'/'+get_anime_tile(i))
        else:
            os.rename(path+'/'+i, path+'/'+get_tile(i))


def find_file_and_trans():
    for root, dirs, files in os.walk("."):
        for file in files:
            str1 = os.path.join(root, file)
            if '0.blv' in str1:
                transcoding(str1)
            else:
                if 'audio.m4s' in str1:
                    unite_video(str1)


def transcoding(str1):
    for s in os.listdir('./download'):
        if s in str1:
            for s1 in os.listdir('./download/' + s):
                if s1 in str1:
                    os.system(
                        'ffmpeg -hwaccel cuvid -c:v h264_cuvid -i ' + str1 + ' -c:v h264_nvenc -y ./download/' + s + '/' + s1 + '.mp4')


def unite_video(str1):
    for s in os.listdir('./download'):
        if s in str1:
            for s1 in os.listdir('./download/' + s):
                if s1 in str1:
                    os.system(
                        'ffmpeg -hwaccel cuvid -c:v h264_cuvid -i ' + str1 + ' -c:v h264_nvenc -y ./download/' + s + '/' + s1 + '.mp4')


def rm_dir():
    path = './download'
    for file in os.listdir(path):
        for in_file in os.listdir(path + '/' + file):
            print(in_file)
            if bool(1 - ('.mp4' in in_file)):
                if os.path.isdir(path + '/' + file + '/' + in_file):
                    shutil.rmtree(path + '/' + file + '/' + in_file)
                else:
                    os.remove(path + '/' + file + '/' + in_file)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def get_anime_tile_part(id1):
    resp = requests.get(
        url=f'https://www.bilibili.com/bangumi/play/ep' + id1,
        # 地址
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.97 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,image/webp,image/apng,*/*;'
                      'q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        },
        # 请求头
    )
    time.sleep(random.randint(1, 3))
    res = ''
    for f in anime_tile_part.findall(resp.text):
        if id1 in f:
            fn = re.compile(r'(?<=").*(?=","hasNext":true,"i":)').findall(f)
            if fn != '':
                res = fn
                break
    return res


def get_tile_part(id1, av_id):
    id1 = id1.replace('c_', '')
    resp = requests.get(
        url=f'https://www.bilibili.com/video/av' + av_id,
        # 地址
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.97 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,image/webp,image/apng,*/*;'
                      'q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        },
        # 请求头
    )
    time.sleep(random.randint(1, 3))
    res = ''
    for f in title_part.findall(resp.text):
        if id1 in str(f):
            fn = re.compile(
                r'(?<="from":"vupload","part":").*(?=","duration")').findall(f)[0]
            if fn != '':
                res = fn
                break
    return res


def rename_file():
    file = './download'
    for li in os.listdir(file):
        for m in os.listdir(file + '/' + li):
            m = m.replace('.mp4', '')
            if 'c_' in m:
                name = get_tile_part(m, li)
                if name != '':
                    name = name.replace('\\', ' ')
                    name = name.replace('/', ' ')
                    os.rename(file + '/' + li + '/' + m + '.mp4',
                              file + '/' + li + '/' + name + '.mp4')
            else:
                if is_number(m):
                    name = get_anime_tile_part(m)
                    for n in name:
                        if n != '':
                            n = n.replace('\\u002F', ' ')
                            n = n.replace('\\', ' ')
                            n = n.replace('/', ' ')
                            n.encode(encoding="utf-8", errors="ignore")
                            os.rename(file + '/' + li + '/' + m + '.mp4',
                                      file + '/' + li + '/' + n + '.mp4')


def main():
    find_file_and_trans()  # 转码完成
    rm_dir()  # 除了已经转码过的视频全部删除
    rename_file()  # 改文件名字
    dir_rename()  # 文件夹改名字


if __name__ == '__main__':
    main()
