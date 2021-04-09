px-to-rem
-------------
一个输入px可转为rem的Sublime Text 3自动完成插件。

#### 与rem-unit的区别

* 修复负数无法转换的bug

* 增加选项是否保留px单位

* 新增首行激活字符串

  > (当文件首行含有指定字符串时,才激活转换功能,默认为空)

  ![首行字符串激活](firstline.gif)

##### 与CSSREM的区别
* 删除多余的小数 1.0rem -> 1rem
* 删除0px转换时多余的单位 0.0rem -> 0
* 增加 前导0的选择 0.25rem -> .25rem
* 增加 可在注释保留原始值 css使用块注释 其他语言行注释
* 增加默认支持文件类型.scss .styl
* TODO: 小数px起始替换位置不正确的bug 16.16px -> 16.1.01rem (should be 1.01rem)

##### 插件效果：（CSSREM）
![效果演示图](cssrem.gif)

#### 安装(Package Control)
* Ctrl+Shift+P 输入 Package Control: Install Packag
* 搜索 rem-unit-fix
* 重启 Sublime Text

##### 配置参数

参数配置文件：Sublime Text -> Preferences -> Package Settings -> rem-unit-fix

```json
{
    "fontsize": 16,
    "precision": 8,
    "leadingzero": false,
    "exts": [".css", ".scss", ".less", ".sass", ".styl"],
    "firstline": "",
    "reservedunit": false
}
```



* `fontsize` - html元素font-size值，默认为16。
* `precision` - px转rem的小数部分的最大长度，默认为8。
* `leadingzero` - 是否保留前导0，默认不保留。
* `exts` - 启用此插件的文件类型。默认为：[".css", ".scss", ".less", ".sass", ".styl"]。
* `firstline` - 指定激活字符串
* `reservedunit` - 是否保留px单位

#### 感谢
* rem-unit 作者  https://github.com/fisker/rem-unit
* CSSREM 作者 https://github.com/flashlizi/cssrem
