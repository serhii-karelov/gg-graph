import collections
import csv
import queue
import math

ERROR_MESSAGE_NO_SUCH_ROUTE = 'NO SUCH ROUTE'

ATTR_NAME_WEIGHT = 'weight'
ATTR_NAME_DEPTH = 'depth'
ATTR_CHOICES = {ATTR_NAME_DEPTH, ATTR_NAME_WEIGHT}

PathInfo = collections.namedtuple('PathInfo', ['path', ATTR_NAME_WEIGHT, ATTR_NAME_DEPTH])


class WeightError(Exception):
    pass


class StopValueError(Exception):
    pass


class PriorityAttributeError(Exception):
    pass


class Graph(object):
    def __init__(self):
        self.__edges = {}

    def add_edge(self, from_vertex, to, weight):
        if not isinstance(weight, int):
            raise WeightError('`weight` must be an integer')

        if not 0 <= weight < math.inf:
            raise WeightError('`weight` must satisfy the condition: 0 <= weight < Infinity')

        self.__edges.setdefault(from_vertex, {})[to] = weight

    @property
    def edges(self):
        return self.__edges.copy()

    def get_distance(self, path):
        """
        Sums the weights of the paths.
        :param path: iterable consequence of vertices
        :rtype: int or str
        """
        vertices = path[::-1]
        current_vertex = vertices.pop()
        edges = self.edges
        weights = []
        while vertices:
            vertex = edges.get(current_vertex)
            next_vertex = vertices.pop()
            weight = vertex.get(next_vertex)
            if weight is None:
                return ERROR_MESSAGE_NO_SUCH_ROUTE
            weights.append(weight)
            current_vertex = next_vertex

        return sum(weights)

    def _get_paths(self, from_vertex, to, stop_value, priority_attr):
        """
        Yields all possible paths between `from_vertex` and `to`.

        :param from_vertex: vertex to start from
        :param to: vertex-endpoint
        :param stop_value: Value which represents the moment when we shouldn't process more data.
                           Works in pair with priority_attr.
                           Example: if stop_value=2 and priority_attr='depth'
                                    then graph won't be processed deeper than 5th level.
        :param priority_attr: Value which determines by which field graph will be prioritised.
                              Valid choices: 'depth' or 'weight'.
        :return: decorator
        """
        def _getattr(obj):
            return getattr(obj, priority_attr)

        if priority_attr not in ATTR_CHOICES:
            raise PriorityAttributeError('Invalid `priority_attr`. Valid choices: %s' % ATTR_CHOICES)

        if not 0 <= stop_value < math.inf:
            raise StopValueError('`stop_value` must satisfy the condition: 0 <= weight < Infinity')

        edges = self.edges
        init_p = (from_vertex,)
        init_pi = PathInfo(init_p, 0, 0)
        q = queue.PriorityQueue()
        q.put((_getattr(init_pi), init_pi))

        while not q.empty():
            _, path_to_process = q.get()
            vertex = path_to_process.path[-1]
            vert = edges[vertex]

            if _getattr(path_to_process) >= stop_value:
                break

            for v in vert.keys():
                new_path = PathInfo(path=path_to_process.path + (v,),
                                    weight=path_to_process.weight + vert[v],
                                    depth=path_to_process.depth + 1)
                q.put((_getattr(new_path), new_path))
                if v == to and _getattr(new_path) <= stop_value:
                    yield new_path

    def get_paths_by_depth(self, from_vertex, to, stop_value):
        return self._get_paths(from_vertex, to, stop_value, ATTR_NAME_DEPTH)

    def get_paths_by_weight(self, from_vertex, to, stop_value):
        return self._get_paths(from_vertex, to, stop_value, ATTR_NAME_WEIGHT)

    def get_shortest_path_length(self, from_vertex, to):
        """
        Finds the shortest path. Uses Dijkstra's algorithm.
        :return: shortest path (sum of weights) between `from_vertex` and `to`
        :rtype int or math.inf
        """
        edges = self.edges
        reweight = {}
        q = queue.PriorityQueue()
        q.put((0, from_vertex))

        while not q.empty():
            path_weight, vert = q.get()
            vertex = edges[vert]
            for v, w in vertex.items():
                new_weight = path_weight + w
                if new_weight < reweight.get(v, math.inf):
                    reweight[v] = new_weight
                    q.put((new_weight, v))

        return reweight.get(to, math.inf)

    def load_from_csv(self, full_path):
        """
        Loads data from CSV file.
        Example formatting:
            A,B,5
            B,C,7
            C,B,2
        First and second columns are for edge. The third column is edge's weight.
        """
        with open(full_path, 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for line in reader:
                line[2] = int(line[2])  # Convert weight to int
                self.add_edge(*line)
