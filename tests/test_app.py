import math

import pytest

from graph import app, graph


@pytest.fixture
def parser():
    return app.init_command_line_args()


@pytest.fixture
def empty_graph():
    return graph.Graph()


@pytest.fixture
def graph_with_data(empty_graph, csv_file_path):
    empty_graph.load_from_csv(csv_file_path)
    return empty_graph


def test_get_distance(graph_with_data):
    assert app.get_distance(graph_with_data, ['A', 'D', 'E']) == 11


def test_get_paths_filtered_by_stops(graph_with_data):
    assert app.get_paths_filtered_by_stops(graph_with_data, 'A', 'E', '==', 3) == 2
    assert app.get_paths_filtered_by_stops(graph_with_data, 'A', 'E', '<=', 3) == 4
    assert app.get_paths_filtered_by_stops(graph_with_data, 'A', 'E', '<', 2) == 1
    assert app.get_paths_filtered_by_stops(graph_with_data, 'E', 'A', '<', 2) == 0


def test_get_paths_filtered_by_length(graph_with_data):
    assert app.get_paths_filtered_by_length(graph_with_data, 'A', 'E', '==', 7) == 1
    assert app.get_paths_filtered_by_length(graph_with_data, 'C', 'C', '<=', 9) == 1
    assert app.get_paths_filtered_by_length(graph_with_data, 'C', 'C', '<', 30) == 7


def test_get_shortest_path_length(graph_with_data):
    assert app.get_shortest_path_length(graph_with_data, 'E', 'A') == math.inf
    assert app.get_shortest_path_length(graph_with_data, 'A', 'E') == 7
    assert app.get_shortest_path_length(graph_with_data, 'C', 'C') == 9



def test_process_distance(parser, csv_file_path):
    args = parser.parse_args(['distance', csv_file_path, '-r', 'A,B,C,D'])
    assert app.process_distance(args) == 17


def test_process_shortest_path(parser, csv_file_path):
    args = parser.parse_args(['shortest-path', csv_file_path, '-s', 'A', '-e', 'B'])
    assert app.process_shortest_path(args) == 5


def test_process_paths_by_stops(parser, csv_file_path):
    args = parser.parse_args(['paths-by-stops', csv_file_path, '-s', 'A', '-e', 'B', '-o', '<', '-v', '3'])
    assert app.process_paths_by_stops(args) == 2


def test_process_paths_by_distance(parser, csv_file_path):
    args = parser.parse_args(['paths-by-distance', csv_file_path, '-s', 'C', '-e', 'C', '-o', '<', '-v', '30'])
    assert app.process_paths_by_distance(args) == 7


def test_cla_distance(parser, csv_file_path):
    args = parser.parse_args(['distance', csv_file_path, '-r', 'A,B,C,D'])
    full_args = parser.parse_args(['distance', csv_file_path, '--route', 'A,B,C,D'])
    assert args.file == full_args.file == csv_file_path
    assert args.route == full_args.route == 'A,B,C,D'


def test_cla_shortest_path(parser, csv_file_path):
    args = parser.parse_args(['shortest-path', csv_file_path, '-s', 'A', '-e', 'B'])
    full_args = parser.parse_args(['shortest-path', csv_file_path, '--start', 'A', '--end', 'B'])
    assert args.file == full_args.file == csv_file_path
    assert args.start == full_args.start == 'A'
    assert args.end == full_args.end == 'B'


def test_cla_paths_by_stops(parser, csv_file_path):
    args = parser.parse_args(['paths-by-stops', csv_file_path, '-s', 'A', '-e', 'B', '-o', '<', '-v', '12'])
    full_args = parser.parse_args(['paths-by-stops', csv_file_path, '--start', 'A', '--end', 'B',
                                                                    '--operator', '<', '--value', '12'])
    assert args.file == full_args.file == csv_file_path
    assert args.start == full_args.start == 'A'
    assert args.end == full_args.end == 'B'
    assert args.operator == full_args.operator == '<'
    assert args.value == full_args.value == 12


def test_cla_paths_by_distance(parser, csv_file_path):
    args = parser.parse_args(['paths-by-distance', csv_file_path, '-s', 'A', '-e', 'B', '-o', '<=', '-v', '3'])
    full_args = parser.parse_args(['paths-by-distance', csv_file_path, '--start', 'A', '--end', 'B',
                                                                       '--operator', '<=', '--value', '3'])
    assert args.file == full_args.file == csv_file_path
    assert args.start == full_args.start == 'A'
    assert args.end == full_args.end == 'B'
    assert args.operator == full_args.operator == '<='
    assert args.value == full_args.value == 3
