#!/usr/bin/env python3
r"""把第 04 讲的连续性、间断点、闭区间性质与二分法画出来。

配套笔记: notes/第04讲-连续性与间断点.md
运行（macOS/Linux）: python3 tools/visualize_continuity.py
运行（Windows）:     python tools\visualize_continuity.py
依赖: matplotlib + numpy 及 Python 标准库，安装方式见 requirements.txt
无显示环境: 设置 MPLBACKEND=Agg，只保存图片、不弹窗

内容与输出清单:
  1. 六面板：连续、可去、跳跃、无穷、振荡，以及振荡被无穷小压住
     -> assets/images/lecture04/continuity_types.png
  2. 四面板：闭区间最值、零点定理、二分区间、连续与跳跃的残差对照
     -> assets/images/lecture04/continuity_theorems.png

空心点表示该位置未取到，实心点表示函数值。曲线在间断处分别绘制，
不跨越间断点连接。有限采样仅用于展示，不能证明连续或极限不存在。
"""

import sys
from pathlib import Path
from typing import Callable, List, Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager, rcParams

# Windows 老控制台兜底：无法输出的字符替换显示，不让中文输出崩溃。
sys.stdout.reconfigure(errors="replace")

BLUE = "#2563eb"
GREEN = "#059669"
ORANGE = "#d97706"
PURPLE = "#7c3aed"
RED = "#dc2626"
BACKGROUND = "#f7f9fc"


def setup_chinese_font() -> None:
    """每个绘图脚本独立选择中文字体，兼容 macOS、Windows 和 Linux。"""
    candidates = [
        # macOS
        "PingFang SC", "Hiragino Sans GB", "Arial Unicode MS", "Heiti TC", "STHeiti",
        # Windows
        "Microsoft YaHei", "SimHei", "SimSun",
        # Linux
        "Noto Sans CJK SC", "WenQuanYi Micro Hei", "WenQuanYi Zen Hei",
    ]
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            rcParams["font.sans-serif"] = [name, "DejaVu Sans"]
            break
    else:
        print("警告：未找到可用中文字体，图中文字可能显示为方框；Linux 可安装 Noto Sans CJK。")
    rcParams["axes.unicode_minus"] = False


def style_panel(ax: plt.Axes) -> None:
    """统一面板风格，浅网格不抢走曲线的注意力。"""
    ax.set_facecolor("white")
    ax.set_axisbelow(True)
    ax.grid(True, color="#e2e8f0", linewidth=0.7)
    ax.tick_params(labelsize=9)
    ax.set_xlabel("x", fontsize=10)
    ax.set_ylabel("函数值", fontsize=10)
    for spine in ax.spines.values():
        spine.set_color("#cbd5e1")


def panel_continuous(ax: plt.Axes) -> None:
    """点附近与点本身一致：平方函数在一处连续。"""
    x = np.linspace(0, 2, 500)
    ax.plot(x, x**2, color=BLUE, linewidth=2, label=r"$f(x)=x^2$")
    ax.plot(1, 1, "o", color=GREEN, markersize=8)
    ax.annotate("实心点：函数值与极限都是 1", xy=(1, 1), xytext=(0.06, 0.86),
                textcoords="axes fraction", fontsize=9, color=GREEN,
                arrowprops=dict(arrowstyle="->", color=GREEN))
    ax.set_title("连续：附近的趋势与点本身接上", fontsize=12, pad=10)
    ax.set_ylim(-0.25, 4.3)
    ax.legend(loc="lower right", fontsize=9)


