from a_star import GraphNode, a_star
from unittest import TestCase


class TestAStar(TestCase):
    def setUp(self):
        self.graph_1 = {
            "A": GraphNode("A", {"B": 1}, 5.5),
            "B": GraphNode("B", {"A": 1, "C": 3}, 4.5),
            "C": GraphNode("C", {"B": 3, "D": 2, "G": 8}, 3.5),
            "D": GraphNode("D", {"C": 2, "E": 2}, 2.5),
            "E": GraphNode("E", {"D": 2, "F": 2}, 2.5),
            "F": GraphNode("F", {"E": 2, "J": 3}, 1.5),
            "G": GraphNode("G", {"C": 8, "H": 2}, 5),
            "H": GraphNode("H", {"G": 2, "I": 7}, 4),
            "I": GraphNode("I", {"H": 8, "J": 1}, 3.5),
            "J": GraphNode("J", {"I": 1, "F": 2}, 0),
        }

        self.graph_2 = {
            "A": GraphNode("A", {"B": 1}, 5.5),
            "B": GraphNode("B", {"A": 1, "C": 3}, 4.5),
            "C": GraphNode("C", {"B": 3, "D": 2, "G": 8}, 3.5),
            "D": GraphNode("D", {"C": 2, "E": 2}, 2.5),
            "E": GraphNode("E", {"D": 2, "F": 2}, 2.5),
            "F": GraphNode("F", {"E": 2, "J": 50}, 1.5),
            "G": GraphNode("G", {"C": 8, "H": 2}, 5),
            "H": GraphNode("H", {"G": 2, "I": 7}, 4),
            "I": GraphNode("I", {"H": 8, "J": 1}, 3.5),
            "J": GraphNode("J", {"I": 1, "F": 2}, 0),
        }

    def test_a_star(self):
        expected_1 = ["A", "B", "C", "D", "E", "F", "J"]
        actual_1 = a_star(self.graph_1, "A", "J")

        expected_2 = ["A", "B", "C", "G", "H", "I", "J"]
        actual_2 = a_star(self.graph_2, "A", "J")

        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)
