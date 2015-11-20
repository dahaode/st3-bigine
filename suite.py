import sublime, sublime_plugin, http.client, json

class SuiteHandler(sublime_plugin.EventListener):
    __suites = {}

    __loading = False

    __entities = {}

    def __list(self, view):
        if not len(view.find_by_selector('text.bigine')) or self.__loading:
            return False
        if len(self.__suites):
            return True
        key = 'bigine.status'
        self.__loading = True
        view.set_status(key, '读取素材包列表…')
        try:
            conn = http.client.HTTPConnection('api.dahao.de', timeout=3)
            conn.request('POST', '/resource', headers={
                'Origin': 'http://dahao.de'
            })
            resp = conn.getresponse()
            if 200 == resp.status:
                self.__suites = json.loads(resp.read().decode('utf-8'))
            conn.close()
        except:
            self.__suites = {}
        view.erase_status(key)
        self.__loading = False
        return 0 < len(self.__suites)

    def __load(self, view):
        if self.__loading:
            return False
        regions = view.find_by_selector('meta.suite.bigine constant.language')
        id = view.substr(regions[0])
        if 'id' in self.__entities and self.__entities['id'] == id:
            return True
        key = 'bigine.status'
        self.__loading = True
        view.set_status(key, '读取素材包内实体列表…')
        try:
            conn = http.client.HTTPConnection('api.dahao.de', timeout=10)
            conn.request('POST', '/resource/' + id, headers={
                'Origin': 'http://dahao.de'
            })
            resp = conn.getresponse()
            if 200 == resp.status:
                self.__entities = json.loads(resp.read().decode('utf-8'))
            conn.close()
        except:
            self.__entities = {}
        print(self.__entities)
        view.erase_status(key)
        self.__loading = False
        return 0 < len(self.__entities)

    def __validate_suite(self, view):
        if not self.__list(view):
            return
        regions = view.find_by_selector('meta.suite.bigine constant.language')
        key = 'bigine.error.suite'
        if 1 == len(regions) and (not len(self.__suites) or view.substr(regions[0]) in self.__suites):
            view.erase_regions(key)
            self.__load(view)
            return
        view.add_regions(key, regions, 'invalid.illegal.bigine')
        self.__entities = {}

    def on_new_async(self, view):
        self.__validate_suite(view)

    def on_load_async(self, view):
        self.__validate_suite(view)

    def on_modified_async(self, view):
        self.__validate_suite(view)

    def __complete_suites(self, view, prefix):
        options = []
        options2 = []
        command = prefix[0:4]
        prefix2 = prefix[4:]
        print(self.__suites)
        for id in self.__suites:
            pos = id.find(prefix2)
            if -1 == pos:
                continue
            option = (prefix + "\t" + self.__suites[id], command + id)
            if pos:
                options2.append(option)
            else:
                options.append(option)
        return options + options2

    def on_query_completions(self, view, prefix, locations):
        if not len(view.find_by_selector('text.bigine')):
            return []
        def __inhibit(list):
            return (list, sublime.INHIBIT_WORD_COMPLETIONS)
        if view.score_selector(locations[0], 'meta.suite.bigine'):
            return __inhibit(self.__complete_suites(view, prefix))
