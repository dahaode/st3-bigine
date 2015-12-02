import sublime, sublime_plugin

class BigineInspectCommand(sublime_plugin.TextCommand):
    _point = None
    _clob = None
    _type = ''

    def run(self, edit):
        if not self._check():
            return
        sublime.message_dialog('查看 %s %s\nTo be continued...' % (self._type, self._clob))

    def _check(self):
        view = self.view
        pos = view.sel()[0].begin()
        if self._point == pos:
            return '' != self._type
        if not view.score_selector(pos, 'text.bigine'):
            self._clob = ''
            self._type = ''
            return False
        self._point = pos
        if view.score_selector(pos, 'meta.bigine.suite'):
            self._clob = view.substr(view.extract_scope(pos))
            found = self._clob.find('：')
            self._clob = self._clob[1 + found:]
            self._type = '素材包'
            return True
        if view.score_selector(pos, 'meta.bigine.theme'):
            self._clob = view.substr(view.extract_scope(pos))
            found = self._clob.find('：')
            self._clob = self._clob[1 + found:]
            self._type = '主题'
            return True
        if view.score_selector(pos, 'meta.bigine - meta.bigine.literal'):
            self._clob = view.substr(view.line(pos)).strip()
            found = self._clob.find('：')
            if -1 != found:
                self._clob = self._clob[0:found]
            found = self._clob.find('（')
            if -1 != found:
                self._clob = self._clob[0:found]
            self._type = '语法'
            return True
        self._clob = ''
        self._type = '其它'
        return True

    def is_enabled(self):
        self._check()
        return '' != self._clob

    def is_visible(self):
        return self._check()

    def description(self):
        if not self._check() or '其它' == self._type:
            return ''
        return self._type