def panel_removable(ax: plt.Axes) -> None:
    """极限为二，特殊点却返回零；仅修改该点可以修复。"""
    for x in [np.linspace(0, 0.999, 300), np.linspace(1.001, 2, 300)]:
        ax.plot(x, x + 1, color=BLUE, linewidth=2)
    ax.plot(1, 2, "o", markersize=10, markerfacecolor="white",
            markeredgecolor=RED, markeredgewidth=2, zorder=5)
    ax.plot(1, 0, "o", color=RED, markersize=8)
    ax.annotate("空心点：极限为 2", xy=(1, 2), xytext=(0.04, 0.87),
                textcoords="axes fraction", fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.annotate("实心点：g(1)=0\n改成 2 就能修好", xy=(1, 0), xytext=(0.53, 0.27),
                textcoords="axes fraction", fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.set_title("可去：极限存在，但返回值不匹配", fontsize=12, pad=10)
    ax.set_ylim(-0.45, 3.7)


def panel_jump(ax: plt.Axes) -> None:
    """左右各画一段，不用折线把跳跃错误地接成连续。"""
    ax.plot([-1, 0], [-1, -1], color=BLUE, linewidth=2)
    ax.plot([0, 1], [1, 1], color=PURPLE, linewidth=2)
    ax.plot(0, -1, "o", markersize=10, markerfacecolor="white",
            markeredgecolor=BLUE, markeredgewidth=2, zorder=5)
    ax.plot(0, 1, "o", color=PURPLE, markersize=8, zorder=5)
    ax.text(0.06, 0.90, "左极限 -1 ≠ 右极限 1", transform=ax.transAxes, color=RED, fontsize=10)
    ax.text(0.5, 0.48, "改一个点的值，接不上左右两侧", transform=ax.transAxes,
            ha="center", fontsize=9, color=RED)
    ax.set_title("跳跃：左右极限有限但不同", fontsize=12, pad=10)
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.7, 1.8)


def panel_infinite(ax: plt.Axes) -> None:
    """双曲线两支分开绘制，虚线仅表示垂直渐近线。"""
    for x in [-np.geomspace(0.01, 1, 800)[::-1], np.geomspace(0.01, 1, 800)]:
        ax.plot(x, 1 / x, color=ORANGE, linewidth=2)
    ax.axvline(0, color=RED, linestyle="--", linewidth=1)
    ax.text(0.05, 0.88, r"$x\to 0^+:\, +\infty$", transform=ax.transAxes,
            fontsize=11, color=ORANGE)
    ax.text(0.59, 0.08, r"$x\to 0^-:\, -\infty$", transform=ax.transAxes,
            fontsize=11, color=ORANGE)
    ax.set_title(r"无穷：$1/x$ 的输出没有有限极限", fontsize=12, pad=10)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-12, 12)


def panel_oscillation(ax: plt.Axes) -> None:
    """振荡函数的局部图，缺口不是停止振荡，而是未绘制更细的输入。"""
    positive = np.linspace(0.002, 0.35, 20000)
    for x in [-positive[::-1], positive]:
        ax.plot(x, np.sin(1 / x), color=PURPLE, linewidth=0.6)
    ax.axvline(0, color="#94a3b8", linestyle="--", linewidth=1)
    ax.set_title(r"振荡：$\sin(1/x)$ 始终定不下来", fontsize=12, pad=10)
    ax.set_xlim(-0.35, 0.35)
    ax.set_ylim(-1.4, 1.7)
    ax.text(0.5, 0.9, "振幅不缩小；越靠近 0 越密", transform=ax.transAxes,
            ha="center", fontsize=9, color=PURPLE)


def panel_damped(ax: plt.Axes) -> None:
    """有界振荡乘以无穷小，补上零点后整个函数连续。"""
    positive = np.linspace(0.002, 0.35, 20000)
    for x in [-positive[::-1], positive]:
        ax.plot(x, x * np.sin(1 / x), color=BLUE, linewidth=0.8)
    x = np.linspace(-0.35, 0.35, 500)
    ax.plot(x, np.abs(x), "--", color=GREEN, linewidth=1.1)
    ax.plot(x, -np.abs(x), "--", color=GREEN, linewidth=1.1)
    ax.plot(0, 0, "o", color=GREEN, markersize=7, zorder=5)
    ax.text(0.5, 0.90, r"$|x\sin(1/x)|\leq |x|\to 0$", transform=ax.transAxes,
            ha="center", color=GREEN, fontsize=11)
    ax.set_title("振荡也能连续：包络把它压到 0", fontsize=12, pad=10)
    ax.set_xlim(-0.35, 0.35)
    ax.set_ylim(-0.42, 0.55)
    ax.text(0.5, 0.06, "定义 f(0)=0；绿虚线是 ±|x|，不是函数本身",
            transform=ax.transAxes, ha="center", fontsize=8, color=GREEN)


