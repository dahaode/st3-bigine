import sublime, sublime_plugin, re

class StateHandler(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if not len(view.find_by_selector('text.bigine')):
            return []
        if 1 < len(locations) or not view.score_selector(locations[0], 'meta.action.state'):
            return ([], sublime.INHIBIT_WORD_COMPLETIONS)
        pos = prefix.find('（')
        options = []
        options2 = []
        if 0 < pos:
            pos += 1
            command = prefix[0:pos]
            prefix2 = prefix[pos:]
            registry = {}
            for region in view.find_by_selector('variable.other.bigine'):
                name = view.substr(region)
                if name in registry:
                    continue
                registry[name] = 1
                pos = name.find(prefix2)
                if -1 == pos:
                    continue
                option = (prefix + "\t" + name, command + name)
                if pos:
                    options2.append(option)
                else:
                    options.append(option)
        return (options + options2, sublime.INHIBIT_WORD_COMPLETIONS)
