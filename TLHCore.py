import requests
from pyquery import PyQuery as pq
import pandas as pd
import math

def get(account=None, password=None, mode='s'):
    if not(account and password):
        raise ValueError('Account or password Error!')
    s = requests.Session()
    s.encoding = 'big5'

    login = s.post("http://register.tlhc.ylc.edu.tw/hcode/login.asp", data={
        'txtID': account,
        'txtPWD': password,
        'login_r7_c5.x': 0,
        'login_r7_c5.y': 0,
        'Chk': 'Y'}) # Login
    login.encoding = 'big5'
    if "無權使用 請登入" in login.text:
        raise ValueError('Account or password Error!')
    login = s.get("http://academic.hchs.hc.edu.tw/skyweb/f_left.asp")

    def get_score(): # 學期成績
        get_score_data = s.get("http://register.tlhc.ylc.edu.tw/hcode/STD_SCORE.asp")
        get_score_data.encoding = 'big5'
        score_datas = pd.read_html(get_score_data.text)[3]
        sum_datas = pd.read_html(get_score_data.text)[5]
        score = {}
        subjects = [i for i in score_datas[0][2:18]]
        sum_titles = [i for i in sum_datas[0][1:-1]]
        for i in range(1,11):
            parsed_scores = [i for i in score_datas[i]][2:18]
            exam = score_datas[i][1]
            try:
                if math.isnan(exam):
                    continue
            except TypeError:
                pass
            score[exam] = dict(zip(subjects, [[i]+[float('nan'),float('nan'),float('nan')] for i in parsed_scores]))
        for i in range(1,8):
            sum_data = sum_datas[i][:-1]
            if not sum_data[0] in score:
                continue
            score[sum_data[0]].update(dict(zip(sum_titles, sum_data[1:])))
        print(score)
        """
        資料格式: {'第1次平時成績':
                    {'◎ 國文Ⅴ':[ 成績 , 平均 , 排名 , 排名人數],
                    '◎ 英文Ⅴ': ['78', nan, nan, nan],
                    ....,
                    '總分': nan....},
                ....}
        }}
        """
        return score

    mode_selector = {
        's': get_score, # 學期成績
        'c': None, # 學分資訊
        'y': None, # 學年成績
        'S': None, # 歷年學期成績
        'Y': None, # 歷年學年成績
        'r': None, # 重修科目
        'g': None, # 擔任幹部
        'C': None, # 社團
        'p': None, # 學期獎懲
        'P': None, # 歷年獎懲
        'n': None, # 學期缺曠
        "N": None # 歷年缺曠
    }
    data = {}
    for i in mode:
        try:
            data[i] = mode_selector[i]()
        except KeyError:
            data[i] = {}
    return data