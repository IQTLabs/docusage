# DocuSage

DocuSage analyzes documents using Large Language Models (LLMs), providing summaries and contextual information based on user specified missions.

## Installation

To install DocuSage, you will first need to install Poetry, a tool for Python dependency management. You can install Poetry by following the instructions on the [official Poetry website](https://python-poetry.org/docs/).

Once you have installed Poetry, you can clone this repository and install the dependencies:

```bash
git clone https://github.com/tensorspace-ai/docusage.git
cd docusage
poetry install
```

## Usage

Example command line usage:

```bash
docusage ./doc1.txt ./doc2.txt --mission "Novel weapons systems"
```

In this command, `docusage` is the command-line interface for our tool. The arguments `./doc1.txt` and `./doc2.txt` are the files that we want to analyze. You can provide as many files as you want.

The `--mission` or `-m` option allows you to specify a mission prompt, such as "Novel weapons systems". This prompt guides the analysis report that DocuSage creates based on the provided documents.

After running this command, DocuSage will process the provided files and display the results. Note that the `--mission` option is optional. If you don't provide a prompt, DocuSage will perform a default analysis of the documents.

## License

DocuSage is licensed under the terms of the Apache License.

## Contact

If you have any questions, feedback, or want to get involved in the DocuSage project, please feel free to reach out by opening an issue on our GitHub repository.