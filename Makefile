LATEXMK=latexmk

all:
	$(LATEXMK) -pdf
	scp proj_desc.pdf supernova:~/public_html/bioe

clean:
	$(LATEXMK) -CA
