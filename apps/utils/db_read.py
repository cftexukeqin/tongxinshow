import pymysql
import pandas as pd


def read_query():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        passwd='123456',
        db='tongxin',
        port=3306,
        charset='utf8'
    )
    df = pd.read_sql('select * from front_data', conn)

    return df

if __name__ == '__main__':
    df = read_query()
    print(list(df.name.unique()))
    print(df[df['year'] == '2018']['jidu_2'])
