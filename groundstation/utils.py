import os


def is_dir(path):
    return (040000 & (os.stat(path).st_mode)) > 0


def find_leaf_dirs(d):
    leafs = []

    def _find_leafs(d):
        for i in os.listdir(d):
            this_path = os.path.join(d, i)
            if sum(1 if is_dir(os.path.join(this_path, n)) else 0 for n in os.listdir(this_path)) > 0:
                _find_leafs(this_path)
            else:
                leafs.append(this_path)
    _find_leafs(d)
    return leafs
