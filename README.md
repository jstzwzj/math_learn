# 高等数学自学计划（程序员版）

> 目标：用 6 个月左右学完高等数学核心内容（同济版上册为主，下册选学），建立扎实的微积分直觉和计算能力。

## 从这里开始

- **读笔记**：点击下面的讲次链接，在 Obsidian 阅读视图、GitHub 或 IDE Markdown 预览中看正文和配图。
- **做练习**：每讲末尾都有题目与答案；做完再对照，用 [错题模板](exercises/README.md) 记录。
- **跑代码**：数值验证不需要安装依赖；重新生成配图才需要安装 `requirements.txt`。
- **找素材**：静态图在 `assets/images/lectureNN/`，动画在 `assets/animations/`；图片已随仓库保存，不运行脚本也能看。

| 讲次 | 学习笔记 | 配图 | 数值验证 / 绘图脚本（位于 tools/） |
|---|---|---|---|
| 01 | [极限的直觉](notes/第01讲-极限的直觉.md) | [极限四面板](assets/images/lecture01/limit_plots.png) | `verify_limit.py` / `visualize_limit.py` |
| 02 | [极限的运算法则与无穷小的比较](notes/第02讲-极限的运算法则与无穷小的比较.md) | [无穷小四面板](assets/images/lecture02/infinitesimal_plots.png) | `verify_infinitesimal.py` / `visualize_infinitesimal.py` |
| 03 | [第二个重要极限与 e](notes/第03讲-第二个重要极限与e.md) | [复利与极限四面板](assets/images/lecture03/e_limit_plots.png) | `verify_e_limit.py` / `visualize_e_limit.py` |
| 04 | [连续性与间断点](notes/第04讲-连续性与间断点.md) | [连续与间断](assets/images/lecture04/continuity_types.png) · [定理与二分法](assets/images/lecture04/continuity_theorems.png) | `verify_continuity.py` / `visualize_continuity.py` |

> **只阅读，无需配置 Python。** 建议按“直觉 → 看图 → 手算 → 数值核对”的顺序学习；完整节奏见 [学习方法](学习方法.md)。讲次是知识单元，不必机械地与下方周计划一一对应。

## 为什么程序员学高数不吃亏

- **机器学习 / AI**：梯度下降、反向传播、损失函数，全是导数和偏导数
- **性能优化**：复杂度分析的本质是函数增长率比较（极限思想）
- **图形 / 游戏**：渲染、物理引擎靠向量和微积分
- **日常底气**：看论文不再卡在公式那一行

程序员的最大优势：**可以用代码数值验证数学结论**，这在传统课堂里是做不到的。

---

## 学习路线（四个阶段）

### 阶段一：函数与极限（第 1–4 周）

| 周 | 内容 |
|---|---|
| 1 | 函数复习（定义域、复合、反函数）、初等函数 |
| 2 | 数列极限、函数极限的直觉与定义 |
| 3 | 无穷小/无穷大、极限运算法则、两个重要极限 |
| 4 | 连续性与间断点、闭区间上连续函数的性质 |

**本阶段目标**：看到 $\lim\limits_{x \to 0} \dfrac{\sin x}{x} = 1$ 不再害怕，能解释"极限"到底在说什么。

### 阶段二：一元微分学（第 5–10 周）

| 周 | 内容 |
|---|---|
| 5 | 导数定义、几何意义、基本求导公式 |
| 6 | 求导法则（四则、复合链式法则、反函数） |
| 7 | 高阶导数、隐函数求导、参数方程求导、微分 |
| 8 | 中值定理（罗尔、拉格朗日）、洛必达法则 |
| 9 | 泰勒公式（重点！理解"用多项式逼近函数"） |
| 10 | 单调性、极值、凹凸性、最优化应用 |

**本阶段目标**：熟练求任何初等函数的导数；理解泰勒展开（这是后续理解很多近似算法的钥匙）。

### 阶段三：一元积分学（第 11–16 周）

| 周 | 内容 |
|---|---|
| 11 | 不定积分概念、基本积分表 |
| 12 | 第一类换元法（凑微分） |
| 13 | 第二类换元法、分部积分法 |
| 14 | 定积分定义（黎曼和）、性质 |
| 15 | 微积分基本定理（牛顿–莱布尼茨公式） |
| 16 | 定积分应用（面积、体积、弧长）、反常积分 |

**本阶段目标**：理解"积分是累加"，能算常见积分，明白微积分基本定理为什么是"整个微积分的核心"。

### 阶段四：进阶主题（第 17–24 周，选学，按需深入）

- 微分方程入门（一阶线性、可分离变量）
- 无穷级数（收敛判别、幂级数展开）
- 多元函数微分（偏导数、梯度——机器学习刚需）
- 重积分（二重积分为主）

---

## 资源清单（按用途搭配）

