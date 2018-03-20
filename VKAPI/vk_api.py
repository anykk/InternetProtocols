import argparse
import json
from urllib import request
"""Например, вывести
список друзей указанного пользователя, вывести названия фотоальбомов указанного пользо-
вателя и т. п."""


def parse_args():
    parser = argparse.ArgumentParser(description='simple vk api util')
    parser.add_argument('-method', type=str, help=("method to execute\n"
                                                   "\n"
                                                   "available methods:\n"))
    parser.add_argument('-parameters', type=str, help='parameters for method')
    return parser.parse_args()


if __name__ == '__main__':
    print(get_response('users.get?user_id=210700286&v=5.73')['response'])
