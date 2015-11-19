import sublime, sublime_plugin, re

class StateAutoComplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if 1 < len(locations):
            return ([], sublime.INHIBIT_WORD_COMPLETIONS)
        match = re.match('(选择|(?:最[大小]|如果|当|对比|设置|增加)数据（)(.*)', prefix)
        if not match:
            return ([], sublime.INHIBIT_WORD_COMPLETIONS)
        command = match.group(1)
        prefix2 = match.group(2)
        registry = {}
        options = []
        options2 = []
        for region in view.find_by_selector('variable.other.bigine'):
            name = view.substr(region)
            pos = name.find(prefix2)
            if -1 == pos or name in registry:
                continue
            registry[name] = 1
            option = (command + "\t" + name, command + name)
            if pos:
                options2.append(option)
            else:
                options.append(option)
        return (options + options2, sublime.INHIBIT_WORD_COMPLETIONS)
