# Written by Stephen Elliott
# (c) Conta Digital Pty Ltd

from src.Env import *
import Interface as Interface

def load_from_dump():
    """
    Loads data from previously saved dumps.
    """
    path = Path(r'dumps\2023-11-21\event_data\event-736580498325646.bin')
    with open(path, 'rb') as f:
        data = pickle.load(f)
    print(f'Loaded data of type {type(data)} from {path}.')
    return data

def get_generator_from_txt_path(txt_path):
    txt_path = str(txt_path)
    with open(txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            # rstripped of commas, letters and newlines
            line = line.strip(',').rstrip(string.ascii_letters).strip('\n')   # TODO - fix
            yield line
