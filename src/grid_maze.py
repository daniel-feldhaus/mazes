from typing import Tuple, Dict
from itertools import product
from maze import ConnectedNodes, Node, NodeConnectionT

import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

GridNodeIdT = Tuple[int, int]
GridNodeMapT = Dict[GridNodeIdT, Node[GridNodeIdT]]
GridConnectionIdT = Tuple[GridNodeIdT, GridNodeIdT]
GridConnectionMapT = Dict[GridConnectionIdT, NodeConnectionT]


class GridNodes(ConnectedNodes[GridNodeIdT]):
    """Grid of inter-connected nodes."""

    width: int
    height: int

    def __init__(self, width: int, height: int, default_connection: NodeConnectionT):
        assert (width > 0) and (
            height > 0
        ), f"Width & Height must be greater than 0: ({width}x{height})"
        self.width = width
        self.height = height
        super().__init__(size=width * height, default_connection=default_connection)

    def __build__(self, default_connection: NodeConnectionT) -> None:
        """Build the node structure with default connections."""
        print(f"Building with default connection: {default_connection}")
        print(f"Grid size: {self.width}x{self.height}")

        def __make_unconnected_grid(width: int, height: int) -> GridNodeMapT:
            return {
                node_id: Node(node_id)
                for node_id in product(range(width), range(height))
            }

        def __get_connections(node_id: Tuple[int, int]) -> GridConnectionMapT:
            """Get a list of existing neighbor ID's"""
            x, y = node_id
            return {
                (node_id, (nx, ny)): default_connection
                for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                if 0 <= nx < self.width and 0 <= ny < self.height
            }

        # Create a grid of empty nodes
        self.nodes = __make_unconnected_grid(self.width, self.height)
        self.connections = {}
        for node_id, node in self.nodes.items():
            connections = __get_connections(node_id)
            print(f"Connections for node {node_id}: {connections}")
            node.connection_ids = set(connections.keys())
            self.connections.update(connections)

        self.run()

    def draw(self) -> Image.Image:
        """Draw the maze using PIL and matplotlib."""
        # Define colors and sizes
        background_color = (255, 255, 255)  # White
        wall_color = (0, 0, 0)  # Black
        cell_size = 20
        wall_thickness = 2

        # Create a blank image
        img_width = (self.width + 1) * cell_size
        img_height = (self.height + 1) * cell_size
        img = Image.new("RGB", (img_width, img_height), background_color)
        draw = ImageDraw.Draw(img)
        for x, y in product(range(self.width + 1), range(self.height + 1)):
            left = x * cell_size
            right = left + cell_size
            bottom = y * cell_size
            top = bottom + cell_size
            if self.connections.get(((x, y), (x + 1, y)), "WALL") == "WALL":
                draw.line(
                    [(right, bottom), (right, top)],
                    fill=wall_color,
                    width=wall_thickness,
                )
            if self.connections.get(((x, y), (x, y + 1)), "WALL") == "WALL":
                draw.line(
                    [(left, top), (right, top)],
                    fill=wall_color,
                    width=wall_thickness,
                )

        return img
