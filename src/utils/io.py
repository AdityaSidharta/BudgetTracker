import oyaml as yaml


def save_yaml(file, path):
    with open(path, "w+") as f:
        yaml.safe_dump(file, f)


def load_yaml(path):
    with open(path, "r+") as f:
        value = yaml.safe_load(f)
    return value
