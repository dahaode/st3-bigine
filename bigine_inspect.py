import sublime, sublime_plugin, webbrowser

class BigineInspectCommand(sublime_plugin.TextCommand):
    _point = None
    _clob = None
    _type = ''
    _actions = {
        '进入房间': 'fangjianlei',
        '设置房间': 'fangjianlei',
        '移动中止': 'fangjianlei',
        '设置时间': 'shijianlei',
        '时刻': 'shijianlei',
        '人物出场': 'renwulei',
        '设置人物': 'renwulei',
        '人物移动': 'renwulei',
        '改变神态': 'renwulei',
        '人物离场': 'renwulei',
        '姿态': 'renwulei',
        '播放音乐': 'yinyuelei',
        '环境音乐': 'yinyuelei',
        '停止音乐': 'yinyuelei',
        '环境静音': 'yinyuelei',
        '音乐': 'yinyuelei',
        '播放音效': 'yinxiaolei',
        '停止音效': 'yinxiaolei',
        '音效': 'yinxiaolei',
        '设置音量': 'yinlianglei',
        '展示特写': 'texielei',
        '关闭特写': 'texielei',
        '特写': 'texielei',
        '切幕动画': 'qiemudonghua',
        '抖动镜头': 'donghualei',
        '放大镜头': 'donghualei',
        '设置镜头': 'donghualei',
        '移动镜头': 'donghualei',
        '复位镜头': 'donghualei',
        '神态动画': 'donghualei',
        '停顿': 'donghualei',
        '旁白': 'pangbai',
        '对白': 'duibai',
        '独白': 'dubai',
        '提示': 'tishi',
        '全屏文本': 'quanpingwenben',
        '清除文本': 'quanpingwenben',
        '隐藏文本': 'quanpingwenben',
        '文字颜色': 'wenziyanse',
        '文字效果': 'wenzixiaoguo',
        '自动播放': 'zidongbofang',
        '自动存档': 'zidongcundang',
        '游戏完结': 'youxiwanjie',
        '选择': 'xuanze',
        '如果': 'ruguo',
        '那么': 'name',
        '否则': 'fouze',
        '定义选择': 'dingyixuanze',
        '添加选项': 'dingyixuanze',
        '去除选项': 'dingyixuanze',
        '设置数据': 'shezhishuju',
        '定义数据': 'shezhishuju',
        '增加数据': 'zengjiashuju',
        '随机数据': 'suijishuju',
        '数据合值': 'shujuhezhi',
        '数据差值': 'shujuchazhi',
        '复制数据': 'fuzhishuju',
        '最大数据': 'zuidashuju&zuixiaoshuju',
        '最小数据': 'zuidashuju&zuixiaoshuju',
        '显示数据': 'xianshishuju',
        '当数据': 'dangshuju',
        '当时间': 'dangshijian',
        '且': 'qie&huo',
        '或': 'qie&huo',
        '对比数据': 'duibishuju',
        '如果数据': 'ruguoshuju',
        '循环': 'xunhuan',
        '循环中止': 'xunhuan',
        '地图': 'ditu',
        '交互点': 'ditu',
        '底图': 'ditu',
        '高亮': 'ditu',
        '区域': 'ditu',
        '对应房间': 'ditu',
        '使用地图': 'ditu',
        '房间': 'dingyifangjian',
        '状态': 'jishizhuangtai',
        '隐藏状态栏': 'yincangzhuangtailan',
        '显示状态栏': 'xianshizhuangtailan',
        '面板': 'jiandanmianban',
        '简单面板': 'jiandanmianban',
        '条目': 'jiandanmianban',
        '数据名': 'jiandanmianban',
        '数据类别': 'jiandanmianban',
        '集合面板': 'jihemianban',
        '使用集合': 'jihemianban',
        '集合结构': 'jihemianban',
        '结构': 'jihemianban',
        '字段': 'jihemianban',
        '头像': 'jihemianban',
        '定义集合': 'jihemianban',
        '上限': 'jihemianban',
        '事件': 'luoji',
        '类型': 'luoji',
        '条件': 'luoji',
        '类别': 'luoji',
        '内容': 'luoji',
        '素材包': 'sucaibao',
        '主题': 'zhuti',
        '人物': 'renwu',
        '主角': 'zhujue'
#        '游戏失败': 'youxishibai',
#        '评分': 'pingfen',
#        '设置天气': 'shezhitianqi',
#        '音源': 'yinyue',
#        '画面': 'texie',
#        '天气': 'yinxiao',
    }

    def run(self, edit):
        if not self._check():
            return
        if '素材包' == self._type:
            webbrowser.open_new_tab('http://dahao.de/bigine/course/sucaibaoxiangguan.html#title')
            # url = 'sucaibao/#' + self._clob
        elif '主题' == self._type:
            webbrowser.open_new_tab('http://dahao.de/bigine/course/zhutidexuanze.html#title')
            # url = 'zhuti/#' + self._clob
        elif self._clob == '人物' or self._clob == '主角':
            webbrowser.open_new_tab('http://dahao.de/bigine/course/dingyirenwu.html#title')
        elif self._clob in self._actions:
            url = self._actions[self._clob] + '.html'
        else:
            url = ''
        if url:
            webbrowser.open_new_tab('http://dahao.de/yinqing/' + url + '#title')

    def _check(self):
        view = self.view
        pos = view.sel()[0].begin()
        if self._point == pos:
            return '' != self._type
        if not view.score_selector(pos, 'text.bigine'):
            self._clob = ''
            self._type = ''
            return False
        self._point = pos
        if view.score_selector(pos, 'meta.bigine.suite'):
            self._clob = view.substr(view.extract_scope(pos))
            found = self._clob.find('：')
            self._clob = self._clob[1 + found:]
            self._type = '素材包'
            return True
        if view.score_selector(pos, 'meta.bigine.theme'):
            self._clob = view.substr(view.extract_scope(pos))
            found = self._clob.find('：')
            self._clob = self._clob[1 + found:]
            self._type = '主题'
            return True
        if view.score_selector(pos, 'meta.bigine - meta.bigine.literal'):
            self._clob = view.substr(view.line(pos)).strip()
            found = self._clob.find('：')
            if -1 != found:
                self._clob = self._clob[0:found]
            found = self._clob.find('（')
            if -1 != found:
                self._clob = self._clob[0:found]
            self._type = '语法'
            return True
        self._clob = ''
        self._type = '其它'
        return True

    def is_enabled(self):
        self._check()
        return '' != self._clob

    def is_visible(self):
        return self._check()

    def description(self):
        if not self._check() or '其它' == self._type:
            return ''
        return self._type
