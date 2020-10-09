import json
import os
import re
from argparse import ArgumentTypeError
from datetime import datetime
from pathlib import Path

file_pattern = '_neuron_classification.json'


def get_filename(pattern, dir_, mode='last'):
    """searches dir_ for file with a given pattern and returns the first or
    last file dependent on mode setting

    Args:
        pattern (str, re.Pattern) : pattern object for which to search files in dir_
        dir_ (str) : directory name
        mode (str, optional) : determines whether to return the first or last
                               file fitting the pattern
    Returns:
        str or None : file name if found, otherwise None
    """
    if isinstance(pattern, re.Pattern):
        files_found = filter(pattern.search, os.listdir(dir_))
    elif isinstance(pattern, str):
        files_found = [fn for fn in os.listdir(dir_) if pattern in fn]
    try:
        if mode == 'first':
            return min(files_found)
        elif mode == 'last':
            return max(files_found)
        else:
            raise ValueError('only first and last are valid modes for file '
                             'selection')
    except ValueError:
        return None


def keys_to_int(dct):
    return {int(k): v for k, v in dct.items()}


def load_file(targ_dir):
    """"""
    fn = get_filename(file_pattern, targ_dir)
    if fn is None:
        raise FileNotFoundError
    full_fn = Path(targ_dir).joinpath(fn)
    with open(full_fn, 'r') as f:
        data = keys_to_int(json.load(f))

    return data


def mk_time_stamp_str():
    return '{0:%y%m%d}_{0:%H%M%S}'.format(datetime.now())


def write_json(data, out_fn):
    with open(out_fn, 'w') as f:
        json.dump(data, f, sort_keys=False, indent=3,
                  separators=(',', ': '))


def str2bool(v):
    """converts str parsed by arg parser to bool
    from https://stackoverflow.com/a/43357954

    Args:
        v:

    Returns:

    """

    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ArgumentTypeError('Boolean value expected.')