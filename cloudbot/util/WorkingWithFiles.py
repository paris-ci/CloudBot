def checkExistsPath(path):
    import os
    if not os.path.exists(path):
        os.makedirs(path)


def checkExistsFile(path):
    import os
    if not os.path.exists(path):
        with open(path)as f:
            f.write(path)


def JSONsaveToDisk(data, filename):
    import json
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4, ensure_ascii=False)


def JSONloadFromDisk(filename, default="{}", error=False):
    import json
    try:
        file = open(filename, 'r')
        data = json.load(file)
        return data
    except IOError:
        if not error:
            file = open(filename, 'w')
            file.write(default)
            file.close()
            file = open(filename, 'r')
            data = json.load(file)
            return data
        else:
            raise
