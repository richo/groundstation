def slices(num, string):
    store = []
    for i in xrange(num):
        store.append(string[0:2])
        string = string[2:]
    store.append(string)
    return store
