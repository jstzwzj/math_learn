# AGENTS.md — 项目指南（供 AI 编码代理阅读）

## 项目概览

这不是一个软件产品，而是一个**个人学习仓库**：「高等数学自学计划（程序员版）」。目标是 6 个月学完高等数学核心内容（同济版上册为主），通过"程序员方式"学数学——用 Python 代码数值验证数学结论、用图形和动画建立直觉。

仓库同时是一个 **Obsidian 笔记库**（`.obsidian/` 已被 gitignore，不影响内容，笔记就是普通 Markdown）。

主要内容形态有四类：

1. **学习笔记**（`notes/`）：每讲一个 Markdown 文件，如 `第01讲-极限的直觉.md`
2. **做题/错题记录**（`exercises/`）：内置 `README.md` 错题模板，按周分节记录
3. **验证 / 绘图脚本**（`tools/`）：独立运行的 Python 脚本，只存代码，不混放生成物
4. **教学素材**（`assets/`）：静态图按 `images/lectureNN/` 分讲存放，GIF 统一放在 `animations/`，由笔记以相对路径引用

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
  - 四个 `tools/verify_*.py`（第 01–04 讲）：**仅用标准库**，零安装即可运行
  - 四个 `tools/visualize_*.py`（第 01–04 讲）：matplotlib + numpy
  - `tools/animate_calculus.py`：matplotlib + numpy + pillow（GIF 用 PillowWriter 写出）
- 当前环境已验证可用版本：matplotlib 3.10.9 / numpy 2.2.6 / pillow 12.1.1

## 运行与验证命令（本项目的"构建与测试"）

没有构建系统、没有测试框架。**验证 = 直接运行脚本并检查输出**。从仓库根目录执行：

```bash
python3 tools/verify_limit.py       # 文字版：数值逼近，看 stdout 趋势
python3 tools/verify_infinitesimal.py # 文字版：等价无穷小与替换陷阱
python3 tools/verify_e_limit.py     # 文字版：复利逼近 e、两侧极限、1^∞ 实战
python3 tools/verify_continuity.py  # 文字版：连续、间断、最值与二分反例
python3 tools/visualize_limit.py   # 第 01 讲：assets/images/lecture01/ 下 1 张 PNG
python3 tools/visualize_infinitesimal.py # 第 02 讲：assets/images/lecture02/ 下 1 张 PNG
python3 tools/visualize_e_limit.py # 第 03 讲：assets/images/lecture03/ 下 1 张 PNG
python3 tools/visualize_continuity.py # 第 04 讲：assets/images/lecture04/ 下 2 张 PNG
python3 tools/animate_calculus.py  # 动画版：assets/animations/ 下 3 个 GIF
```

无显示环境（CI、SSH、代理沙箱）下加 `MPLBACKEND=Agg`，脚本只保存文件不弹窗：

```bash
MPLBACKEND=Agg python3 tools/visualize_limit.py         # macOS / Linux（bash）
$env:MPLBACKEND="Agg"; python tools\visualize_limit.py  # Windows PowerShell 5.1 / 7
```

Windows 补充：CMD 中环境变量用 `set MPLBACKEND=Agg`（单独一行）；PowerShell 5.1 不支持 `&&` 串联命令，需分行执行。

验证方式是运行上述九个脚本：文字输出核对趋势，绘图用 Agg 后端生成 PNG/GIF 并检查。输出在相同依赖版本、后端和字体下可复现；跨系统字体不同可能改变图片字节，不要求跨平台逐字节一致。

## 目录结构与模块划分

```
math_learn/
├── README.md            # 学习路线图（24 周计划、资源清单、使用方法）
├── 学习方法.md           # 学习方法论（费曼学习法、做题策略等）
├── requirements.txt     # Python 依赖清单
├── .gitattributes       # 文本统一 LF、PNG/GIF 标记二进制（mac/Windows 双端协作）
├── notes/               # 学习笔记，一讲一文件
│   ├── 第01讲-极限的直觉.md
│   ├── 第02讲-极限的运算法则与无穷小的比较.md
│   ├── 第03讲-第二个重要极限与e.md
│   └── 第04讲-连续性与间断点.md
├── exercises/           # 做题记录/错题本（内置 README.md 记录模板）
├── tools/               # 代码与素材分离，保留现有脚本运行入口
│   ├── verify_*.py       # 四讲数值验证：仅标准库
│   ├── visualize_*.py    # 四讲绘图：五张 PNG
│   └── animate_calculus.py # 三个 GIF：割线→切线、黎曼和、泰勒逼近
└── assets/              # 生成物需要随代码保存进 git
    ├── images/
    │   ├── lecture01/   # limit_plots.png
    │   ├── lecture02/   # infinitesimal_plots.png
    │   ├── lecture03/   # e_limit_plots.png
    │   └── lecture04/   # continuity_types.png、continuity_theorems.png
    └── animations/     # secant_to_tangent.gif、riemann_sum.gif、taylor_sin.gif
```

