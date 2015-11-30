package = Bigine.sublime-package
files = $(wildcard Bigine.tm*) \
	Bigine.sublime-settings Bigine.sublime-build Main.sublime-menu \
	$(shell ls Default*.sublime-keymap | sed 's/ /?/g') \
	$(wildcard Completions/*.sublime-completions) \
	$(wildcard Snippets/*.sublime-snippet) \
	$(wildcard *.py) bootstrap.html CHANGELOG.md
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
