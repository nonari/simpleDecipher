import time


class Progress:

    def __init__(self):
        # Timestamp
        self._timestamp = time.time()
        # Last nodes record
        self._node_record = 0
        # Number of explored nodes
        self._node_counter = 0
        # Max depth reached
        self._max_depth = 0
        # Average depth reached
        self._avg_depth = float(0)
        # Current depth counter
        self._current_depth = 0
        # Number of leaf nodes reached
        self._leaf_nodes = 0
        # Path words list
        self._path_words = []
        # Current words path
        self._temp_path_words = []

    def node(self, word: tuple) -> str:
        info = ''
        if divmod(self._node_counter, 100000)[1] == 0:
            info += self.stats()
        info += 'Node: ' + self._node_counter.__str__()
        info += 'Current: ' + word.__str__()
        self._node_counter += 1
        self._current_depth += 1
        self._temp_path_words.append(word)
        return info

    def node_up(self) -> str:
        info = ''
        info += 'Up ↑ '
        if self._current_depth > 0:
            self._current_depth -= 1
            info += self._temp_path_words.pop(-1).__str__()
        return info

    def leaf(self, word) -> str:
        info = 'Node: ' + self._node_counter.__str__() + ' (Leaf)'
        info += 'Current: ' + word.__str__()
        self._temp_path_words.append(word)
        if len(self._temp_path_words) > len(self._path_words):
            self._path_words = self._temp_path_words.copy()
        self._current_depth += 1
        self._node_counter += 1
        if self._max_depth < self._current_depth:
            self._max_depth = self._current_depth
        self._avg_depth = (self._current_depth + (self._avg_depth * float(self._leaf_nodes)))\
            / (self._leaf_nodes + 1)
        self._leaf_nodes += 1
        return info

    def root(self) -> str:
        self._current_depth = 0
        self._node_counter += 1
        return 'ROOT NODE'

    def stats(self) -> str:
        elapsed = time.time() - self._timestamp
        self._timestamp = time.time()
        nodes = self._node_counter - self._node_record
        self._node_record = self._node_counter
        nodes_per_second = int(nodes / elapsed)

        return 'Nodes: ' + self._node_counter.__str__() + '\n' \
               + 'Nodes/s: ' + nodes_per_second.__str__() + '\n' \
               + 'Max Depth: ' + self._max_depth.__str__() + '\n'\
               + 'Avg Depth: ' + "{:.2f}".format(self._avg_depth) + '\n' \
               + 'Path: ' + self._path_words.__str__() + '\n'
