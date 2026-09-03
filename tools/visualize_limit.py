#!/usr/bin/env python3
"""把第 01 讲的四个极限结论画出来（可视化版）。

运行: python3 tools/visualize_limit.py
  - 弹出图窗口，同时保存 PNG 到 tools/limit_plots.png
  - 在无显示环境（MPLBACKEND=Agg）下只保存不弹窗
依赖: matplotlib（pip3 install --user matplotlib）

四个面板:
  1. 数列 n/(n+1) 收敛到 1 —— 趋势逼近但永远不到达
  2. sin(x)/x 在 x->0 时趋于 1 —— 注意 x=0 处是"空心点"
  3. 割线逼近切线 —— 导数是差商的极限（第 05 讲预告）
  4. sin(1/x) 在 x->0 附近震荡 —— 极限不存在的反例
"""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager, rcParams


def setup_chinese_font() -> None:
    """macOS 上挑一个可用的中文字体，避免图里中文变方框。"""
    candidates = ["PingFang SC", "Hiragino Sans GB", "Arial Unicode MS", "Heiti TC", "STHeiti"]
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            rcParams["font.sans-serif"] = [name]
            break
    rcParams["axes.unicode_minus"] = False


def panel_sequence(ax: plt.Axes) -> None:
    """1. 数列 n/(n+1) -> 1"""
    n = np.arange(1, 26)
    a_n = n / (n + 1)
    ax.plot(n, a_n, "o-", ms=4, color="#1f77b4", label=r"$a_n = \frac{n}{n+1}$")
    ax.axhline(1, color="red", ls="--", lw=1, label="极限值 1")
    ax.set_title("数列收敛：$n/(n+1) \\to 1$（逼近但永远不到达）")
    ax.set_xlabel("n")
    ax.set_ylabel(r"$a_n$")
    ax.legend(loc="lower right")


def panel_sin_over_x(ax: plt.Axes) -> None:
    """2. sin(x)/x -> 1 (x->0)"""
    x = np.linspace(-8, 8, 2001)
    with np.errstate(invalid="ignore"):
        y = np.where(x == 0, np.nan, np.sin(x) / x)  # x=0 处 0/0，置为 nan 留出"空心"
    ax.plot(x, y, color="#1f77b4", label=r"$f(x)=\frac{\sin x}{x}$")
    ax.axhline(1, color="red", ls="--", lw=1, label="极限值 1")
    # x=0 处函数无定义，但极限存在——画一个"空心点"
    ax.plot(0, 1, "o", ms=12, mfc="none", mec="red", mew=2)
    ax.annotate("空心点：x=0 无定义，\n但左右两侧都逼近 1", xy=(0, 1), xytext=(2.2, 0.55),
                fontsize=9, color="red", arrowprops=dict(arrowstyle="->", color="red"))
    ax.set_title(r"第一个重要极限：$\sin(x)/x \to 1 \ (x \to 0)$")
    ax.set_xlabel("x（弧度）")
    ax.set_ylabel("f(x)")
    ax.legend(loc="lower left")


def panel_secant_to_tangent(ax: plt.Axes) -> None:
    """3. 割线逼近切线：f(x)=x^2 在 x=3 处"""
    x = np.linspace(0, 4.5, 200)
    ax.plot(x, x**2, color="#1f77b4", lw=2, label=r"$f(x)=x^2$")
    ax.plot(3, 9, "ko", ms=6)
    ax.annotate("(3, 9)", xy=(3, 9), xytext=(2.0, 13.5), fontsize=9,
                arrowprops=dict(arrowstyle="->", color="black"))
    # 切线：斜率 6
    xs = np.linspace(1.2, 4.5, 50)
    ax.plot(xs, 6 * (xs - 3) + 9, color="red", lw=2.5,
            label=r"切线（斜率 $f'(3)=6$）")
    # 三条割线：h 越小越贴近切线
    for h, color, alpha in [(1.5, "#ff9896", 0.9), (0.6, "#d62728", 0.6), (0.15, "#9467bd", 0.9)]:
        slope = 6 + h  # ((3+h)^2 - 9)/h = 6 + h
        xs = np.linspace(1.6, 4.4, 50)
        ax.plot(xs, slope * (xs - 3) + 9, color=color, lw=1.4, alpha=alpha,
                label=f"割线 h={h}（斜率 {slope}）")
        ax.plot(3 + h, (3 + h) ** 2, "s", ms=5, color=color)
    ax.set_title("割线 → 切线：导数是差商的极限")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="upper left", fontsize=8)


def panel_sin_one_over_x(ax: plt.Axes) -> None:
    """4. sin(1/x)：极限不存在的反例"""
    x = np.linspace(-0.4, 0.4, 40001)
    x = x[x != 0.0]
    ax.plot(x, np.sin(1 / x), lw=0.5, color="#1f77b4")
    ax.axvline(0, color="gray", ls="--", lw=1)
    ax.set_title(r"$\sin(1/x)$：在 $x=0$ 附近无限震荡，极限不存在")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.text(0.08, -0.8, "越靠近 0 震荡越密集，\n不趋于任何数", fontsize=9, color="gray")


def main() -> None:
    setup_chinese_font()

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    panel_sequence(axes[0][0])
    panel_sin_over_x(axes[0][1])
    panel_secant_to_tangent(axes[1][0])
    panel_sin_one_over_x(axes[1][1])
    fig.suptitle("第 01 讲 · 用眼睛看极限", fontsize=15, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    out_path = Path(__file__).resolve().parent / "limit_plots.png"
    fig.savefig(out_path, dpi=150)
    print(f"已保存图片: {out_path}")

    if matplotlib.get_backend().lower() != "agg":
        plt.show()
    else:
        print("当前为无显示环境（Agg），跳过弹窗。")


if __name__ == "__main__":
    main()
