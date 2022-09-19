import argparse
import time
import httpx


def main():
    parser = argparse.ArgumentParser(
        description='A simple example for sheep game')
    parser.add_argument('--rank_score', type=int, default=1,
                        help='rank_score default 1')
    parser.add_argument('--rank_state', type=int, default=1,
                        help='rank_state default 1')
    parser.add_argument('--rank_time', type=int, default=320,
                        help='rank_time default 320')
    parser.add_argument('--rank_role', type=int, default=2,
                        help='rank_role default 2')
    parser.add_argument('--skin', type=int, default=1, help='skin default 1')
    parser.add_argument('--t', type=str, required=True,
                        help='t token, required')

    args = parser.parse_args()

    header = {
        'Host': 'cat-match.easygame2021.com',
        'Connection': 'keep-alive',
        't': args.t,
        'content-type': 'application/json',
        'Accept-Encoding': 'gzip,compress,br,deflate',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.28(0x18001c26) NetType/WIFI Language/zh_CN',
    }
    err_time = 0
    while err_time < 5:
        try:
            response = httpx.get(
                f"https://cat-match.easygame2021.com/sheep/v1/game/game_over_ex?rank_score={args.rank_score}&rank_state={args.rank_state}&rank_time={args.rank_time}&rank_role={args.rank_role}&skin={args.skin}&t={args.t}", headers=header).json()
            print(
                f"运行时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}: {response}")
            return
        except Exception as e:
            err_time += 1
            print(f"err-{err_time}: {e}")
            continue
    print(f"运行时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}: 请求失败")
    raise Exception("请求失败")


if __name__ == '__main__':
    main()
