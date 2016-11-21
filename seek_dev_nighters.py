import argparse
import datetime
import pytz
import requests


def load_attempts():  # Currently, some attempts are lost because API only provides 10 pages.
    """
    Retrieves all attempts made by Devman users as far back as the API keeps track.
    :returns a generator of attempts
    """
    numeration_shift = 1
    base = 'https://devman.org/api/challenges/solution_attempts/'
    base_response = requests.get(base)
    if base_response.status_code != requests.codes.ok:
        return None
    base_response_json = base_response.json()
    number_of_pages = base_response_json['number_of_pages']
    for page in range(numeration_shift, number_of_pages + numeration_shift):
        payload = {'page': page}
        response_json = requests.get(base, params=payload).json()
        for record in response_json['records']:
            yield record


def get_owls(records, dawn_time=5):
    """
    From the given records, gets usernames of users who made their attempts between
    midnight and dawn_time, where dawn_time can be set as a parameter.
    :returns a generator of usernames
    """
    for record in records:
        attempt_time = get_local_time(record)
        if attempt_time is None:
            continue
        midnight = attempt_time.replace(hour=0, minute=0, second=0, microsecond=0)
        dawn = attempt_time.replace(hour=dawn_time, minute=0, second=0, microsecond=0)
        if midnight < attempt_time < dawn:
            yield record['username']


def get_local_time(record):
    if record['timestamp'] is None or record['timezone'] is None:
        return None
    naive_time = datetime.datetime.utcfromtimestamp(record['timestamp'])
    aware_time = pytz.utc.localize(naive_time)
    local_time = aware_time.astimezone(pytz.timezone(record['timezone']))
    return local_time


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('dawn_time', action='store', type=int,
                        help='the time you want to consider the end of the night')
    return parser.parse_args()


if __name__ == '__main__':
    arguments = parse_arguments()
    dawn_time = arguments.dawn_time
    attempts = load_attempts()
    if attempts is None:
        print('There was a problem with your request.')
        raise SystemExit
    owl_generator = get_owls(attempts, dawn_time)
    unique_owls = set(list(owl_generator))
    print(unique_owls)
