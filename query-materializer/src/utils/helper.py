def chunk(l, size):
    for i in range(0, len(l), size):
        yield l[i:i+size]

def get_all_constants_values(class_name):
    return [value for name, value in vars(class_name).items() if not name.startswith('_')]
