# 🧙‍♂️ DocuSage

Welcome to DocuSage - a fast, automated, and AI-fueled document analysis tool. Harnessing the power of advanced Large Language Models (LLMs), DocuSage is your platform to surf through mountains of data and pinpoint important information from your documents.

Imagine having an intelligent assistant, ready to dive into the haystack of information, pulling out not just the needle but the essential threads of value. That's DocuSage for you - your personal intelligence analyst, on call 24/7.

DocuSage accepts custom intelligence missions and capably handles multiple documents simultaneously, not only simplifying but enriching your document analysis tasks. It ensures you don't miss those crucial "needle-in-the-haystack" insights that can easily get lost in the sea of information.

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

### OpenAI API Key Requirement

To use DocuSage, you need to have an account with OpenAI and an associated API key. The API key is used to interact with OpenAI's models, which are at the core of DocuSage's document analysis capabilities.

Here are the steps you need to follow to set up the OpenAI API key:

1. Create an account on the [OpenAI website](https://platform.openai.com/signup/).

2. After logging into your account, go to the API section. Here, you will find your API key. 

3. Set your OpenAI API key as an environment variable named `OPENAI_API_KEY` in your system.

    On Unix-based systems (like Linux or macOS), you can add the following line to your shell profile file (like `.bashrc`, `.bash_profile`, or `.zshrc`):

    ```bash
    export OPENAI_API_KEY="your-api-key"
    ```

    On Windows, you can set environment variables in the System Properties.

Remember to replace `"your-api-key"` with your actual OpenAI API key.

⚠️ **IMPORTANT:** Your OpenAI API key is sensitive information. Do not share it with others or expose it in public places like GitHub repositories.

## License

DocuSage is licensed under the terms of the Apache License.

## Contact

If you have any questions, feedback, or want to get involved in the DocuSage project, please feel free to reach out by opening an issue on our GitHub repository.