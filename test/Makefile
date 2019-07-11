test.pdf : test.md
	#pandoc $< -t json | python3 ../pandoc_include.py | pandoc -f json -o test.pdf
	pandoc $< --filter pandoc-include -o test-out.pdf
	pandoc $< --filter pandoc-include -o test-out.md

.PHONY: clean

clean:
	rm -f test-out.md test-out.pdf test.out

