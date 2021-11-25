# src/__main__.py
import pandas as pd

from src.io import get_data_catalog
from src.cli import main_cli, arg_cli


if __name__ == '__main__':
    args = arg_cli()
    main_cli(args)

    