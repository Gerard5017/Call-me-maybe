import argparse


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the application.

    Returns:
        The parsed command-line arguments as a Namespace object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--functions_definition", type=str,
                        default="data/input/functions_definition.json")
    parser.add_argument("--input", type=str,
                        default="data/input/function_calling_tests.json")
    parser.add_argument("--output", type=str,
                        default="data/output/function_calls.json")

    return parser.parse_args()
