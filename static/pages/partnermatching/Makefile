# Makes html or pdf file from pairmatching source Markdown

BASENAME = partnermatching
HTMLOPTS = --mathml --css styles/$(BASENAME).css  --include-in-header=header.html
SLIDEOPTS = --mathml --css styles/$(BASENAME)-slides.css --include-in-header=header.html -V slidy-url="." -t slidy
PDFOPTS =
PDFSLIDEOPTS = -t beamer

html: $(BASENAME).html

$(BASENAME).html: $(BASENAME).md
	pandoc -s $(HTMLOPTS)   $(BASENAME).md -o $(BASENAME).html

slides: $(BASENAME)-slides.html

$(BASENAME)-slides.html: $(BASENAME)-slides.md
	pandoc -s $(SLIDEOPTS) $(BASENAME)-slides.md -o $(BASENAME)-slides.html


pdf: $(BASENAME).pdf

$(BASENAME).pdf: $(BASENAME).md
	pandoc -s $(PDFOPTS) $(BASENAME).md -o $(BASENAME).pdf

pdfslides: $(BASENAME)-slides.pdf

$(BASENAME)-slides.pdf: $(BASENAME)-slides.md
	pandoc $(PDFSLIDEOPTS) $(BASENAME)-slides.md -o $(BASENAME)-slides.pdf

all: html slides pdf pdfslides
