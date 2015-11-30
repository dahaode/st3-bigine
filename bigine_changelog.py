import sublime, sublime_plugin

class BigineChangelogCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.new_file()
        view.set_syntax_file('Packages/Markdown/Markdown.tmLanguage')
        view.set_name('CHANGELOG')
        view.run_command('insert', {
            'characters': sublime.load_resource('Packages/Bigine/CHANGELOG.md')
        })
        view.set_read_only(True)
        view.set_scratch(True)
