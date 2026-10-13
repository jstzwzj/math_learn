#!/usr/bin/env python3
r"""把第 03 讲的第二个重要极限与复利故事画成四面板数学图。

对应笔记：notes/第03讲-第二个重要极限与e.md
运行（macOS/Linux）：python3 tools/visualize_e_limit.py
运行（Windows）：    python tools\visualize_e_limit.py
依赖：现有 matplotlib、numpy 及 Python 标准库，兼容 Python 3.8+。
无显示环境可设置 MPLBACKEND=Agg，只保存图片、不弹窗。

内容与输出列表：
  1. 整数付息次数增加，复利终值从下方逼近 e。
  2. 用 |x| 对齐正负两侧，展示从下方和上方逼近 e。
  3. t 趋于 0 的左右两段，以及原式在 0 处未定义的空心点。
  4. 不同 A 对应不同极限 e^A，说明 1^∞ 型不是固定答案。
  5. 保存 assets/images/lecture03/e_limit_plots.png；非 Agg 后端弹窗。

脚本独立运行，不导入仓库其他脚本；所有幂式用 log1p 稳定计算。
"""

import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager, rcParams

# Windows 老控制台兜底：打不出的字符用 "?" 代替而不是崩溃（PS7 / macOS / Linux 无影响）
sys.stdout.reconfigure(errors="replace")

BLUE = "#2563eb"
GREEN = "#059669"
ORANGE = "#d97706"
PURPLE = "#7c3aed"
RED = "#dc2626"
BACKGROUND = "#f7f9fc"


