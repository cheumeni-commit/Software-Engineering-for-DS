from datetime import datetime
import argparse


from src.config.config import get_config
from src.context import context
from src.run_dataset import main_dataset
from src.run_train import main_train

parser = argparse.ArgumentParser()

parser.add_argument('command', choices=['run_dataset', 'run_train'])
#parser.add_argument("-i", "--input-data")
parser.add_argument('--environment', choices=['dev', 'prod'])
parser.add_argument('--show-time', action='store_true')

args = parser.parse_args()

def main_cli(args):
    
    if args.command == 'run_dataset':
        main_dataset()
    else:
        main_train(args.command)

    if args.show_time:
        print(f"Current date & time: {datetime.now()}")

def arg_cli():
    return parser.parse_args()

