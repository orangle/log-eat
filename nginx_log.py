# coding:utf-8
from datetime import datetime
from math import log

import click
import pandas as pd 
from ding import DingHK

ding_token = "6f0c3e73c7eb83ae86cc96c7b741af22403787d6a35d86bbdaa66c53218caadb"


def parser(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            try:
                cl = line.split()
                # 0 clientip  # 3 time # 7 uri
                # 9 status # 10 bytes
                record = {
                    'ip': cl[0],
                    'time': datetime.strptime(cl[3][1:], "%d/%B/%Y:%H:%M:%S"),
                    'uri': cl[7],
                    'code': cl[9],
                    'bytes': int(cl[10])
                }
                res.append(record)
            except Exception as e:
                pass
    return res

def summary(datas):
    df = pd.DataFrame(datas)
    # total pv, uv, keys, bytes, code distribution
    # pv time distribution
    msg = ("pv: {}, uv: {}\nall keys: {}, total bytes: {}\n" 
           "\n{}\n\n{}").format(
            len(df),
            len(df['ip'].unique()),
            len(df['uri'].unique()),
            pretty_size(df['bytes'].sum()),
            df.groupby(df['code']).size().reset_index(name='Size'),
            df.groupby(df['time'].map(
                lambda x: x.hour)).size().reset_index(name='Size')
          )
    return msg 


def pretty_size(n,pow=0,b=1024,u='B',pre=['']+[p+'i'for p in'KMGTPEZY']):
    pow,n=min(int(log(max(n*b**pow,1),b)),len(pre)-1),n*b**pow
    return "%%.%if %%s%%s"%abs(pow%(-pow-1))%(n/b**float(pow),pre[pow],u)


@click.command()
@click.argument('filepath')
def main(filepath):
    data = parser(filepath) 
    msg = summary(data)
    if msg:
        ding = DingHK(ding_token)
        ding.send_text(msg) 


if __name__ == "__main__":
    main()
