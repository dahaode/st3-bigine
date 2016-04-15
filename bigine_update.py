import sublime, sublime_plugin, webbrowser, http.client, json, re

class BigineUpdateCommand(sublime_plugin.WindowCommand):
    __version = '0.2.1'

    def run(self):
        try:
            conn = http.client.HTTPConnection('s.dahao.de', timeout=3)
            conn.request('GET', '/tools/latest.json')
            resp = conn.getresponse()
            if 200 != resp.status:
                conn.close()
                raise ValueError('')
            # sublime.message_dialog(jsonCode)
            responseJSON = json.loads(resp.read().decode('utf-8'))
            conn.close()
            latestVersion = responseJSON["v"]
            isOK = False
            if self.__version != latestVersion:
                isOK = sublime.ok_cancel_dialog('检测到存在最新版本' + latestVersion + ', 是否进行更新？')
            if isOK:
                webbrowser.open_new_tab('http://dahao.de/yinqing/gongju.html')
        except:
            sublime.status_message('读取最新版本信息…失败 ₍₍ (̨̡ ‾᷄ᗣ‾᷅ )̧̢ ₎₎')