| 用途 | 资源 | 说明 |
|---|---|---|
| 建立直觉 | 3Blue1Brown《微积分的本质》 | B站有官方中字，共 12 集，先看一遍，每集 15 分钟 |
| 系统学习 | 宋浩老师《高等数学》 | B站免费，讲得细、适合自学，配合同济教材 |
| 教材 | 同济《高等数学》第七版（上册） | 权威教材，课后题必做 |
| 课外读物 | 《普林斯顿微积分读本》 | 最白话的微积分书，卡壳时的救命稻草 |
| 代码验证 | Python + sympy / numpy | 见 `tools/` 目录示例 |

> 不建议入门就用《吉米多维奇》，题量太大容易劝退。

---

## 每周节奏建议（工作日每天 1 小时 + 周末 2 小时）

- **周一~周五**：看视频或读书 40 分钟 + 动手做题 20 分钟
- **每个知识点**：至少做 5–10 道课后题（数学是练出来的，不是看出来的）
- **周日**：整理本周笔记，用自己的话写一篇周总结（费曼学习法）

## 目录结构

```
math_learn/
├── README.md               # 学习入口：讲次导航 + 24 周路线图
├── 学习方法.md              # 怎么学、怎么做题和复习
├── requirements.txt        # 绘图 / 符号验算依赖
├── AGENTS.md               # AI 协作指南，学习时可忽略
├── notes/                  # 读：按讲次排列，正文中直接显示配图
│   ├── 第01讲-极限的直觉.md
│   ├── 第02讲-极限的运算法则与无穷小的比较.md
│   ├── 第03讲-第二个重要极限与e.md
│   └── 第04讲-连续性与间断点.md
├── exercises/              # 练：做题记录 / 错题本
│   └── README.md           # 记录模板
├── tools/                  # 跑：独立 Python 脚本，不存图片
│   ├── verify_*.py         # 数值核对（仅标准库）
│   ├── visualize_*.py      # 数学配图（matplotlib + numpy）
│   └── animate_calculus.py # 后续微积分概念动画
└── assets/                 # 看：配图 / 动画，随仓库保存
    ├── images/
    │   ├── lecture01/      # 极限的直觉
    │   ├── lecture02/      # 无穷小与替换陷阱
    │   ├── lecture03/      # 第二个重要极限与 e
    │   └── lecture04/      # 连续、间断、定理与二分法
    └── animations/         # 割线变切线 / 黎曼和 / 泰勒逼近
```

## 使用方法

1. 先读 [学习方法](学习方法.md)（5 分钟）。
2. 从首页讲次表打开笔记；切换到 Markdown 预览 / 阅读视图，就能看到公式和配图。纯文本编辑视图中显示的是图片引用语法。
3. 先完成课后练习，再运行该讲的 `verify_*.py` 核对数值。想探索图形时，运行对应的 `visualize_*.py`，可修改参数后重新生成图片。
4. 在 `exercises/` 里记录错题，按周回顾；新讲次沿用 `第NN讲-标题.md` 命名。

笔记使用标准 Markdown 相对图片路径，Obsidian 与 GitHub 均可显示。移动笔记或素材时需同步更新引用；分享时应保留仓库目录结构，不要只发送一个 `.md` 文件。

## 在 Windows / Linux 上运行

工程本身跨平台，脚本会自动选择当前系统的中文字体。需已安装 Python 3.8+（Windows 安装时记得勾选 "Add to PATH"）。先安装依赖（一次即可）：

```bash
# Windows（PowerShell 或 CMD）
pip install -r requirements.txt

# macOS / Linux
pip3 install -r requirements.txt
```

然后运行脚本（Windows 推荐 PowerShell 7；macOS / Linux 用 `python3`）：

```powershell
# Windows（PowerShell 7）
python tools\verify_limit.py
python tools\visualize_limit.py
python tools\visualize_infinitesimal.py
python tools\visualize_e_limit.py
python tools\visualize_continuity.py
python tools\animate_calculus.py

# 无显示环境（远程 / CI）：只生成图片，不弹窗
$env:MPLBACKEND="Agg"
python tools\visualize_limit.py
```

```bash
# macOS / Linux
python3 tools/verify_limit.py
python3 tools/visualize_limit.py
python3 tools/visualize_infinitesimal.py
python3 tools/visualize_e_limit.py
python3 tools/visualize_continuity.py
python3 tools/animate_calculus.py

# 无显示环境（SSH / CI）：只生成图片，不弹窗
MPLBACKEND=Agg python3 tools/visualize_limit.py
```

> **还在用 Windows 自带的 PowerShell 5.1 或 CMD？**
> - PowerShell 5.1 不支持 `&&` 串联命令，请分行执行；环境变量写法 `$env:MPLBACKEND="Agg"` 与 PS7 相同。
> - CMD 设置环境变量用 `set MPLBACKEND=Agg`（单独一行，再执行脚本）。
> - 个别老控制台打印中文可能显示为 `?`，不影响图片 / GIF 生成；换用 PS7 或 Windows Terminal 即正常。

Windows 下首次运行若弹出"防火墙允许"提示，允许即可（本地绘图不需要联网）。PNG 输出到 `assets/images/lectureNN/`，GIF 输出到 `assets/animations/`。输出路径以脚本位置为基准，从其他工作目录运行也不会把图片写到错误的位置；目录不存在时脚本会自动创建。