def make_types_figure() -> plt.Figure:
    """六面板对应笔记的定义、间断分类和夹逼例子。"""
    fig, axes = plt.subplots(3, 2, figsize=(12, 11), facecolor=BACKGROUND)
    panels = [panel_continuous, panel_removable, panel_jump,
              panel_infinite, panel_oscillation, panel_damped]
    for ax, panel in zip(axes.flat, panels):
        style_panel(ax)
        panel(ax)
    fig.suptitle("第 04 讲 · 连续与间断，差别在哪里？", fontsize=16, fontweight="bold")
    fig.text(0.5, 0.015, "空心点表示该值未取到，实心点表示函数值；有限绘图不代替极限证明。",
             ha="center", fontsize=10, color="#475569")
    fig.tight_layout(rect=(0, 0.045, 1, 0.96), h_pad=2, w_pad=2)
    return fig


def polynomial(x: float) -> float:
    """笔记中的连续多项式。"""
    return x**3 - x - 2


def jump(x: float) -> float:
    """反例：没有零点的跳跃函数。"""
    return -1.0 if x < 0 else 1.0


def bisection_trace(
    function: Callable[[float], float], left: float, right: float, steps: int,
) -> List[Tuple[float, float]]:
    """记录初始区间与每次二分后的区间；连续性需另行检查。

    跳跃函数也能通过端点符号检查；本脚本故意记录这个反例。
    """
    if left >= right or steps < 0:
        raise ValueError("需要左端点小于右端点，且二分次数非负")
    f_left, f_right = function(left), function(right)
    if not (np.isfinite(f_left) and np.isfinite(f_right)):
        raise ValueError("端点函数值必须有限")
    if f_left == 0:
        return [(left, left)]
    if f_right == 0:
        return [(right, right)]
    if (f_left < 0) == (f_right < 0):
        raise ValueError("两个端点需要异号")
    intervals = [(left, right)]
    for _ in range(steps):
        middle = (left + right) / 2
        if middle == left or middle == right:
            break
        f_middle = function(middle)
        if not np.isfinite(f_middle):
            raise ValueError("中点函数值必须有限")
        if f_middle == 0:
            intervals.append((middle, middle))
            break
        if (f_left < 0) == (f_middle < 0):
            left, f_left = middle, f_middle
        else:
            right = middle
        intervals.append((left, right))
    return intervals


def panel_extrema(ax: plt.Axes) -> None:
    """用实心端点与中点，展示真正取得的最小值和最大值。"""
    x = np.linspace(0, 1, 500)
    ax.plot(x, x * (1 - x), color=BLUE, linewidth=2, label=r"$x(1-x)$")
    ax.fill_between(x, x * (1 - x), alpha=0.07, color=BLUE)
    ax.plot([0, 1], [0, 0], "o", color=GREEN, markersize=7)
    ax.plot(0.5, 0.25, "o", color=ORANGE, markersize=7)
    ax.text(0.5, 0.9, "最大值 1/4，在 x=1/2 取得", transform=ax.transAxes,
            ha="center", color=ORANGE, fontsize=10)
    ax.text(0.5, 0.06, "最小值 0，在两个端点取得", transform=ax.transAxes,
            ha="center", color=GREEN, fontsize=9)
    ax.set_title("闭区间最值：不只是逼近，还取得到", fontsize=12, pad=10)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.06, 0.34)


def panel_zero(ax: plt.Axes) -> None:
    """端点异号，连续曲线必须经过零。"""
    x = np.linspace(1, 2, 500)
    ax.plot(x, x**3 - x - 2, color=BLUE, linewidth=2)
    ax.axhline(0, color="#64748b", linewidth=1)
    ax.plot([1, 2], [-2, 4], "o", color=ORANGE, markersize=7)
    left, right = bisection_trace(polynomial, 1, 2, 40)[-1]
    root = (left + right) / 2
    ax.plot(root, 0, "o", color=GREEN, markersize=7)
    ax.annotate("至少一个零点\nx 约为 1.52138", xy=(root, 0), xytext=(1.06, 1.5),
                fontsize=9, color=GREEN, arrowprops=dict(arrowstyle="->", color=GREEN))
    ax.text(0.04, 0.06, "左端 -2 < 0", transform=ax.transAxes, fontsize=9, color=ORANGE)
    ax.text(0.97, 0.93, "右端 4 > 0", transform=ax.transAxes, fontsize=9,
            color=ORANGE, ha="right")
    ax.set_title(r"零点定理：连续的 $x^3-x-2$", fontsize=12, pad=10)
    ax.set_xlim(0.98, 2.02)
    ax.set_ylim(-2.7, 4.8)


