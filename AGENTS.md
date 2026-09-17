# AGENTS.md — 项目指南（供 AI 编码代理阅读）

## 项目概览

这不是一个软件产品，而是一个**个人学习仓库**：「高等数学自学计划（程序员版）」。目标是 6 个月学完高等数学核心内容（同济版上册为主），通过"程序员方式"学数学——用 Python 代码数值验证数学结论、用图形和动画建立直觉。

仓库同时是一个 **Obsidian 笔记库**（`.obsidian/` 已被 gitignore，不影响内容，笔记就是普通 Markdown）。

主要内容形态有三类：

1. **学习笔记**（`notes/`）：每讲一个 Markdown 文件，如 `第01讲-极限的直觉.md`
2. **做题/错题记录**（`exercises/`）：内置 `README.md` 错题模板，按周分节记录
3. **验证脚本**（`tools/`）：用代码验证当讲数学结论的 Python 脚本，及其生成的图片/GIF

`README.md` 是 24 周学习路线图（四个阶段：极限 → 微分 → 积分 → 进阶选学），`学习方法.md` 是学习方法论。修改路线或方法时请同步这两个文件。

## 技术栈与依赖

- **语言**：Python 3（README 要求 3.8+；当前环境实测 3.10.11）
- 依赖清单在根目录 `requirements.txt`（matplotlib + pillow + sympy；numpy 随 matplotlib 装好）：
  ```bash
  pip3 install -r requirements.txt   # macOS / Linux
  pip install -r requirements.txt    # Windows
  ```
- sympy 仅供学习者手算后对照答案（见 `学习方法.md`「符号计算」一节），`tools/` 脚本不 import 它。
- 各脚本依赖不同，注意区分：
  - `tools/verify_limit.py`、`tools/verify_infinitesimal.py`：**仅用标准库** `math`，零安装即可运行
  - `tools/visualize_limit.py`：matplotlib + numpy
  - `tools/animate_calculus.py`：matplotlib + numpy + pillow（GIF 用 PillowWriter 写出）
- 当前环境已验证可用版本：matplotlib 3.10.9 / numpy 2.2.6 / pillow 12.1.1

## 运行与验证命令（本项目的"构建与测试"）

没有构建系统、没有测试框架。**验证 = 直接运行脚本并检查输出**。从仓库根目录执行：

```bash
python3 tools/verify_limit.py       # 文字版：数值逼近，看 stdout 趋势
python3 tools/visualize_limit.py    # 图形版：生成 tools/limit_plots.png 并弹窗
python3 tools/animate_calculus.py   # 动画版：生成 tools/ 下 3 个 GIF 并弹窗
```

无显示环境（CI、SSH、代理沙箱）下加 `MPLBACKEND=Agg`，脚本只保存文件不弹窗：

```bash
MPLBACKEND=Agg python3 tools/visualize_limit.py         # macOS / Linux（bash）
$env:MPLBACKEND="Agg"; python tools\visualize_limit.py  # Windows PowerShell 5.1 / 7
```

Windows 补充：CMD 中环境变量用 `set MPLBACKEND=Agg`（单独一行）；PowerShell 5.1 不支持 `&&` 串联命令，需分行执行。

三个脚本均已实测通过（Python 3.10.11，Agg 后端）：数值输出趋势正确，PNG/GIF 重新生成后与仓库中已提交版本一致（输出是确定性的）。

## 目录结构与模块划分

```
math_learn/
├── README.md            # 学习路线图（24 周计划、资源清单、使用方法）
├── 学习方法.md           # 学习方法论（费曼学习法、做题策略等）
├── requirements.txt     # Python 依赖清单
├── .gitattributes       # 文本统一 LF、PNG/GIF 标记二进制（mac/Windows 双端协作）
├── notes/               # 学习笔记，一讲一文件
│   ├── 第01讲-极限的直觉.md
│   └── 第02讲-极限的运算法则与无穷小的比较.md
├── exercises/           # 做题记录/错题本（内置 README.md 记录模板）
└── tools/               # 验证脚本及其生成物（生成物已提交进 git）
    ├── verify_limit.py       # 数值验证：数列极限、sin(x)/x、差商、震荡反例（第 01 讲）
    ├── verify_infinitesimal.py # 数值验证：等价无穷小、高阶比较、替换陷阱（第 02 讲）
    ├── visualize_limit.py    # 四面板可视化 → limit_plots.png
    ├── animate_calculus.py   # 三个 GIF：割线→切线、黎曼和、泰勒逼近
    └── *.png / *.gif         # 脚本输出，确定性与脚本同步提交
```

脚本与讲次的对应关系写在各自模块 docstring 里（例如动画脚本注明分别预告第 05/09/14 讲），笔记末尾的「动手环节」也会引用对应脚本。**新增讲次时保持这种双向引用**。

## 代码风格约定

