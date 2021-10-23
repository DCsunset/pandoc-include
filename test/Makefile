test.pdf : test.md entryTest/test.md ../pandoc_include/main.py
	pandoc $< -t json | python3 run.py | pandoc -f json -o test.pdf
	#pandoc $< --filter pandoc-include -o test-out.pdf
	#pandoc test.md --filter pandoc-include -o test-out.md
	#pandoc entryTest/test.md --filter pandoc-include -o entryTest/test-out.md

.PHONY: debug
debug:
	pandoc debug.md -t json | python3 run.py | pandoc -f json -o debug.pdf
	# pandoc debug.md --filter pandoc-include -o debug.pdf

.PHONY: clean
clean:
	rm -f test-out.md test-out.pdf test.pdf included/test.out debug.pdf

