import math

import pytest

import graph


@pytest.fixture
def empty_graph():
    return graph.Graph()


@pytest.fixture
def graph_with_data(empty_graph, csv_file_path):
    empty_graph.load_from_csv(csv_file_path)
    return empty_graph


def test_init_graph(empty_graph):
    assert empty_graph.edges == {}


def test_get_edges_copy(empty_graph):
    assert empty_graph.edges is not empty_graph.edges


def test_add_edges(empty_graph):
    empty_graph.add_edge('a', 'b', 1)
    assert empty_graph.edges == {'a': {'b': 1}}
    empty_graph.add_edge('c', 'b', 2)
    assert empty_graph.edges == {'a': {'b': 1}, 'c': {'b': 2}}
    empty_graph.add_edge('a', 'b', 2)
    assert empty_graph.edges == {'a': {'b': 2}, 'c': {'b': 2}}


def test_add_negative_edge(empty_graph):
    with pytest.raises(graph.WeightError):
        empty_graph.add_edge('a', 'b', -1)


def test_add_infinite_edge(empty_graph):
    with pytest.raises(graph.WeightError):
        empty_graph.add_edge('a', 'b', math.inf)


def test_add_non_int_edge(empty_graph):
    with pytest.raises(graph.WeightError):
        empty_graph.add_edge('a', 'b', '5')


def test_load_from_csv(empty_graph, csv_file_path):
    assert empty_graph.edges == {}
    empty_graph.load_from_csv(csv_file_path)
    assert empty_graph.edges == {'A': {'B': 5, 'D': 5, 'E': 7},
                                 'B': {'C': 4},
                                 'C': {'D': 8, 'E': 2},
                                 'D': {'C': 8, 'E': 6},
                                 'E': {'B': 3},
                                 }


def test_get_distance(graph_with_data):
    g = graph_with_data
    assert g.get_distance(['A', 'B', 'C']) == 9
    assert g.get_distance(['D', 'E', 'B', 'C', 'E']) == 15
    assert g.get_distance(['A']) == 0
    assert g.get_distance(['A', 'A']) == 'NO SUCH ROUTE'
    assert g.get_distance(['A', 'C', 'E']) == 'NO SUCH ROUTE'


def test_get_path_invalid_stop_value(graph_with_data):
    g = graph_with_data
    with pytest.raises(graph.StopValueError):
        next(g._get_paths('A', 'B', -5, 'weight'))

    with pytest.raises(graph.StopValueError):
        next(g._get_paths('A', 'C', math.inf, 'depth'))


def test_get_path_invalid_priority_attr(graph_with_data):
    g = graph_with_data
    with pytest.raises(graph.PriorityAttributeError):
        next(g._get_paths('A', 'B', 20, 'attr'))


def test_get_path_in_depth(graph_with_data):
    # TODO: Move weight & depth checks in separate tests
    g = graph_with_data
    assert set(g._get_paths('A', 'E', 2, 'depth')) == {graph.PathInfo(('A', 'E'), 7, 1),
                                                       graph.PathInfo(('A', 'D', 'E'), 11, 2),
                                                       }
    assert set(g._get_paths('C', 'C', 2, 'depth')) == {graph.PathInfo(('C', 'D', 'C'), 16, 2)}
    assert set(g._get_paths('E', 'A', 5, 'depth')) == set()


def test_get_path_in_weight(graph_with_data):
    # TODO: Move weight & depth checks in separate tests
    g = graph_with_data
    assert set(g._get_paths('A', 'E', 15, 'weight')) == {graph.PathInfo(('A', 'E'), 7, 1),
                                                         graph.PathInfo(('A', 'D', 'E'), 11, 2),
                                                         graph.PathInfo(('A', 'B', 'C', 'E'), 11, 3),
                                                         graph.PathInfo(('A', 'D', 'C', 'E'), 15, 3),
                                                         }
    assert set(g._get_paths('C', 'C', 16, 'weight')) == {graph.PathInfo(('C', 'D', 'C'), 16, 2),
                                                         graph.PathInfo(('C', 'E', 'B', 'C'), 9, 3),
                                                         }
    assert set(g._get_paths('E', 'A', 99, 'weight')) == set()  # There is no any paths
    assert set(g._get_paths('C', 'C', 20, 'weight')) == {graph.PathInfo(('C', 'D', 'C'), 16, 2),
                                                         graph.PathInfo(('C', 'E', 'B', 'C'), 9, 3),
                                                         graph.PathInfo(('C', 'E', 'B', 'C', 'E', 'B', 'C'), 18, 6),
                                                         }


def test_get_shortest_path_length(graph_with_data):
    g = graph_with_data
    assert g.get_shortest_path_length('E', 'A') == math.inf  # No such path
    assert g.get_shortest_path_length('A', 'E') == 7  # Direct path A->E
    assert g.get_shortest_path_length('C', 'C') == 9  # C->E->B->C
    assert g.get_shortest_path_length('D', 'D') == 16  # D->C->D
