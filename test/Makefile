
test.pdf : test.md
	pandoc $< -t json | python3 ../pandoc_include.py | pandoc -f json -o test.pdf

