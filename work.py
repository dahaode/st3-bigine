import sublime, sublime_plugin, sublime_lib, os, tempfile, webbrowser

class WorkCommand(sublime_lib.WindowAndTextCommand):
    def run(self, edit=None):
        if len(self.view.find_by_selector('invalid.illegal.bigine') or self.view.get_regions('bigine.error.theme') or self.view.get_regions('bigine.error.suite')):
            sublime.error_message('源代码中存在错误，请处理 :-(')
            return
        if self.view.is_dirty():
            self.view.run_command('save')
            if self.view.is_dirty():
                sublime.error_message('自动保存失败 :-(')
                return
        tpl_file = os.path.dirname(sublime.packages_path()) + '/' + os.path.dirname(self.view.settings().get('syntax')) + '/work.html'
        fh = open(tpl_file)
        tpl = fh.read(os.path.getsize(tpl_file))
        fh.close()
        src_file = self.view.file_name()
        fh = open(src_file, encoding='utf-8')
        src = fh.read(os.path.getsize(src_file))
        fh.close()
        html_file = tempfile.gettempdir() + '/bigine.draft.html'
        fh = open(html_file, 'w+', encoding='utf-8')
        fh.write(tpl % src)
        fh.close()
        webbrowser.open_new_tab('file://' + html_file)