- **全仓库使用简体中文**：文档、笔记、docstring、注释、图表文字、git commit message 一律中文。
- Python 脚本模板（三个脚本均遵循）：
  - 首行 shebang `#!/usr/bin/env python3`
  - 模块 docstring 固定包含：脚本目的、运行命令（macOS/Linux 与 Windows 两种写法）、依赖说明、内容/输出清单
  - 函数带类型标注（`-> None`、`-> FuncAnimation` 等）
  - 输出路径用 `Path(__file__).resolve().parent / "文件名"`，保证从任何目录运行都写到 `tools/` 下
  - `plt.show()` 前判断 `matplotlib.get_backend().lower() != "agg"`，兼容无显示环境
  - import 块后调用 `sys.stdout.reconfigure(errors="replace")`：防止 Windows 老控制台（PS5.1 / cmd 的部分代码页）打印中文直接崩溃，对 PS7 / macOS / Linux 无影响
- 两个 matplotlib 脚本各自重复定义了 `setup_chinese_font()`（按 macOS/Windows/Linux 候选字体列表选第一个可用的中文字体，找不到任何候选时打印警告，并设 `axes.unicode_minus = False`）。这是**有意为之**：每个脚本保持独立可运行，不要为了去重而抽公共模块。
- 脚本定位是"教学演示"而非工程代码：优先可读性和注释的教学价值，不追求抽象。

## 笔记内容约定

- 文件命名：`第NN讲-标题.md`（NN 两位数字，如 `第01讲-极限的直觉.md`）
- 现有讲次的结构模板（新讲次请对齐）：开头引用块注明学习时长 → 正文分节（直觉先行，ε-δ 等严格定义靠后且注明"见过即可"）→「课后练习」→ 折叠线后附「答案」→「动手环节」（引用 `tools/` 脚本）→「下一讲预告」
- 教学口吻：面向"会编程、数学忘掉大半"的读者，大量把数学概念映射到编程概念（极限≈收敛迭代、积分≈for 循环累加等）
- 数学公式用 LaTeX 写：行内 `$...$`，独立成行用 `$$...$$`（Obsidian 与 GitHub 都能渲染成真正的数学符号，见 `notes/` 现有讲次的写法）
  - 多行公式用 `\begin{aligned}` 配 `&` 对齐，**不要用** `\begin{align}`（GitHub 的 MathJax 不支持）
  - 公式内不混中文：`\text{...}` 里的中文在部分渲染器会缺字形，中文一律写在公式外面
  - 行内分数优先用 `\dfrac`（显示体，可读性好于 `\frac`）
  - 代码块、终端输出、commit message 里仍用 ASCII 写法（这些场合不渲染 LaTeX）
  - 行内 `$...$` 的**起始 `$` 前必须留一个空格**：GitHub 的解析器要求它前面是空白，紧贴中文或字母都不渲染（实测 `字$x$字` ✗ / `字 $x$字` ✓；闭合 `$` 之后无此要求）。写完新讲次请到 GitHub 页面抽查公式是否都渲染出来了
  - `$$...$$` 块级公式无此限制，`\begin{aligned}` 多行对齐也正常
  - 标题里不写 LaTeX（会让锚点变成转义字符），用 Unicode 符号即可（如 `→`、`≤`、`α`、`ε`）

## 测试策略

无自动化测试。正确性靠两层人工验证：

1. **数值验证**：脚本输出应呈现预期的逼近趋势（如 sin(x)/x 随 x 减小趋近 1）
2. **重新生成对比**：PNG/GIF 是确定性输出且已提交，改脚本后重新运行，`git status` 若无变化说明行为未变；有变化则肉眼检查新图是否符合教学意图

数学答案的验算约定（见 `学习方法.md`）：sympy 只用于"手算完对答案"，不让工具代替手算。

## Git 约定

- commit message 用中文，格式如 `跨平台：中文字体自动适配 macOS/Windows/Linux，README 补充 Windows 运行说明`
- `.gitignore` 已排除：`.DS_Store`、`.obsidian/`、`__pycache__/`、`*.pyc`、`.venv/`
- `.gitattributes` 强制文本文件 LF 换行、PNG/GIF 按二进制处理，避免 Windows 检出/提交时的 CRLF 转换产生假改动
- `tools/` 下的 PNG/GIF 生成物**需要提交**（让读者不跑脚本也能看到结果）

## 部署

无部署流程。这是纯本地学习仓库，唯一"分发"方式是 git 仓库本身。脚本跨平台（macOS/Windows/Linux），中文字体自动适配，无需联网。

## 安全注意事项

- 无密钥、无网络请求、无外部服务依赖；`pip install` 是唯一需要联网的环节
- 不要提交 `.obsidian/`（个人工作区状态）和任何虚拟环境目录
- 脚本只写 `tools/` 目录下的图片文件，无其他副作用
