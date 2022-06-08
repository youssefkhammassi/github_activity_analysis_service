import inflection


def camelize(string: str):
    return inflection.camelize('_' + string)[1:]
