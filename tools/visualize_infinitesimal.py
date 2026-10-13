#!/usr/bin/env python3
r"""把第 02 讲的等价无穷小、高阶比较与替换陷阱画成四面板数学图。

对应笔记：notes/第02讲-极限的运算法则与无穷小的比较.md
运行（macOS/Linux）：python3 tools/visualize_infinitesimal.py
运行（Windows）：python tools\visualize_infinitesimal.py
无显示环境（macOS/Linux）：MPLBACKEND=Agg python3 tools/visualize_infinitesimal.py
无显示环境（Windows PowerShell）：
    $env:MPLBACKEND="Agg"; python tools\visualize_infinitesimal.py
依赖：matplotlib、numpy 和标准库，兼容 Python 3.8+，不依赖仓库其他脚本。
安装依赖：pip3 install -r requirements.txt（Windows 使用 pip）。

内容清单：
  1. 三个等价无穷小比值在零点右侧趋于 1。
  2. 双对数坐标比较一次、二次、三次无穷小的消失速度。
  3. 乘除因子等价替换：正弦与正切的比值从两侧趋于 1.5。
  4. 加减替换陷阱：真实极限为 0.5，错误替换推断为 0。
输出列表：assets/images/lecture02/infinitesimal_plots.png。
运行时自动创建输出目录；非 Agg 后端保存并弹窗，Agg 后端只保存并关闭图形。
"""

import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager, rcParams

# 老版 Windows 控制台无法输出的字符用替代字符显示，避免中文输出崩溃。
sys.stdout.reconfigure(errors='replace')

BLUE = "#2563eb"
GREEN = "#059669"
ORANGE = "#d97706"
PURPLE = "#7c3aed"
RED = "#dc2626"
BACKGROUND = "#f7f9fc"


def setup_chinese_font() -> None:
    """按平台挑一个可用的中文字体，避免图里中文变方框。"""
    candidates = [
        # 苹果系统候选字体。
        "PingFang SC", "Hiragino Sans GB", "Arial Unicode MS", "Heiti TC", "STHeiti",
        # 微软系统候选字体。
        "Microsoft YaHei", "SimHei", "SimSun",
        # 开源系统候选字体。
        "Noto Sans CJK SC", "WenQuanYi Micro Hei", "WenQuanYi Zen Hei",
    ]
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            rcParams["font.sans-serif"] = [name, "DejaVu Sans"]
            break
    else:
        print("警告：未找到可用中文字体，图中文字可能显示为方框"
              "（macOS/Windows 一般自带中文字体，Linux 可安装 Noto Sans CJK）。")
    rcParams["axes.unicode_minus"] = False


def style_panel(ax: plt.Axes) -> None:
    """统一白色面板、网格与坐标轴样式。"""
    ax.set_facecolor("white")
    ax.set_axisbelow(True)
    ax.grid(True, which="major", color="#e2e8f0", linewidth=0.7)
    ax.tick_params(labelsize=9)
    for spine in ax.spines.values():
        spine.set_color("#cbd5e1")


def legend_below(ax: plt.Axes) -> None:
    """把图例放在坐标轴下方，避免遮挡曲线及图注。"""
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.24),
              ncol=2, fontsize=8, frameon=False, borderaxespad=0,
              columnspacing=1.2, handlelength=2.4)


def panel_equivalent(ax: plt.Axes) -> None:
    """三个等价无穷小的比值在零点右侧趋于一。"""
    x = np.logspace(-4, np.log10(0.3), 600)
    ax.plot(x, np.sin(x) / x, color=BLUE, linewidth=2,
            label=r"$\sin x/x$")
    ax.plot(x, np.tan(x) / x, color=GREEN, linewidth=2,
            label=r"$\tan x/x$")
    # 半角恒等式避免直接计算一减余弦时的灾难性抵消。
    cosine_ratio = 4 * np.sin(x / 2)**2 / x**2
    ax.plot(x, cosine_ratio, color=ORANGE, linewidth=2,
            label=r"$2(1-\cos x)/x^2$")
    ax.axhline(1, color=PURPLE, linestyle="--", linewidth=1.3,
               label="共同极限：1")
    ax.set_xscale("log")
    ax.set_xlim(1e-4, 0.3)
    ax.set_ylim(0.978, 1.052)
    ax.set_title("等价无穷小：比值趋于 1", fontsize=12, pad=10)
    ax.set_xlabel(r"$x$（弧度，对数坐标；趋于 0 向左）", fontsize=9)
    ax.set_ylabel("无穷小的比值", fontsize=10)
    ax.text(0.04, 0.90, r"$\sin x\sim x,\quad \tan x\sim x$" + "\n"
            + r"$1-\cos x\sim x^2/2$", transform=ax.transAxes,
            fontsize=10, va="top", color=PURPLE)
    legend_below(ax)


def panel_orders(ax: plt.Axes) -> None:
    """沿横轴向左观察：高阶无穷小消失得更快，而非增长得更快。"""
    x = np.logspace(-4, np.log10(0.95), 600)
    for power, color in [(1, BLUE), (2, GREEN), (3, ORANGE)]:
        label = r"$x$" if power == 1 else rf"$x^{power}$"
        ax.loglog(x, x**power, color=color, linewidth=2, label=label)
    ax.set_xlim(1e-4, 1)
    ax.set_ylim(1e-13, 10)
    ax.set_title("高阶无穷小：消失得更快", fontsize=12, pad=10)
    ax.set_xlabel(r"$x$（对数坐标；趋于 0 向左）", fontsize=9)
    ax.set_ylabel("无穷小的大小（对数坐标）", fontsize=10)
    ax.text(0.96, 0.08, r"$x^2/x=x\to 0$" + "\n"
            + "向左看：三次比二次、一次消失更快",
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=9, color=PURPLE)
    legend_below(ax)


