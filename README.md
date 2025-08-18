# README file for the kashubian-parser project written in Python 3.

This software preprocesses, tokenizes, and performs a morphological analysis of Kashubian-language texts with the optional assistance of a **PostgreSQL** lexical database to allow for morphological disambiguation.

Output can either be written as JSON-formatted plain text to text files or to a MongoDB database if preferred.

The following run configurations are recommended to test out the software on the texts provided.

  python parse.py -f "/Texts/Ana_Ch1.txt"

	python parse.py -f "/Texts/Ana_pure_text.txt"

The first configuration runs on the first chapter of the Kashubian translation of *Anne of Green Gables*.
The second runs on the full text of the novel, and gives an idea of how long parsing typically takes.

