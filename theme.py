import sublime, sublime_plugin, http.client, json

class ThemeHandler(sublime_plugin.EventListener):
    __themes = {}

    __loading = False

    def __list(self, view):
        if not len(view.find_by_selector('text.bigine')) or self.__loading:
            return False
        key = 'bigine.status'
        if len(self.__themes):
            return True
        self.__loading = True
        sublime.status_message('读取主题列表…')
        try:
            conn = http.client.HTTPConnection('s.dahao.de', timeout=3)
            conn.request('GET', '/theme/index.json')
            resp = conn.getresponse()
            if 200 != resp.status:
                conn.close()
                raise ValueError('')
            self.__themes = json.loads(resp.read().decode('utf-8'))
            conn.close()
            sublime.status_message('')
            view.set_status(key, '主题列表就绪')
        except:
            sublime.status_message('读取主题列表…失败 ₍₍ (̨̡ ‾᷄ᗣ‾᷅ )̧̢ ₎₎')
            self.__themes = {}
        self.__loading = False
        return 0 < len(self.__themes)

    def __validate(self, view):
        if not self.__list(view):
            return
        regions = view.find_by_selector('meta.bigine.theme constant.language')
        key = 'bigine.error.theme'
        if 1 == len(regions):
            sublime.status_message('')
            view.erase_regions(key)
            return
        sublime.status_message('无效的主题编号 ₍₍ (̨̡ ‾᷄ᗣ‾᷅ )̧̢ ₎₎')
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
