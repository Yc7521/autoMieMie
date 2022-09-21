import argparse
import base64
import json
import random
import struct
import time
import httpx
import config

http = httpx.Client()


def api_get(url: str, header={}, log: bool = True):
    err_time = 0
    err_msg = ""
    while err_time < 5:
        try:
            response = http.get(url, headers=header).json()
            if log:
                print(
                    f"运行时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}: {response}")
            return response
        except Exception as e:
            err_time += 1
            err_msg += f"err-{err_time}: {e}\n"
            continue
    if log:
        print(
            f"运行时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}: 请求失败")
    raise Exception(f"请求失败:\n{err_msg}")


def old_api(url="/sheep/v1/game/game_over", header={}, args={}):
    api_get(
        f"https://cat-match.easygame2021.com{url}?rank_score={args.rank_score}&rank_state={args.rank_state}&rank_time={args.rank_time}&rank_role={args.rank_role}&skin={args.skin}&t={args.t}",
        header)


def temp_api(header, args, log=True):
    err_time = 0
    err_msg = ""
    while err_time < 5:
        try:
            response = http.post(
                f"https://cat-match.easygame2021.com/sheep/v1/game/game_over_ex",
                headers=header,
                content=json.dumps({
                    "rank_score": args.rank_score,
                    "rank_state": args.rank_state,
                    "rank_time": args.rank_time,
                    "rank_role": args.rank_role,
                    "skin": args.skin,
                    "MatchPlayInfo": config.steps
                })
            ).json()
            if log:
                print(
                    f"运行时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}: {response}")
            return
        except Exception as e:
            err_time += 1
            err_msg += f"err-{err_time}: {e}\n"
            continue
    if log:
        print(
            f"运行时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}: 请求失败")
    raise Exception(f"请求失败:\n{err_msg}")


def map_api(header={}, log: bool = True):
    map = api_get(
        f"https://cat-match.easygame2021.com/sheep/v1/game/map_info_ex?matchType=3", header, False)
    map = f"https://cat-match-static.easygame2021.com/maps/{map['data']['map_md5'][1]}.txt"
    if log:
        print(map)
    header = dict(header)
    header['Host'] = "cat-match-static.easygame2021.com"
    map = api_get(map, header, log)['levelData']
    count = sum([len(i) for i in list(map.values())])
    # need to gen a step list (but i don't now how to impl)
    return count


def multi_byte_int(number: int):
    # <128      : 1
    # <16384    : 2
    # <2097152  : 3
    # <268435456: 4
    # else      : 5
    if number < 128:
        return struct.pack('B', number)
    elif number < 16384:
        return struct.pack('BB', number & 127 | 128, number >> 7)
    elif number < 2097152:
        return struct.pack('BBB', number & 127 | 128, number >> 7 & 127 | 128, number >> 14)
    elif number < 268435456:
        return struct.pack('BBBB', number & 127 | 128, number >> 7 & 127 | 128, number >> 14 & 127 | 128, number >> 21)
    else:
        return struct.pack('BBBBB', number & 127 | 128, number >> 7 & 127 | 128, number >> 14 & 127 | 128, number >> 21 & 127 | 128, number >> 28)


def gen_play_info(count: int, log: bool = True):
    p = []
    for h in range(count):  # 生成操作序列
        p.append({'chessIndex': h,
                 'timeTag': random.randint(0, 200)})
    p[0]['timeTag'] = 0
    if log:
        print(len(p))
    GAME_DAILY = 3
    GAME_TOPIC = 4
    data = struct.pack('BB', 8, GAME_DAILY)
    for i in p:
        c, t = i.values()
        data += struct.pack('BBB', 34, 4, 8)
        data += multi_byte_int(c)
        data += struct.pack('B', 16)
        data += multi_byte_int(t)
    data = base64.b64encode(data).decode("utf-8")
    if log:
        print(data)
    return data


def new_api(url="/sheep/v1/game/user_rank_info", header={}, args={}, log: bool = True):
    api_get(
        f"https://cat-match.easygame2021.com{url}?rank_score={args.rank_score}&rank_state={args.rank_state}&rank_time={args.rank_time}&rank_role={args.rank_role}&skin={args.skin}&uid={args.uid}",
        header, log)


def main():
    parser = argparse.ArgumentParser(
        description='A simple example for sheep game')
    parser.add_argument('--rank_score', type=int, default=1,
                        help='rank_score default 1')
    parser.add_argument('--rank_state', type=int, default=1,
                        help='rank_state default 1')
    parser.add_argument('--rank_time', type=int, default=320,
                        help='rank_time default 320')
    parser.add_argument('--rank_role', type=int, default=1,
                        help='rank_role default 1')
    parser.add_argument('--skin', type=int, default=1, help='skin default 1')
    parser.add_argument('--t', type=str, required=True,
                        help='t token, required')
    parser.add_argument('--uid', type=str, required=True,
                        help='user id, required')

    args = parser.parse_args()
#     print(f"""{{
#   "rank_time": {args.rank_time},
#   "rank_role": {args.rank_role},
#   "rank_score": {args.rank_score},
#   "rank_state": {args.rank_state},
#   "skin": {args.skin}
# }}
# """)
#     return

    header = {
        'Host': 'cat-match.easygame2021.com',
        't': args.t,
        'content-type': 'application/json',
        'Accept-Encoding': 'gzip,compress,br,deflate',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.28(0x18001c26) NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx141bfb9b73c970a9/15/page-frame.html',
    }

    # 用户信息
    # new_api("/sheep/v1/game/personal_info", header, args)

    # 每日
    # print(f"will sleep {args.rank_time}s")
    config.steps = gen_play_info(
        map_api(header, log=False),
        log=False)
    time.sleep(args.rank_time)
    temp_api(header, args, log=False)
    time.sleep(1)
    # api_get(
    #     f"https://cat-match.easygame2021.com/sheep/v1/game/update_user_skin?skin={24}", header, log=False)

    # 用户信息
    new_api("/sheep/v1/game/personal_info", header, args)
    # new_api("/sheep/v1/game/user_rank_info", header, args)

    # 话题
    # new_api("/sheep/v1/game/topic_game_over", header, args)


if __name__ == '__main__':
    main()
