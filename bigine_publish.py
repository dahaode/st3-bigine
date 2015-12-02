import sublime, sublime_plugin, os, tempfile, webbrowser

class BiginePublishCommand(sublime_plugin.WindowCommand):
    def run(self):
        if not self._ok():
            return
        view = self.window.active_view()
        if len(view.find_by_selector('invalid.illegal.bigine') or view.get_regions('bigine.error.theme') or view.get_regions('bigine.error.suite')):
            sublime.error_message('源代码中存在错误，请处理 ₍₍ (̨̡ ‾᷄ᗣ‾᷅ )̧̢ ₎₎')
            return
        if view.is_dirty():
            view.run_command('save')
            if view.is_dirty():
                sublime.error_message('自动保存失败 ₍₍ (̨̡ ‾᷄ᗣ‾᷅ )̧̢ ₎₎')
                return
        src_file = view.file_name()
        if not src_file:
            sublime.error_message('空作品无法发布 ₍₍ (̨̡ ‾᷄ᗣ‾᷅ )̧̢ ₎₎')
            return
        fh = open(src_file, encoding='utf-8')
        src = fh.read(os.path.getsize(src_file))
        fh.close()
        tpl = sublime.load_resource(os.path.dirname(view.settings().get('syntax')) + '/Resources/bootstrap.html')
        html_file = tempfile.gettempdir() + '/bigine.draft.html'
        fh = open(html_file, 'w+', encoding='utf-8')
        fh.write(tpl % src)
        fh.close()
        webbrowser.open_new_tab('file://' + html_file)

    def _ok(self):
        return 0 < self.window.active_view().score_selector(0, 'text.bigine')

    def is_enabled(self):
        return self._ok()
