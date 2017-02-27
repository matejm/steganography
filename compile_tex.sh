# latex compile first time
pdflatex -shell-escape steganography.tex
read -n1 -r -p 'Press any key to continue...' foo

# compile bibliography
bibtex steganography
read -n1 -r -p 'Press any key to continue...' foo

# complile twice -> to make all refferences work
pdflatex -shell-escape steganography.tex
pdflatex -shell-escape steganography.tex

# cleanup
rm steganography.log steganography.aux steganography.toc steganography.bbl steganography.run.xml steganography-blx.bib steganography.blg
