import sublime_plugin

class BigineNewCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.new_file()
        view.set_syntax_file('Packages/Bigine/Bigine.tmLanguage')
        view.set_name('untitled.bws')
        view.run_command('insert_snippet', {
            'name': 'Packages/Bigine/Snippets/new.sublime-snippet'
        })
