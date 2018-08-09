def camel_case(word):
    return "".join([group[0].upper() + group[1:] for group in word.split("_")])
