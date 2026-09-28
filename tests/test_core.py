import unittest

from logictree.core import (
    create_tree,
    gen_multi_step_data,
    generate_dataset,
    is_valid_parentheses,
    logic_tree_equal,
)


class CoreTests(unittest.TestCase):
    def test_parentheses_and_unicode_implication_are_parsed(self):
        self.assertTrue(is_valid_parentheses("((P0→Q0)&P0)"))
        self.assertFalse(is_valid_parentheses("((P0→Q0)"))

        tree = create_tree("(P0→Q0)")
        self.assertEqual(tree.sym, "→")
        self.assertEqual(tree.left.val, "P0")
        self.assertEqual(tree.right.val, "Q0")

    def test_generated_row_has_expected_schema(self):
        row = gen_multi_step_data(3)

        self.assertEqual(row["step"], 3)
        self.assertEqual(len(row["reasoning_process"]), 3)
        self.assertIn(row["logic_tree"][0], row["inodes"])
        self.assertTrue(row["leaf_nodes"])

    def test_generate_dataset_is_seeded_and_unique(self):
        first = generate_dataset({2: 3}, seed=7)
        second = generate_dataset({2: 3}, seed=7)

        self.assertEqual(first, second)
        self.assertEqual([row["num"] for row in first], [0, 1, 2])
        for index, row in enumerate(first):
            self.assertFalse(
                any(
                    logic_tree_equal(row["logic_tree"], other["logic_tree"])
                    for other in first[index + 1 :]
                )
            )
