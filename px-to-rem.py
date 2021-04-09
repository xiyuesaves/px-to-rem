
import sublime
import sublime_plugin
import re
import time
import os

SETTINGS = {}
lastCompletion = {"needFix": False, "value": None, "region": None}

    # 插件加载完成
def plugin_loaded():
    # 调用初始化设置
    init_settings()

    # 初始化设定
def init_settings():
    # 从配置文件获取设置
    get_settings()
    # 应该是动态监听配置文件变动的
    sublime.load_settings('px-to-rem.sublime-settings').add_on_change('get_settings', get_settings)

    # 从配置文件加载设置
def get_settings():
    settings = sublime.load_settings('px-to-rem.sublime-settings')
    SETTINGS['fontsize'] = settings.get('fontsize', 16)
    SETTINGS['precision'] = settings.get('precision', 8)
    SETTINGS['exts'] = settings.get('exts', [".css", ".scss", ".less", ".sass", ".styl"])
    SETTINGS['leadingzero'] = settings.get('leadingzero', False)
    SETTINGS['firstline'] = settings.get('firstline', '')
    SETTINGS['reservedunit'] = settings.get('reservedunit', False)

    # 获取设定中某一项值
def get_setting(view, key):
    return view.settings().get(key, SETTINGS[key]);

    # 插件的事件监听
class CssRemCommand(sublime_plugin.EventListener):
    def on_text_command(self, view, name, args):
        if name == 'commit_completion':
            view.run_command('replace_rem')
        return None

    def on_query_completions(self, view, prefix, locations):
        # print('px-to-rem start {0}, {1}'.format(prefix, locations))

        # 判断是否符合文件类型不符合直接return出去
        fileName, fileExtension = os.path.splitext(view.file_name())
        # 添加判断首行是否含有特定字符串
        firstLine = view.substr(view.line(0))
        match = re.search("(" + get_setting(view, 'firstline') + ")+", firstLine)
        # print(firstLine, match, match == None)
        if not fileExtension.lower() in get_setting(view, 'exts') or match == None:
            return []

        # 重置完成对比
        lastCompletion["needFix"] = False
        location = locations[0]
        snippets = []

        # 计算出rem值
        match = re.compile("(-?[\d.]+)p(x)?").match(prefix)
        if match:
            lineLocation = view.line(location)
            line = view.substr(sublime.Region(lineLocation.a, location))
            value = match.group(1)

            # 修复值类似"0.5px"
            segmentStart = line.rfind(" ", 0, location)
            if segmentStart == -1:
                segmentStart = 0
            segmentStr = line[segmentStart:location]

            segment = re.compile("(-?[\d.])+" + value).search(segmentStr)
            if segment:
                value = segment.group(0)
                start = lineLocation.a + segmentStart + 0 + segment.start(0)
                lastCompletion["needFix"] = True
            else:
                start = location

            remValue = round(float(value) / get_setting(view, 'fontsize'), get_setting(view, 'precision'))

            # 删除无用的".0"
            intValue = int(remValue)
            if intValue == remValue:
                remValue = intValue

            strRem = str(remValue)

            # 删除前导零
            if (get_setting(view, 'leadingzero') == False) and (remValue < 1.0):
                strRem = strRem[1:]

            # 如果值是0则删除单位
            if remValue != 0:
                strRem += 'rem'
            else:
                strRem = '0'

            # 保存以进行替换
            lastCompletion["value"] = strRem
            lastCompletion["region"] = sublime.Region(start, location)

            commentStr = '';
            if (fileExtension.lower() in [".sass", ".scss", ".styl", ".less"]):
                commentStr = '; // ' + value + 'px';
            else:
                commentStr = '/* ' + value + 'px */';

            if re.compile("(-){1}").match(prefix):
                strRem = '-' + strRem

            # set completion snippet
            if get_setting(view, 'reservedunit'):
                snippets += [(value + 'px -> ' + strRem + '(keep px value)', strRem + commentStr)]
            else:
                snippets += [(value + 'px -> ' + strRem + '(' + str(get_setting(view, 'fontsize')) + 'px/rem)', strRem)]
        return snippets

class ReplaceRemCommand(sublime_plugin.TextCommand):
    def run(self, view, args):
        needFix = lastCompletion["needFix"]
        if needFix == True:
            value = lastCompletion["value"]
            region = lastCompletion["region"]
            # print('replace: {0}, {1}'.format(value, region))
            view.replace(region, value)
            view.end_edit()
