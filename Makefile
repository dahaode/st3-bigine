package = Bigine.sublime-package
install = $(HOME)/Library/Application\ Support/Sublime\ Text\ 3/Installed\ Packages/$(package)
files = $(wildcard Bigine.tm*) \
	Bigine.sublime-settings Bigine.sublime-build Main.sublime-menu \
	$(shell ls Default*.sublime-keymap | sed 's/ /?/g') \
	$(shell ls Default*.sublime-mousemap | sed 's/ /?/g') \
	$(wildcard Completions/*.sublime-completions) \
	$(wildcard Snippets/*.sublime-snippet) \
	$(wildcard *.py) $(wildcard Resources/*)
sp:=
sp+=
lb:=(
rb:=)

.PHONY: dist clean c install i uninstall u

dist: $(package)

$(package): $(files)
	zip -9rq "$@" $(subst ?,\$(sp), $(subst $(rb),\$(rb), $(subst $(lb),\$(lb), $(files))))

clean:
	-$(RM) $(package)

c: clean

$(install): $(package)
	-cp -f "$<" "$@"

install: $(install)

i: install

uninstall:
	-$(RM) $(install)

u: uninstall
