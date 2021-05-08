import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV = os.environ.get('ENV', 'local').lower()


with open(os.path.join(BASE_DIR, 'AdjustHome', 'build', 'env', '%s.json' % ENV.lower())) as data_file:
    environment_details = json.load(data_file)


def get_environment_details():
    return environment_details, ENV