脚本与讲次的对应关系写在各自模块 docstring 里（例如动画脚本注明分别预告第 05/09/14 讲），笔记末尾的「动手环节」也会引用对应脚本。**新增讲次时保持这种双向引用**。首页讲次表同步新增笔记、配图和脚本；笔记正文用 `![说明](../assets/images/lectureNN/文件名.png)` 嵌入配图，保持 Obsidian / GitHub 通用的标准 Markdown。

## 代码风格约定

- **全仓库使用简体中文**：文档、笔记、docstring、注释、图表文字、git commit message 一律中文。
- Python 脚本约定：
  - 首行 shebang `#!/usr/bin/env python3`
  - 模块 docstring 固定包含：脚本目的、对应笔记、运行命令（macOS/Linux 与 Windows 两种写法）、依赖说明、内容/输出清单；包含 Windows 路径或 LaTeX 反斜杠时使用 raw docstring，避免转义问题
  - 函数带类型标注（`-> None`、`-> FuncAnimation` 等）
  - 输出路径以 `Path(__file__).resolve().parent.parent` 定位仓库根目录；PNG 写 `assets/images/lectureNN/`，GIF 写 `assets/animations/`，使用 `mkdir(parents=True, exist_ok=True)` 自动创建目录，不依赖当前工作目录
  - `plt.show()` 前判断 `matplotlib.get_backend().lower() != "agg"`，兼容无显示环境
  - import 块后调用 `sys.stdout.reconfigure(errors="replace")`：防止 Windows 老控制台（PS5.1 / cmd 的部分代码页）打印中文直接崩溃，对 PS7 / macOS / Linux 无影响
- 各个 matplotlib 脚本各自重复定义了 `setup_chinese_font()`（按 macOS/Windows/Linux 候选字体列表选第一个可用的中文字体，找不到任何候选时打印警告，并设 `axes.unicode_minus = False`）。这是**有意为之**：每个脚本保持独立可运行，不要为了去重而抽公共模块。
- 中文与数学符号的字体分开考虑：必要时在中文字体列表后追加 `DejaVu Sans` 回退；对数刻度的负指数若仍缺字，为数字刻度单独指定 `DejaVu Sans`。不要把中文刻度标签也强制换成不支持中文的字体，不要通过屏蔽警告掩盖缺字。
- 脚本定位是"教学演示"而非工程代码：优先可读性和注释的教学价值，不追求抽象。

## 笔记内容约定

