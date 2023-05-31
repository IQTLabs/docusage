import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Analyze documents using Large Language Models."
    )
    parser.add_argument(
        "files", metavar="F", type=str, nargs="+", help="a list of files to be analyzed"
    )
    parser.add_argument(
        "--mission", "-m", type=str, required=False, help="an optional mission prompt"
    )

    args = parser.parse_args()

    files = args.files
    prompt = args.prompt

    print("Files:", files)
    if prompt:
        print("Prompt:", prompt)
