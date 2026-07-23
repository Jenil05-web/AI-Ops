# "I included this module, then consciously decided chunking wasn't needed for short-form data, here's why

"""Chunking is not required for this project.

Unlike long-document RAG (PDFs, wikis, articles), our retrieval unit is
a single support ticket's text_input (subject + body) paired with its
answer. These are already short, self-contained units — chunking would
fragment context without adding retrieval value."""
