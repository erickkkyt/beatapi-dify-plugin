from __future__ import annotations

import unittest

from tool_inputs import parse_image_urls


class ImageUrlInputTests(unittest.TestCase):
    def test_accepts_newline_comma_or_json_array_input(self) -> None:
        self.assertEqual(
            parse_image_urls(
                '["https://media.example.com/one.png", '
                '"https://media.example.com/two.jpg"]'
            ),
            [
                "https://media.example.com/one.png",
                "https://media.example.com/two.jpg",
            ],
        )
        self.assertEqual(
            parse_image_urls(
                "https://media.example.com/one.png,\n"
                "https://media.example.com/two.jpg"
            ),
            [
                "https://media.example.com/one.png",
                "https://media.example.com/two.jpg",
            ],
        )

    def test_rejects_non_https_or_more_than_seven_images(self) -> None:
        with self.assertRaisesRegex(ValueError, "public HTTPS"):
            parse_image_urls("http://media.example.com/one.png")

        with self.assertRaisesRegex(ValueError, "1 to 7"):
            parse_image_urls(
                "\n".join(
                    f"https://media.example.com/{index}.png" for index in range(8)
                )
            )


if __name__ == "__main__":
    unittest.main()
