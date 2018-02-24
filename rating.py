import json
import sys
import math


class User(object):

    def __init__(self, rank, old_rating, handle='', official_new_rating=0):
        self.rank = float(rank)
        self.old_rating = int(old_rating)
        self.seed = 1.0
        self.handle = str(handle)
        self.official_new_rating = int(official_new_rating)


class Calculator(object):

    def __init__(self, users):
        self.user_list = []
        for user in users:
            self.user_list.append(User(user['rank'], user['oldRating'], user['handle'], user['newRating']))

    def cal_p(self, user_a, user_b):
        return 1.0 / (1.0 + pow(10, (user_b.old_rating - user_a.old_rating) / 400.0))

    def get_ex_seed(self, user_list, rating, own_user):
        ex_user = User(0.0, rating)
        result = 1.0
        for user in user_list:
            if user != own_user:
                result += self.cal_p(user, ex_user)
        return result

    def cal_rating(self, user_list, rank, user):
        left = 1
        right = 8000
        while right - left > 1:
            mid = int((left + right) / 2)
            if self.get_ex_seed(user_list, mid, user) < rank:
                right = mid
            else:
                left = mid
        return left

    def calculate(self):
        for i in range(len(self.user_list)):
            self.user_list[i].seed = 1.0
            for j in range(len(self.user_list)):
                if i != j:
                    self.user_list[i].seed += self.cal_p(self.user_list[j], self.user_list[i])
        sum_delta = 0
        for user in self.user_list:
            user.delta = int(
                (self.cal_rating(self.user_list, math.sqrt(user.rank * user.seed), user) - user.old_rating) / 2)
            sum_delta += user.delta
        inc = int(-sum_delta / len(self.user_list)) - 1
        for user in self.user_list:
            user.delta += inc
        self.user_list = sorted(self.user_list, key=lambda x: x.old_rating, reverse=True)
        s = min(len(self.user_list), int(4 * math.sqrt(len(self.user_list))))
        sum_s = 0
        for i in range(s):
            sum_s += self.user_list[i].delta
        inc = min(max(int(-sum_s / s), -10), 0)
        for user in self.user_list:
            user.delta += inc
            user.new_rating = user.old_rating + user.delta
        self.user_list = sorted(self.user_list, key=lambda x: x.rank, reverse=False)


if __name__ == '__main__':
    contest_id = sys.argv[1]
    with open('cf_rating_' + contest_id + '.json', 'r') as f:
        test_users = json.loads(f.read())
    last_idx = 0
    last_rank = 1
    for i in range(1, len(test_users)):
        if test_users[i]['rank'] > last_rank:
            for j in range(last_idx, i):
                test_users[j]['rank'] = i
            last_idx = i
            last_rank = test_users[i]['rank']

    calculator = Calculator(test_users)
    calculator.calculate()
    res = []
    validation = True
    for user in calculator.user_list:
        res.append({
            'handle': user.handle,
            'rank': int(user.rank),
            'old_rating': user.old_rating,
            'new_rating': user.new_rating,
            'rating_change': user.delta,
        })
        if user.new_rating != user.official_new_rating:
            validation = False
    with open('cf_rating_changes_' + contest_id + '.json', 'w') as f:
        f.write(json.dumps(res, indent=4))
    print('Validation:', validation)
