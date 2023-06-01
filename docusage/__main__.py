import os
import argparse


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError(
            "The environment variable OPENAI_API_KEY is not set. You must have a paid OpenAI account to use DocuSage."
        )

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
