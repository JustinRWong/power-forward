


## Reference: https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def stringify_dict(dictlike, building_str=''):
    for k, v in dictlike.items():
        building_str = building_str + "\n  > {k}: {v}".format(k=k, v=v)
    return building_str
