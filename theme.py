import sublime, sublime_plugin

class ThemeAutoComplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if 1 < len(locations):
            return ([], sublime.INHIBIT_WORD_COMPLETIONS)
        command = '主题：'
        pos = prefix.find(command)
        if pos:
            return ([], sublime.INHIBIT_WORD_COMPLETIONS)
        prefix2 = prefix[3:]
        themes = {
            'dahao': '默认主题',
            'fl9t': '凤唳九天',
            '100': '高考恋爱100天'
        }
        options = []
        options2 = []
        for id in themes:
            pos = id.find(prefix2)
            if -1 == pos:
                continue
            option = (command + "\t" + themes[id], command + id)
            if pos:
                options2.append(option)
            else:
                options.append(option)
        return (options + options2, sublime.INHIBIT_WORD_COMPLETIONS)
