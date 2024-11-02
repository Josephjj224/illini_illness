from flask_restful import reqparse
def reg_args_valid(parser):
    parser.add_argument('email', type=str, location='json')
    parser.add_argument('password', type=str, dest='pwd', location='json')

def create_parser(arg_configs):
    """
    Creates a request parser with the given argument configurations.

    :param arg_configs: A list of dictionaries, each representing the configuration for one argument.
                        Each dictionary should have keys like 'name', 'type', 'required', 'location', etc.
    :return: A configured request parser.
    """
    parser = reqparse.RequestParser()
    for config in arg_configs:
        parser.add_argument(**config)
    return parser

