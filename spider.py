# coding=utf-8
import json
import sys
import requests


def get_rating(contest_id=0):
    url = 'http://codeforces.com/api/contest.ratingChanges?contestId=' + str(contest_id)
    rst = requests.get(url)
    json_response = rst.content.decode()
    dict_json = json.loads(json_response)
    if dict_json['status'] == 'OK':
        return dict_json['result']
    else:
        return None


def work(contest_id=0):
    data = get_rating(contest_id)
    if data:
        with open('cf_rating_{}.json'.format(contest_id), 'w') as fr:
            fr.write(json.dumps(data, indent=4))
    else:
        print('error!')


if __name__ == '__main__':
    contest_id = sys.argv[1]
    work(contest_id)