- 文件命名：`第NN讲-标题.md`（NN 两位数字，如 `第01讲-极限的直觉.md`）
- 现有讲次的结构模板（新讲次请对齐）：开头引用块注明学习时长 → 首页 / 上一讲 / 下一讲导航 → 正文分节与对应配图（直觉先行，ε-δ 等严格定义靠后且注明"见过即可"）→「课后练习」→ 分隔线后附「答案」→「动手环节」（引用数值 / 绘图脚本）→「下一讲预告」。只链接已存在的讲次，尚未生成的下一讲保留文字预告。
- 每讲至少有一张专属数学配图，内容较多时可拆图。图片放在对应知识点之后，并附读图说明；使用标准 Markdown 相对路径，避免本机绝对路径或 Obsidian 专属嵌入语法。迁移目录时同步更新首页、笔记、脚本 docstring 和本指南。
- 教学配图按数学公式用 Python 绘制，保持可复现。空心点 / 实心点、参考线 / 函数曲线、对数轴与逼近方向须明确区分；间断点两侧分段绘制，不跨间断连接。数值稳定性有风险时优先使用 `log1p`、半角恒等式等准确的等价变形。
- 图片与有限采样用于建立直觉，不代替证明；不要把残差当成根误差，也不要把有限末项或网格最大值直接当成极限或真实最值。
- 教学口吻：面向"会编程、数学忘掉大半"的读者，大量把数学概念映射到编程概念（极限≈收敛迭代、积分≈for 循环累加等）
- 数学公式用 LaTeX 写：行内 `$...$`，独立成行用 `$$...$$`（Obsidian 与 GitHub 都能渲染成真正的数学符号，见 `notes/` 现有讲次的写法）
  - 多行公式用 `\begin{aligned}` 配 `&` 对齐，**不要用** `\begin{align}`（GitHub 的 MathJax 不支持）
  - 公式内不混中文：`\text{...}` 里的中文在部分渲染器会缺字形，中文一律写在公式外面
  - 行内分数优先用 `\dfrac`（显示体，可读性好于 `\frac`）
  - 代码块、终端输出、commit message 里仍用 ASCII 写法（这些场合不渲染 LaTeX）
  - 行内 `$...$` 的**起始 `$` 前必须留一个空格**：GitHub 的解析器要求它前面是空白，紧贴中文或字母都不渲染（实测 `字$x$字` ✗ / `字 $x$字` ✓；闭合 `$` 之后无此要求）。写完新讲次请到 GitHub 页面抽查公式是否都渲染出来了
  - 公式里**不要用** `\,` `\;` `\!` 这类标点型间距命令：GitHub 的 Markdown 转义会吃掉反斜杠，`\,` 会渲染成一个多余的逗号（实测翻车）。需要间距用 `\ `（反斜杠+空格，实测安全）或 `\quad`；逗号后的间距 MathJax 会自动处理
  - `$$...$$` 块级公式无此限制，`\begin{aligned}` 多行对齐也正常
  - 标题里不写 LaTeX（会让锚点变成转义字符），用 Unicode 符号即可（如 `→`、`≤`、`α`、`ε`）

## 测试策略

没有固定的自动化测试框架。正确性与可读性通过以下检查确认：

1. **数值验证**：运行相关脚本，输出应呈现预期的逼近趋势（如 sin(x)/x 随 x 减小趋近 1）。数学定义、定理前提与练习答案需要独立核对，不能仅凭数值认定正确。
2. **重新生成对比**：改绘图脚本后用 Agg 后端重新生成素材；同一环境下可比较校验值，已有提交的素材也可查看 Git 差异。检查是否有缺字、标注遮挡或裁切；跨平台字体不同导致字节变化不一定代表数学内容变化。
3. **引用与目录**：确认笔记中嵌入的图片、首页讲次表及上下讲链接均存在；从仓库外运行绘图脚本，输出仍应位于仓库的 `assets/` 下。素材迁移后不要在 `tools/` 留下重复的 PNG/GIF。
4. **阅读体验**：在 Obsidian 阅读视图或 Markdown 预览中检查图文展示；未实际检查某个渲染环境时，不宣称已完成该环境的显示验证。

数学答案的验算约定（见 `学习方法.md`）：sympy 只用于"手算完对答案"，不让工具代替手算。

## Git 约定

- commit message 用中文，格式如 `跨平台：中文字体自动适配 macOS/Windows/Linux，README 补充 Windows 运行说明`
- `.gitignore` 已排除：`.DS_Store`、`.obsidian/`、`__pycache__/`、`*.pyc`、`.venv/`
- `.gitattributes` 强制文本文件 LF 换行、PNG/GIF 按二进制处理，避免 Windows 检出/提交时的 CRLF 转换产生假改动
- `assets/` 下的 PNG/GIF 生成物**需要提交**（让读者不跑脚本也能看到结果）

## 部署

无部署流程。这是纯本地学习仓库，唯一"分发"方式是 git 仓库本身。脚本跨平台（macOS/Windows/Linux），中文字体自动适配，无需联网。

## 安全注意事项

- 无密钥、无网络请求、无外部服务依赖；`pip install` 是唯一需要联网的环节
- 不要提交 `.obsidian/`（个人工作区状态）和任何虚拟环境目录
- 绘图脚本只创建 `assets/` 下的素材目录并写入对应 PNG/GIF，无其他副作用
