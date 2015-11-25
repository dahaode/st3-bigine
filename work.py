import sublime, sublime_plugin, os, tempfile, webbrowser

class WorkCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        if len(view.find_by_selector('invalid.illegal.bigine') or view.get_regions('bigine.error.theme') or view.get_regions('bigine.error.suite')):
            sublime.error_message('源代码中存在错误，请处理 :-(')
            return
        if view.is_dirty():
            view.run_command('save')
            if view.is_dirty():
                sublime.error_message('自动保存失败 :-(')
                return
        tpl_file = os.path.dirname(sublime.packages_path()) + '/' + os.path.dirname(view.settings().get('syntax')) + '/work.html'
        fh = open(tpl_file)
        tpl = fh.read(os.path.getsize(tpl_file))
        fh.close()
        src_file = view.file_name()
        fh = open(src_file, encoding='utf-8')
        src = fh.read(os.path.getsize(src_file))
        fh.close()
        html_file = tempfile.gettempdir() + '/bigine.draft.html'
        fh = open(html_file, 'w+', encoding='utf-8')
        fh.write(tpl % src)
        fh.close()
        webbrowser.open_new_tab('file://' + html_file)
