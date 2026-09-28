import unittest

from logictree.prompts.story import EXAMPLE_DICT, PROMPT_TEMPLATE_DICT


class StoryPromptTests(unittest.TestCase):
    def test_every_template_accepts_standard_fields(self):
        for output_format, template in PROMPT_TEMPLATE_DICT.items():
            rendered = template.format(
                examples_block=EXAMPLE_DICT[output_format],
                entities={"P0": "An event happened."},
                premise_events={"P0": "An event happened."},
                reasoning=["P0 therefore Q0"],
                reasoning_skeleton=["P0 therefore Q0"],
            )
            self.assertTrue(rendered.strip())
