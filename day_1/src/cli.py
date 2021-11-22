from datetime import datetime

from src.run_dataset import main_dataset
from src.run_train import main_train

def main_cli(args):
    if args.command == 'run_dataset':
        main_dataset()
    else:
       main_train()

    if args.show_time:
        print(f"Current date & time: {datetime.now()}")
