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
            if 200 != resp.status:
                conn.close()
                raise ValueError('')
            self.__suites = json.loads(resp.read().decode('utf-8'))
            conn.close()
            view.erase_status(key)
        except:
            view.set_status(key, '读取素材包列表…失败')
            self.__suites = {}
        self.__loading = False
        return 0 < len(self.__suites)

    def __load(self, view):
        if self.__loading:
            return False
        regions = view.find_by_selector('meta.bigine.suite constant.language')
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
            if 200 != resp.status:
                conn.close()
                raise ValueError('')
            self.__entities = {
                'id': id
            }
            data = json.loads(resp.read().decode('utf-8'))
            for type in ['ses', 'bgms', 'cgs', 'rooms', 'chars']:
                self.__entities[type] = []
                if type in data:
                    for id in data[type]:
                        obj = {
                            'id': data[type][id]['title']
                        }
                        if 'poses' in data[type][id]:
                            obj['meta'] = []
                            for item in data[type][id]['poses']:
                                obj['meta'].append(item)
                        self.__entities[type].append(obj)
            conn.close()
            view.erase_status(key)
        except:
            view.set_status(key, '读取素材包内实体列表…失败')
            self.__entities = {}
        self.__loading = False
        return 0 < len(self.__entities)

    def __validate_suite(self, view):
        if not self.__list(view):
            return
        regions = view.find_by_selector('meta.bigine.suite constant.language')
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

    def __complete_suite(self, view, prefix):
        options = []
        options2 = []
        command = prefix[0:4]
        prefix2 = prefix[4:]
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

    def __complete_entity(self, view, prefix, location):
        patterns = []
        for scope in view.scope_name(location).split():
            if 'meta.bigine.ref.' == scope[0:16]:
                pattern = scope[16:].split('.')
                if 'pose' == pattern[1]:
                    continue
                pattern[1] += 's'
                if 'colon' == pattern[0]:
                    pattern[0] = '：'
                elif 'comma' == pattern[0]:
                    pattern[0] = '，'
                else:
                    pattern[0] = '（'
                patterns.append(pattern)
        if not len(patterns):
            return []
        pos = -1
        for pattern in patterns:
            test = prefix.rfind(pattern[0])
            if test > pos:
                pos = test
                symbol, type = pattern
        print(patterns, pos, type, symbol)
        if type not in self.__entities or -1 == pos:
            return []
        options = []
        options2 = []
        pos += 1
        command = prefix[0:pos]
        prefix2 = prefix[pos:]
        for entity in self.__entities[type]:
            pos = entity['id'].find(prefix2)
            print(entity['id'], pos)
            if -1 == pos:
                continue
            option = (prefix + "\t" + entity['id'], command + entity['id'])
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
        if view.score_selector(locations[0], 'meta.bigine.suite'):
            return __inhibit(self.__complete_suite(view, prefix))
        if view.score_selector(locations[0], 'meta.bigine.ref - meta.bigine.ref.bracket.state'):
            return __inhibit(self.__complete_entity(view, prefix, locations[0]))
