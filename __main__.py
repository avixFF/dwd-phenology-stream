import os
import time
import json
import shutil
import argparse
from dotenv import load_dotenv
from streams import Stream

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument(
    '-c', '--clear-cache',
    const=True,
    action='store_const',
    default=False,
    help='clear cache before running (default: false)'
)
parser.add_argument(
    '-m', '--migrate',
    const=True,
    action='store_const',
    default=False,
    help='migrate database'
)
parser.add_argument(
    '--fresh',
    const=True,
    action='store_const',
    default=False,
    help='re-run all database migrations'
)

args = parser.parse_args()

if args.migrate:
    from database.migrate import run as migrate
    migrate(fresh=args.fresh)
    exit()

if args.clear_cache and os.path.exists('cache'):
    shutil.rmtree('cache')

config = {}

with open('config.json', 'r') as f:
    config = json.load(f)

    for options in config.get('streams', []):
        stream = Stream.make(options.get('type'), options)
        stream.fetch()
