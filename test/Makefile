BIN ?= pandoc-include

test.pdf: test.md ../pandoc_include/main.py
	pandoc $< --filter $(BIN) -o test.pdf
	# pandoc $< -t json | python3 run.py | pandoc -f json -o test.pdf
	#pandoc $< --filter pandoc-include -o test-out.pdf
	#pandoc test.md --filter pandoc-include -o test-out.md
	#pandoc entryTest/test.md --filter pandoc-include -o entryTest/test-out.md

entryTest.pdf: entryTest/test.md ../pandoc_include/main.py
	pandoc $< --filter pandoc-include -o entry-test.pdf

.PHONY: debug
debug:
	# pandoc debug.md -t json | python3 run.py | pandoc -f json -o debug.pdf
	pandoc debug.md --filter pandoc-include -o debug.pdf

.PHONY: clean
clean:
	rm -f test-out.md test-out.pdf test.pdf included/test.out debug.pdf

.PHONY: nixpkgs
nixpkgs:
	pandoc test.md -t json | ${NIXPKGS}/result/bin/pandoc-include | pandoc -f json -o test.pdf

