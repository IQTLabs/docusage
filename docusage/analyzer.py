from typing import Iterable
from langchain.document_loaders import UnstructuredFileLoader
from langchain.indexes import VectorstoreIndexCreator

default_prompt = "What would be important to know about this document?"
template_prompt = "How does this document relate to {source}?"


class Mission:
    def __init__(self, docs: Iterable[str], description: str = None):
        loaders = [UnstructuredFileLoader(path) for path in docs]
        self.index = VectorstoreIndexCreator().from_loaders(loaders)
        if description is None:
            self.description = default_prompt
        else:
            self.description = template_prompt.format(source=description)

    def write_report(self) -> str:
        return self.index.query(self.description)

    def write_report_with_sources(self) -> str:
        return self.index.query_with_sources(self.description)
