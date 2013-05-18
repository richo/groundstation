import os


def is_dir(path):
    try:
        return (040000 & (os.stat(path).st_mode)) > 0
    except OSError:
        return False


def find_leaf_dirs(root, ident_format=False):
    leafs = []

    def _find_leafs(d):
        for i in os.listdir(d):
            this_path = os.path.join(d, i)
            if sum(1 if is_dir(os.path.join(this_path, n)) else 0 for n in os.listdir(this_path)) > 0:
                _find_leafs(this_path)
            else:
                if ident_format:
                    this_path = this_path.replace(root+"/", "")
                leafs.append(this_path)
    _find_leafs(root)
    return leafs


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def oid2hex(oid):
    return oid.hex


def path2id(path):
    o_dir, o_name = os.path.split(path)
    return "%s%s" % (os.path.basename(o_dir), o_name)
