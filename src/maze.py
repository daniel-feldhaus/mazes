import random
from typing import Generic, TypeVar, Set, Dict, Any, Literal, Tuple
from collections.abc import Hashable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from itertools import product

NodeConnectionT = Literal["HALL", "WALL"]
NodeLookupT = TypeVar("NodeLookupT", bound=Hashable)
NodeLookupPairT = Tuple[NodeLookupT, NodeLookupT]
ConnectionMapT = TypeVar("ConnectionMapT", bound=Dict[NodeLookupPairT, NodeConnectionT])


@dataclass
class Node(Generic[NodeLookupT]):
    """Single node in a maze."""

    id: NodeLookupT
    connection_ids: Set[NodeLookupPairT] = field(default_factory=set)
    data: Dict[str, Any] = field(default_factory=dict)

    def __hash__(self):
        return hash(self.id)

    def draw(self) -> None:
        """Abstract parent class. Used for drawing the node."""
        raise NotImplementedError


class ConnectedNodes(ABC, Generic[NodeLookupT]):
    """Collection of inter-connected nodes."""

    size: int
    nodes: Dict[NodeLookupT, Node[NodeLookupT]]
    connections: Dict[Tuple[NodeLookupT, NodeLookupT], NodeConnectionT]

    def __init__(self, size: int, default_connection: NodeConnectionT):
        self.size = size
        self.__build__(default_connection)

    def run(self):
        """Generate a maze."""

        def __get_unvisited_neighbor_ids(
            node_id: NodeLookupT, visited_node_ids: Set[NodeLookupT]
        ) -> Set[NodeLookupT]:
            node = self.nodes[node_id]
            return {
                connection_id[0 if connection_id[1] == node_id else connection_id[1]]
                for connection_id in node.connection_ids
                if connection_id not in visited_node_ids
            }

        start_node_id = random.choice(list(self.nodes.keys()))
        visited_node_ids = {start_node_id}
        print("Running")
        while visited_node_ids:
            node_id = random.choice(list(visited_node_ids))
            print(f"Selected {node_id}")
            unvisited_neighbor_ids = __get_unvisited_neighbor_ids(
                node_id, visited_node_ids
            )
            if not unvisited_neighbor_ids:
                print(f"Dropping {node_id}")
                visited_node_ids.remove(node_id)
                continue
            neighbor_id = random.choice(list(unvisited_neighbor_ids))
            self.connections[(node_id, neighbor_id)] = "HALL"
            visited_node_ids.add(neighbor_id)
            print({f"Added {neighbor_id}"})

    @abstractmethod
    def __build__(self, default_connection: NodeConnectionT) -> None:
        """
        Abstract method to build the node structure.
        Must be implemented by subclasses.
        """

    @abstractmethod
    def draw(self) -> None:
        """
        Represent the nodes and their connections visually.
        """
