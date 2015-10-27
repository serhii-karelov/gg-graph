import argparse
import sys
import operator

import graph

OPERATOR_LT = '<'
OPERATOR_LE = '<='
OPERATOR_EQ = '=='

OPERATORS = {
    OPERATOR_LT: operator.lt,
    OPERATOR_LE: operator.le,
    OPERATOR_EQ: operator.eq,
}


def _filter(paths, attr, op, stop_value):
    op = OPERATORS.get(op)
    filtered = list(filter(lambda p: op(getattr(p, attr), stop_value), paths))
    return filtered


def get_distance(g, path):
    return g.get_distance(path)


def get_paths_filtered_by_stops(g, start, end, op, stop_value):
    paths = g.get_paths_by_depth(start, end, stop_value)
    filtered = list(_filter(paths, graph.ATTR_NAME_DEPTH, op, stop_value))
    return len(filtered)


def get_paths_filtered_by_length(g, start, end, op, stop_value):
    paths = g.get_paths_by_weight(start, end, stop_value)
    filtered = list(_filter(paths, graph.ATTR_NAME_WEIGHT, op, stop_value))
    return len(filtered)


def get_shortest_path_length(g, start, end):
    return g.get_shortest_path_length(start, end)


def get_graph(path):
    g = graph.Graph()
    g.load_from_csv(path)

    return g


def process_distance(args):
    g = get_graph(args.file)
    route = args.route.split(',')
    return get_distance(g, route)


def process_shortest_path(args):
    g = get_graph(args.file)
    return get_shortest_path_length(g, args.start, args.end)


def process_paths_by_stops(args):
    g = get_graph(args.file)
    return get_paths_filtered_by_stops(g, args.start, args.end, args.operator, args.value)


def process_paths_by_distance(args):
    g = get_graph(args.file)
    return get_paths_filtered_by_length(g, args.start, args.end, args.operator, args.value)


def init_command_line_args():
    distance_args = [
        ((), dict(type=str, help='path to csv file which represents a graph', dest='file')),
        (('-r', '--route'), dict(required=True, help='route to calculate a distance', dest='route')),
    ]

    start_end_args = [
        ((), dict(type=str, help='path to csv file which represents a graph', dest='file')),
        (('-s', '--start'), dict(required=True, help='start of the path', dest='start')),
        (('-e', '--end'), dict(required=True, help='end of the path', dest='end')),
    ]

    filtering_args = start_end_args + [
        (('-o', '--operator'), dict(required=True, choices=OPERATORS.keys(),
                                    help='filtering operator', dest='operator', default=OPERATOR_LE)),
        (('-v', '--value'), dict(required=True, type=int, help='Filtering value - positive integer', dest='value')),
    ]

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands')
    distance_parser = subparsers.add_parser('distance')
    distance_parser.set_defaults(process=process_distance)

    for args, kwargs in distance_args:
        distance_parser.add_argument(*args, **kwargs)

    shortest_path_parser = subparsers.add_parser('shortest-path')
    shortest_path_parser.set_defaults(process=process_shortest_path)

    for args, kwargs in start_end_args:
        shortest_path_parser.add_argument(*args, **kwargs)

    paths_by_stops_path_parser = subparsers.add_parser('paths-by-stops')
    paths_by_stops_path_parser.set_defaults(process=process_paths_by_stops)

    paths_by_distance_parser = subparsers.add_parser('paths-by-distance')
    paths_by_distance_parser.set_defaults(process=process_paths_by_distance)

    for p in (paths_by_stops_path_parser, paths_by_distance_parser):
        for args, kwargs in filtering_args:
            p.add_argument(*args, **kwargs)

    return parser


def main():
    parser = init_command_line_args()
    args = parser.parse_args()
    if hasattr(args, 'process'):
        print(args.process(args))
    return 0


if __name__ == '__main__':
    sys.exit(main())