def panel_intervals(ax: plt.Axes) -> None:
    """将前六个保留区间排成行，直观看每次宽度减半。"""
    intervals = bisection_trace(polynomial, 1, 2, 5)
    for step, (left, right) in enumerate(intervals):
        ax.plot([left, right], [step, step], "o-", linewidth=4, markersize=5, color=BLUE)
    ax.set_yticks(range(len(intervals)))
    ax.set_yticklabels([f"第 {step} 次" for step in range(len(intervals))])
    ax.set_xlim(0.95, 2.3)
    ax.set_ylim(5.6, -1)
    ax.set_xlabel("仍夹着根的区间", fontsize=10)
    ax.set_ylabel("完成的二分次数", fontsize=10)
    ax.text(0.98, 0.80, "每次宽度减半\n中点误差 ≤ 半宽", transform=ax.transAxes,
            ha="right", color=GREEN, fontsize=9)
    ax.set_title("二分循环：一直保留端点异号的一半", fontsize=12, pad=10)


def panel_residuals(ax: plt.Axes) -> None:
    """区间都在缩小，只有连续例子的残差走向零；残差不必单调。"""
    for function, left, right, color, label in [
        (polynomial, 1, 2, BLUE, "连续多项式：趋近零点"),
        (jump, -1, 1, RED, "跳跃函数：残差始终为 1"),
    ]:
        intervals = bisection_trace(function, left, right, 16)
        residuals = [abs(function((a + b) / 2)) for a, b in intervals]
        ax.semilogy(range(len(intervals)), residuals, "o-", color=color,
                    markersize=3, linewidth=1.6, label=label)
    ax.set_title("收敛反例：区间变窄，不代表有根", fontsize=12, pad=10)
    ax.set_xlabel("完成的二分次数", fontsize=10)
    ax.set_ylabel("中点残差的绝对值（对数轴）", fontsize=10)
    ax.set_ylim(1e-6, 10)
    ax.set_xticks([0, 4, 8, 12, 16])
    # 残差对数轴含负指数，数字刻度单独使用能显示数学负号的字体。
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontfamily("DejaVu Sans")
    ax.legend(loc="lower left", fontsize=8)
    ax.text(0.5, 0.92, "残差不是根误差；也不保证每次都变小", transform=ax.transAxes,
            ha="center", fontsize=8, color=PURPLE)


def make_theorems_figure() -> plt.Figure:
    """四面板对应闭区间连续函数的性质与二分法。"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 8.5), facecolor=BACKGROUND)
    panels = [panel_extrema, panel_zero, panel_intervals, panel_residuals]
    for ax, panel in zip(axes.flat, panels):
        style_panel(ax)
        panel(ax)
    fig.suptitle("第 04 讲 · 连续性给算法的保证", fontsize=16, fontweight="bold")
    fig.text(0.5, 0.015, "最值与零点定理要求整个闭区间上连续；反例故意违反连续性前提。",
             ha="center", fontsize=10, color=RED)
    fig.tight_layout(rect=(0, 0.045, 1, 0.95), h_pad=2, w_pad=2)
    return fig


def main() -> None:
    """生成两张教学图，目录自动创建，Agg 后端不弹窗。"""
    setup_chinese_font()
    output_dir = Path(__file__).resolve().parent.parent / "assets" / "images" / "lecture04"
    output_dir.mkdir(parents=True, exist_ok=True)
    figures = [
        (make_types_figure(), "continuity_types.png"),
        (make_theorems_figure(), "continuity_theorems.png"),
    ]
    for fig, filename in figures:
        output_path = output_dir / filename
        fig.savefig(output_path, dpi=160, facecolor=BACKGROUND)
        print(f"已保存图片: {output_path}")
    if matplotlib.get_backend().lower() != "agg":
        plt.show()
    else:
        print("当前为无显示环境（Agg），跳过弹窗。")
    for fig, _ in figures:
        plt.close(fig)


if __name__ == "__main__":
    main()
