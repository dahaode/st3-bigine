import sublime, sublime_plugin

class ThemeHandler(sublime_plugin.EventListener):
    __themes = {
        'dahao': '默认主题',
        'fl9t': '凤唳九天',
        '100': '高考恋爱100天'
    }

    def __validate(self, view):
        if not len(view.find_by_selector('text.bigine')):
            return
        regions = view.find_by_selector('meta.bigine.theme constant.language')
        key = 'bigine.error.theme'
        if 1 == len(regions) and view.substr(regions[0]) in self.__themes:
            sublime.status_message('')
            view.erase_regions(key)
            return
        sublime.status_message('无效的主题编号 :-(')
        view.add_regions(key, regions, 'invalid.illegal.bigine')

    def on_new_async(self, view):
        self.__validate(view)

    def on_load_async(self, view):
        self.__validate(view)

    def on_modified_async(self, view):
        self.__validate(view)

    def on_query_completions(self, view, prefix, locations):
        if not len(view.find_by_selector('text.bigine')):
            return []
        if 1 < len(locations) or not view.score_selector(locations[0], 'meta.bigine.theme'):
            return ([], sublime.INHIBIT_WORD_COMPLETIONS)
        options = []
        options2 = []
        command = '主题：'
        prefix2 = prefix[3:]
        for id in self.__themes:
            pos = id.find(prefix2)
            if -1 == pos:
                continue
            option = (prefix + "\t" + self.__themes[id], command + id)
            if pos:
                options2.append(option)
            else:
                options.append(option)
        return (options + options2, sublime.INHIBIT_WORD_COMPLETIONS)
