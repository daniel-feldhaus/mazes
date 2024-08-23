import random
from typing import Generic, TypeVar, Set, Dict, Any, Literal, Tuple
from collections.abc import Hashable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

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


def get_connection_id(
    a: NodeLookupT, b: NodeLookupT
) -> Tuple[NodeLookupT, NodeLookupT]:
    return (a, b) if a < b else (b, a)  # type: ignore


class ConnectedNodes(ABC, Generic[NodeLookupT]):
    """Collection of inter-connected nodes."""

    size: int
    nodes: Dict[NodeLookupT, Node[NodeLookupT]] = {}
    connections: Dict[Tuple[NodeLookupT, NodeLookupT], NodeConnectionT] = {}

    def __init__(self, size: int, default_connection: NodeConnectionT):
        self.size = size
        self.__build__(default_connection)

    def run(self):
        """Generate a maze."""

        def __get_unvisited_neighbor_ids(
            node_id: NodeLookupT, unvisited_node_ids: Set[NodeLookupT]
        ) -> Set[NodeLookupT]:
            node = self.nodes[node_id]
            neighbor_ids = {
                connection_id[0 if connection_id[1] == node_id else 1]
                for connection_id in node.connection_ids
            }
            return {
                neighbor_id
                for neighbor_id in neighbor_ids
                if neighbor_id in unvisited_node_ids
            }

        start_node_id = random.choice(list(self.nodes.keys()))
        active_node_ids = {start_node_id}
        unvisited_node_ids = set(list(self.nodes.keys()))
        unvisited_node_ids.remove(start_node_id)
        while active_node_ids:
            node_id = random.choice(list(active_node_ids))
            unvisited_neighbor_ids = __get_unvisited_neighbor_ids(
                node_id, unvisited_node_ids
            )
            if len(unvisited_neighbor_ids) == 0:
                active_node_ids.remove(node_id)

                continue
            neighbor_id = random.choice(list(unvisited_neighbor_ids))
            connection_id = get_connection_id(node_id, neighbor_id)
            self.connections[connection_id] = "HALL"
            active_node_ids.add(neighbor_id)
            unvisited_node_ids.remove(neighbor_id)
            print(f"Connecting {node_id} to {neighbor_id}")
        for a, b in self.connections.items():
            print(f"{a}: {b}")

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
