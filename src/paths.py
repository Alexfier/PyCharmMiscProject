import os

def root_join(*parts):
    """ A function that returns the path to the file specified from the root """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, *parts)
    return full_path