def panel_product_quotient(ax: plt.Axes) -> None:
    """乘除替换的例子：零点两侧分别逼近一点五，不连接零点。"""
    positive = np.logspace(-4, np.log10(0.2), 600)
    for x, label in [(-positive[::-1], r"$\sin(3x)/\tan(2x)$"),
                     (positive, "_nolegend_")]:
        ax.plot(x, np.sin(3 * x) / np.tan(2 * x), color=BLUE,
                linewidth=2, label=label)
    # 极限参考线不是函数曲线；空心点明确原式在零点无定义。
    ax.axhline(1.5, color=PURPLE, linestyle="--", linewidth=1.3,
               label="极限：1.5")
    ax.plot(0, 1.5, marker="o", markersize=9, markerfacecolor="white",
            markeredgecolor=RED, markeredgewidth=1.8, linestyle="none",
            zorder=5, label="空心点：原式在零点无定义")
    for start in [-0.13, 0.13]:
        ax.annotate("", xy=(0, 1.565), xytext=(start, 1.565),
                    arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))
    ax.text(0, 1.60, "左右两侧趋于同一极限", ha="center",
            va="center", fontsize=9, color=GREEN)
    ax.text(0.5, 0.06, r"$\sin(3x)\sim 3x,\quad \tan(2x)\sim 2x$",
            transform=ax.transAxes, ha="center", fontsize=10, color=PURPLE)
    ax.set_xlim(-0.21, 0.21)
    ax.set_ylim(1.25, 1.64)
    ax.set_title("乘除替换：两侧趋于 1.5", fontsize=12, pad=10)
    ax.set_xlabel(r"$x$（弧度）", fontsize=9)
    ax.set_ylabel("原式的值", fontsize=10)
    legend_below(ax)


def panel_subtraction_trap(ax: plt.Axes) -> None:
    """保留加减中的高阶项，区分真实极限与错误替换推断。"""
    positive = np.logspace(-4, np.log10(0.3), 600)
    for x, label in [(-positive[::-1], r"$(\tan x-\sin x)/x^3$"),
                     (positive, "_nolegend_")]:
        # 恒等变形后计算，避免两个接近的三角函数直接相减。
        y = np.sin(x) * 2 * np.sin(x / 2)**2 / (np.cos(x) * x**3)
        ax.plot(x, y, color=BLUE, linewidth=2, label=label)
    ax.axhline(0.5, color=GREEN, linestyle=":", linewidth=1.5,
               label="真实极限：0.5")
    ax.plot(0, 0.5, marker="o", markersize=9, markerfacecolor="white",
            markeredgecolor=GREEN, markeredgewidth=1.8,
            linestyle="none", zorder=5)
    # 这条独立虚线仅表示错误推断，绝不是原式的另一条数值曲线。
    ax.axhline(0, color=RED, linestyle="--", linewidth=1.7,
               label="错误替换推断：0（非真实极限）")
    ax.text(0.5, 0.86, "空心点：原式在零点无定义",
            transform=ax.transAxes, ha="center", fontsize=9, color=GREEN)
    ax.text(0.5, 0.47, r"$\tan x-\sin x\sim x^3/2$",
            transform=ax.transAxes, ha="center", fontsize=11, color=PURPLE)
    ax.text(0.5, 0.23, "加减乱换会丢掉决定答案的高阶项",
            transform=ax.transAxes, ha="center", fontsize=9, color=RED)
    ax.set_xlim(-0.315, 0.315)
    ax.set_ylim(-0.09, 0.68)
    ax.set_title("加减陷阱：不能把差直接换成 0", fontsize=12, pad=10)
    ax.set_xlabel(r"$x$（弧度）", fontsize=9)
    ax.set_ylabel("原式的值 / 错误推断对照", fontsize=10)
    legend_below(ax)


def main() -> None:
    """创建四面板图，保存到第二讲图片目录并按后端处理窗口。"""
    setup_chinese_font()
    fig, axes = plt.subplots(2, 2, figsize=(12, 8.5), dpi=160,
                             facecolor=BACKGROUND)
    for ax in axes.flat:
        style_panel(ax)
    panel_equivalent(axes[0, 0])
    panel_orders(axes[0, 1])
    panel_product_quotient(axes[1, 0])
    panel_subtraction_trap(axes[1, 1])
    # 对数刻度包含负指数；数字刻度使用数学字体，中文标题仍用系统中文字体。
    for ax in axes.flat:
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontfamily("DejaVu Sans")
    fig.suptitle("第 02 讲 · 无穷小的比较与替换", fontsize=16, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95), h_pad=2.5, w_pad=2.0)

    output_dir = Path(__file__).resolve().parent.parent / 'assets' / 'images' / 'lecture02'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / 'infinitesimal_plots.png'
    try:
        fig.savefig(output_path, dpi=160, facecolor=BACKGROUND)
        print(f"已保存图片：{output_path}")
        if matplotlib.get_backend().lower() != "agg":
            plt.show()
        else:
            print("当前为无显示环境（Agg），跳过弹窗。")
    finally:
        plt.close(fig)


if __name__ == "__main__":
    main()
