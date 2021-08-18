test.pdf : test.md entryTest/test.md ../src/pandoc_include.py
	pandoc $< -t json | python3 ../src/pandoc_include.py | pandoc -f json -o test.pdf
	#pandoc $< --filter pandoc-include -o test-out.pdf
	#pandoc test.md --filter pandoc-include -o test-out.md
	#pandoc entryTest/test.md --filter pandoc-include -o entryTest/test-out.md

.PHONY: clean

clean:
	rm -f test-out.md test-out.pdf test.pdf included/test.out

