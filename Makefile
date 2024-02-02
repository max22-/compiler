SRC = program.txt
TAL = $(SRC:.txt=.tal)
ROM = $(TAL:.tal=.rom)
COMPILER = compiler.py
PY = $(wildcard *.py)

all: $(ROM)

$(ROM): $(TAL)
	uxnasm $< $@

$(TAL): $(SRC) $(PY)
	@echo $(PY)
	./$(COMPILER) $< $@

run: $(ROM)
	uxnemu $(ROM)

clean:
	rm -f $(TAL) $(ROM)
