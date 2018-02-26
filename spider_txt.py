# coding=utf-8
import json
import sys
import requests


# Get official rating changes data from Codeforces API
def get_rating(contest_id):
    url = 'http://codeforces.com/api/contest.ratingChanges?contestId={}'.format(contest_id)
    rst = requests.get(url)
    json_response = rst.content.decode()
    dict_json = json.loads(json_response)
    if dict_json['status'] == 'OK':
        return dict_json['result']
    else:
        return None


def work(contest_id):
    data = get_rating(contest_id)
    if data:
        with open('tests/cf_rating_official_{}.txt'.format(contest_id), 'w') as f:
            for d in data:
                f.write('{} {} {} {}\n'.format(d['rank'], d['handle'], d['oldRating'], d['newRating']))
    else:
        print('error!')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 file_name.py [codeforces_contest_id]')
        sys.exit(1)
    contest_id = sys.argv[1]
    work(contest_id)
