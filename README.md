# JSON语言包翻译器

这是一个用于翻译JSON格式语言包的Python脚本。它可以自动检测语言包缺失的翻译，并使用LLM模型(如DeepSeek)一键自动生成翻译。

## 功能

- 使用LLM模型(如DeepSeek)自动生成翻译
- 与英文语言包对照，自动检测非英文语言包缺失的翻译（增量翻译）
- 支持分批翻译以避免触发大模型输出上限
- 支持多种语言批量翻译（取决于LLM模型支持的语言）
- 保持JSON文件的原始结构和顺序
- 支持嵌套的JSON结构
- 支持自定义翻译要求文件（多用于指定关键词翻译）
- 支持通过命令行指定某个文案进行重新翻译

## 限制

- 语言包文件必须为JSON格式，且文件名必须为`语言代码.json`，如`zh.json`、`ja.json`等。所有语言包和翻译要求文件都必须放在同一个目录下。
- JSON语言包格式示例见`locale/en.json`，不支持包含数组结构的JSON
- 如果添加新语言文件必须创建对应的`语言代码.json`文件并且填入空JSON内容`{}`再开始翻译
- 由于LLM模型本身的能力限制，翻译结果可能存在错误，请提前做好备份以及人工校对
- LLM提示词还有很大优化的空间，欢迎贡献提示词优化建议
- 目前只走通了Deepseek官方API的流程，SiliconFlow的DeepSeek模型因为大模型输出结果不理想(输出内容被无故截断），其它模型未经过测试，使用时请注意。

## 使用方法

0. 准备DeepSeek大模型API Key，[点击注册](https://deepseek.com/)送500万tokens；如果要用SiliconFlow的模型，[点击注册](https://cloud.siliconflow.cn/i/cVmjfg55)获取2000万tokens
1. 把仓库clone到本地，安装python3环境
2. 将配置文件`config.py.example`重命名为`config.py`，并设置API Key等参数
3. 确保locale文件夹下存在`en.json`文件，并建好其它语言的`语言代码.json`文件，如`zh.json`、`ja.json`等。翻译结果会插入回locale文件夹下原有的语言包文件中，请注意版本控制或备份
4. （可选）修改翻译要求文件，添加需要特殊翻译的关键词和翻译要求
5. 执行命令，等待翻译完成

```
    python3 main.py path/to/your/locales
```

6. 确认翻译结果

## 其它功能

- 支持对已经存在翻译的某个文案进行重新翻译（改动英文文案后同步翻译到多语言文案中），通过JSON中的字段路径标识目标文案。（暂时没想到更简单的输入方式）

```
    python3 main.py path/to/your/locales --retranslate a.b.c d.e.f
```

- 支持通过命令行参数使用不同模型进行翻译

```
    python3 main.py path/to/your/locales --model siliconflow
```

- 翻译过程中可以对照打印翻译结果供人工检查。使用方法：去掉translator.py文件中下面代码的#注释

```
    # print_translations(translated_dict, missing_translations)
```

## 后续考虑的更新

- 增加OpenRouter大模型支持

## 免责声明

本项目为个人使用脚本，仅在个人场景下走通了翻译流程，未经过充分测试，请提前做好文件备份以及翻译结果校对。
项目所有代码使用Cursor的Claude 3.5 Sonnet版本生成。

## 反馈

欢迎反馈问题，欢迎贡献代码。
