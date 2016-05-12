import sublime, sublime_plugin, webbrowser

class BigineInspectCommand(sublime_plugin.TextCommand):
    _point = None
    _clob = None
    _type = ''
    _actions = {
        '音乐': 'yinyue',
        '音源': 'yinyue',
        '画面': 'texie',
        '特写': 'texie',
        '人物': 'renwu',
        '头像': 'renwu',
        '姿态': 'renwu',
        '地图': 'ditu',
        '底图': 'ditu',
        '交互点': 'ditu',
        '高亮': 'ditu',
        '区域': 'ditu',
        '对应房间': 'ditu',
        '房间': 'fangjian',
        '使用地图': 'fangjian',
        '时刻': 'fangjian',
        '音效': 'yinxiao',
        '天气': 'yinxiao',
        '自动播放': 'zidongbofang',
        '主角': 'zhujue',
        '素材包': 'sucaibao',
        '主题': 'zhuti',
        '事件': 'shijian',
        '类型': 'leixing',
        '条件': 'tiaojian',
        '内容': 'neirong',
        '人物出场': 'renwuchuchang',
        '人物离场': 'renwulichang',
        '设置人物': 'shezhirenwu',
        '改变神态': 'gaibianshentai',
        '人物移动': 'renwuyidong',
        '独白': 'dubai',
        '对白': 'duibai',
        '提示': 'tishi',
        '旁白': 'pangbai',
        '自动存档': 'zidongcundang',
        '游戏完结': 'youxiwanjie',
        '游戏失败': 'youxishibai',
        '评分': 'pingfen',
        '播放音乐': 'bofangyinyue',
        '关闭特写': 'guanbitexie',
        '展示特写': 'zhanshitexie',
        '设置房间': 'shezhifangjian',
        '移动中止': 'yidongzhongzhi',
        '设置时间': 'shezhishijian',
        '进入房间': 'jinrufangjian',
        '播放音效': 'bofangyinxiao',
        '设置天气': 'shezhitianqi',
        '停止音乐': 'tingzhiyinyue',
        '当数据': 'dangshuju',
        '设置数据': 'shezhishuju',
        '对比数据': 'duibishuju',
        '增加数据': 'zengjiashuju',
        '循环中止': 'xunhuanzhongzhi',
        '最大数据': 'zuidashuju',
        '最小数据': 'zuixiaoshuju',
        '选择': 'xuanze',
        '随机数据': 'suijishuju',
        '当时间': 'dangshijian',
        '复制数据': 'fuzhishuju',
        '数据合值': 'shujuhezhi',
        '数据差值': 'shujuchazhi',
        '定义选择': 'dingyixuanze',
        '添加选项': 'tianjiaxuanxiang',
        '去除选项': 'quchuxuanxiang',
        '且': 'qie',
        '或': 'huo',
        '否则': 'fouze',
        '那么': 'name',
        '如果': 'ruguo',
        '循环': 'xunhuan',
        '如果数据': 'ruguoshuju',
        '状态': 'zhuangtai',
        '面板': 'jiandanmianban',
        '简单面板': 'jiandanmianban',
        '条目': 'tiaomu',
        '数据名': 'shujuming',
        '数据类别': 'shujuleibie',
        '集合面板': 'jihemianban',
        '使用集合': 'shiyongjihe',
        '集合结构': 'jihejiegou',
        '结构': 'jiegou',
        '字段': 'ziduan',
        '类别': 'leibie',
        '定义数据': 'dingyishuju',
        '定义集合': 'dingyijihe',
        '切幕动画': 'qiemudonghua',
        '抖动镜头': 'doudongjingtou',
        '放大镜头': 'fangdajingtou',
        '设置镜头': 'shezhijingtou',
        '移动镜头': 'yidongjingtou',
        '复位镜头': 'fuweijingtou',
        '停顿': 'tingdun'
    }

    def run(self, edit):
        if not self._check():
            return
        if '素材包' == self._type:
            url = 'sucaibao/#' + self._clob
        elif '主题' == self._type:
            url = 'zhuti/#' + self._clob
        elif self._clob in self._actions:
            url = self._actions[self._clob] + '.html'
        else:
            url = ''
        if url:
            webbrowser.open_new_tab('http://dahao.de/yinqing/' + url)

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
