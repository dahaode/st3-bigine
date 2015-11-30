package = Bigine.sublime-package
files = Bigine.sublime-build Bigine.sublime-settings Main.sublime-menu bootstrap.html \
	$(wildcard Bigine.tm*) \
	$(wildcard Completions/*.sublime-completions) \
	$(wildcard Snippets/*.sublime-snippet) \
	$(shell ls Default*.sublime-keymap | sed 's/ /?/g') \
	$(wildcard *.py)
sp:=
sp+=
lb:=(
rb:=)

.PHONY: dist clean

dist: $(package)

$(package): $(files)
	zip -9rq "$@" $(subst ?,\$(sp), $(subst $(rb),\$(rb), $(subst $(lb),\$(lb), $(files))))

clean:
	$(RM) $(package)
