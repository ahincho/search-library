"""search-library: A professional, extensible search algorithm framework."""

__version__ = "1.0.0"

from search_library.algorithms.astar import AStarSearch, astar_search
from search_library.algorithms.bfs import BFS, bfs_search
from search_library.algorithms.bidirectional import BidirectionalSearch, bidirectional_search
from search_library.algorithms.dfs import DFS, dfs_search
from search_library.algorithms.dijkstra import Dijkstra, dijkstra_search
from search_library.core.nodes import Node
from search_library.core.problem import SearchProblem
from search_library.core.result import SearchResult
from search_library.graph.graph import Graph
from search_library.grid.grid import Grid
from search_library.heuristics.euclidean import EuclideanHeuristic
from search_library.heuristics.manhattan import ManhattanHeuristic

__all__ = [
    "BFS",
    "DFS",
    "AStarSearch",
    "BidirectionalSearch",
    "Dijkstra",
    "EuclideanHeuristic",
    "Graph",
    "Grid",
    "ManhattanHeuristic",
    "Node",
    "SearchProblem",
    "SearchResult",
    "astar_search",
    "bfs_search",
    "bidirectional_search",
    "dfs_search",
    "dijkstra_search",
]