def setup_chinese_font() -> None:
    """按平台挑一个可用的中文字体，避免图里中文变方框。"""
    candidates = [
        # macOS
        "PingFang SC", "Hiragino Sans GB", "Arial Unicode MS", "Heiti TC", "STHeiti",
        # Windows
        "Microsoft YaHei", "SimHei", "SimSun",
        # Linux
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
    """统一白色坐标区与浅色网格，保留数学图的可读性。"""
    ax.set_facecolor("white")
    ax.set_axisbelow(True)
    ax.grid(True, which="major", color="#e2e8f0", linewidth=0.7)
    ax.tick_params(axis="both", labelsize=9)
    for spine in ax.spines.values():
        spine.set_color("#cbd5e1")


def add_legend(ax: plt.Axes) -> None:
    """将图例放在坐标区下方，避免遮挡曲线和数学标注。"""
    ax.legend(
        loc="upper left", bbox_to_anchor=(0, -0.22),
        ncol=2, fontsize=8, frameon=False, borderaxespad=0,
    )


def panel_compound_interest(ax: plt.Axes) -> None:
    """整数 n 的复利数列从下方逼近 e，所有绘制点均为有限项。"""
    # 对数采样后取整去重：横轴仍然是整数次数，不是连续实数。
    n = np.unique(np.concatenate((
        np.rint(np.geomspace(1, 1_000_000, 700)).astype(np.int64),
        np.array([1, 2, 12, 365], dtype=np.int64),
    )))
    values = np.exp(n * np.log1p(1.0 / n))
    ax.plot(n, values, color=BLUE, linewidth=2,
            label=r"复利终值 $(1+1/n)^n$")
    ax.axhline(np.e, color=RED, linestyle="--", linewidth=1.3,
               label=r"极限 $e\approx 2.71828$")

    # 标注使用坐标区比例定位，避免挤在收敛曲线附近。
    examples = [
        (1, "一年一次", (0.08, 0.22)),
        (2, "半年一次", (0.23, 0.40)),
        (12, "每月一次", (0.40, 0.59)),
        (365, "每日一次", (0.64, 0.73)),
    ]
    for count, text, position in examples:
        value = float(np.exp(count * np.log1p(1.0 / count)))
        ax.plot(count, value, "o", color=ORANGE, markersize=5, zorder=4)
        ax.annotate(
            f"{text}\n次数 {count}，终值 {value:.4f}",
            xy=(count, value), xytext=position, textcoords="axes fraction",
            fontsize=8, color=ORANGE,
            arrowprops=dict(arrowstyle="->", color=ORANGE, linewidth=0.9),
        )
    ax.set_xscale("log")
    ax.set_xlim(0.8, 1_500_000)
    ax.set_ylim(1.94, 2.82)
    ax.set_title("复利：从下方逼近 e", fontsize=12)
    ax.set_xlabel(r"一年付息次数 $n$（整数，对数轴）")
    ax.set_ylabel("一年后的终值（元）")
    add_legend(ax)


def panel_two_sides(ax: plt.Axes) -> None:
    """用正数 s=|x| 对齐两侧，不把负 x 错画在正 x 横轴上。"""
    s = np.geomspace(2.0, 10_000.0, 600)
    positive = np.exp(s * np.log1p(1.0 / s))
    negative = np.exp(-s * np.log1p(-1.0 / s))
    ax.plot(s, positive, color=BLUE, linewidth=2,
            label=r"下方：$x=s\to +\infty$")
    ax.plot(s, negative, color=PURPLE, linewidth=2,
            label=r"上方：$x=-s\to -\infty$")
    ax.axhline(np.e, color=RED, linestyle="--", linewidth=1.3,
               label=r"共同极限 $e$")
    ax.text(0.97, 0.90, r"$(1+1/x)^x$", transform=ax.transAxes,
            ha="right", fontsize=13, color=PURPLE)
    ax.text(0.97, 0.77, "负侧取 x <= -2，底数保持为正", transform=ax.transAxes,
            ha="right", fontsize=8, color=PURPLE)
    ax.set_xscale("log")
    ax.set_xlim(2, 10_000)
    ax.set_ylim(2.12, 4.15)
    ax.set_title("正负两侧：一下一上", fontsize=12)
    ax.set_xlabel(r"大小 $s=|x|$（不是 $x$，对数轴）")
    ax.set_ylabel("幂式的值")
    add_legend(ax)


def panel_near_zero(ax: plt.Axes) -> None:
    """分别计算 t 的负段与正段，原式在 t=0 处不计算也不连接。"""
    # 两段都满足 t>-1；最近点为 ±10^-6，不包含 0。
    distance = np.geomspace(1e-6, 0.6, 600)
    left = -distance[::-1]
    right = distance
    ax.plot(left, np.exp(np.log1p(left) / left), color=PURPLE,
            linewidth=2, label=r"左侧 $t\to 0^-$")
    ax.plot(right, np.exp(np.log1p(right) / right), color=GREEN,
            linewidth=2, label=r"右侧 $t\to 0^+$")
    ax.axhline(np.e, color=RED, linestyle="--", linewidth=1.3,
               label=r"共同极限 $e$")
    # 白色填充盖住参考线，让空心点明确表示原式未定义，而非函数值。
    ax.plot(0, np.e, "o", markersize=9, markerfacecolor="white",
            markeredgecolor=RED, markeredgewidth=1.8, zorder=5)
    ax.annotate(
        "空心点：原式在 t=0 未定义\n左右极限都为 e",
        xy=(0, np.e), xytext=(0.54, 0.74), textcoords="axes fraction",
        fontsize=9, color=RED,
        arrowprops=dict(arrowstyle="->", color=RED, linewidth=1),
    )
    ax.set_xlim(-0.65, 0.65)
    ax.set_ylim(2.0, 4.8)
    ax.set_title(r"换元：$(1+t)^{1/t}\to e$", fontsize=12)
    ax.set_xlabel(r"增量 $t$（趋于 0，且 $t>-1$）")
    ax.set_ylabel("幂式的值")
    add_legend(ax)


def panel_indeterminate(ax: plt.Axes) -> None:
    """对比四个 A：极限由 A 决定，A=0 时每一项恒等于 1。"""
    n = np.unique(np.rint(np.geomspace(10, 10_000, 600)).astype(np.int64))
    cases = [
        (-1, PURPLE, r"$e^{-1}\approx 0.3679$"),
        (0, GREEN, r"$e^0=1$"),
        (1, BLUE, r"$e\approx 2.7183$"),
        (2, ORANGE, r"$e^2\approx 7.3891$"),
    ]
    for a, color, limit_label in cases:
        # n>=10 保证所有底数为正；A=0 的指数恰为 0，结果恒为 1。
        values = np.exp(n * np.log1p(a / n))
        limit = float(np.exp(a))
        ax.plot(n, values, color=color, linewidth=2, label=f"参数 A={a}")
        ax.axhline(limit, color=color, linestyle="--", linewidth=0.8, alpha=0.5)
        # 标签写明极限，不把有限末项误称为已经到达终值。
        ax.annotate(
            "极限 " + limit_label, xy=(1, limit),
            xycoords=ax.get_yaxis_transform(), xytext=(7, 0),
            textcoords="offset points", va="center", fontsize=8, color=color,
            annotation_clip=False,
        )
    ax.set_xscale("log")
    ax.set_xlim(10, 10_000)
    ax.set_ylim(-0.15, 8.05)
    ax.set_title(r"不同参数：$(1+A/n)^n\to e^A$", fontsize=12)
    ax.set_xlabel(r"次数 $n\geq 10$（整数，对数轴）")
    ax.set_ylabel("幂式的值")
    add_legend(ax)


def main() -> None:
    """绘制四面板，保存到固定目录，按后端决定是否弹窗并关闭画布。"""
    setup_chinese_font()
    fig, axes = plt.subplots(2, 2, figsize=(12, 8.5), dpi=160,
                             facecolor=BACKGROUND)
    try:
        for ax in axes.flat:
            style_panel(ax)
        panel_compound_interest(axes[0, 0])
        panel_two_sides(axes[0, 1])
        panel_near_zero(axes[1, 0])
        panel_indeterminate(axes[1, 1])
        fig.suptitle("第 03 讲 · 第二个重要极限与 e", fontsize=16,
                     fontweight="bold", color=BLUE)
        fig.text(
            0.5, 0.025,
            r"$1^{\infty}$ 型是不定式，不是固定答案；底数减 1 与指数的乘积决定这里的极限。",
            ha="center", fontsize=10, color=RED,
        )
        fig.tight_layout(rect=(0, 0.065, 1, 0.95), h_pad=2.0, w_pad=2.0)

        output_dir = (Path(__file__).resolve().parent.parent
                      / "assets" / "images" / "lecture03")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "e_limit_plots.png"
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
