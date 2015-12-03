import sublime, sublime_plugin

class StateHandler(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if not len(view.find_by_selector('text.bigine')):
            return []
        if 1 < len(locations) or not view.score_selector(locations[0], 'meta.bigine.ref.state'):
            return ([], sublime.INHIBIT_WORD_COMPLETIONS)
        pos1 = pos2 = pos3 = 0
        if view.score_selector(locations[0], 'meta.bigine.ref.state.bracket'):
            pos1 = prefix.rfind('（')
        if view.score_selector(locations[0], 'meta.bigine.ref.state.comma'):
            pos2 = prefix.rfind('，')
        pos = max(pos1, pos2)
        options = []
        options2 = []
        if 0 < pos:
            pos += 1
            command = prefix[0:pos]
            prefix2 = prefix[pos:]
            perline = False
        elif view.score_selector(locations[0], 'meta.bigine.ref.state.perline'):
            prefix2 = prefix
            perline = True
        else:
            return ([], sublime.INHIBIT_WORD_COMPLETIONS)
        registry = {}
        for region in view.find_by_selector('variable.other.state.bigine'):
            name = view.substr(region)
            if name in registry:
                continue
            registry[name] = 1
            pos = name.find(prefix2)
            if -1 == pos:
                continue
            if perline:
                option = (name, name)
            else:
                option = (prefix + "\t" + name, command + name)
            if pos:
                options2.append(option)
            else:
                options.append(option)
        return (options + options2, sublime.INHIBIT_WORD_COMPLETIONS)
