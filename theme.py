import sublime, sublime_plugin

class ThemeAutoComplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if 1 < len(locations) or not view.score_selector(locations[0], 'meta.theme.bigine'):
            return ([], sublime.INHIBIT_WORD_COMPLETIONS)
        options = []
        options2 = []
        command = '主题：'
        if prefix[0:3] == command:
            themes = {
                'dahao': '默认主题',
                'fl9t': '凤唳九天',
                '100': '高考恋爱100天'
            }
            prefix2 = prefix[3:]
            for id in themes:
                pos = id.find(prefix2)
                if -1 == pos:
                    continue
                option = (prefix + "\t" + themes[id], command + id)
                if pos:
                    options2.append(option)
                else:
                    options.append(option)
        return (options + options2, sublime.INHIBIT_WORD_COMPLETIONS)
