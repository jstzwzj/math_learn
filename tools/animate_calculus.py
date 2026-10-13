#!/usr/bin/env python3
r"""把微积分里"动起来才好懂"的概念做成 GIF 动画。

导读笔记: notes/第01讲-极限的直觉.md（预告第 05、09、14 讲）

运行（macOS/Linux）: python3 tools/animate_calculus.py
运行（Windows）:     python tools\animate_calculus.py
  - 生成三个 GIF 到 assets/animations/ 目录
  - 在有显示环境时会弹出三个动画窗口（关闭即退出）
依赖: matplotlib + pillow（pip install -r requirements.txt），macOS/Windows/Linux 通用，中文字体自动选择

三个动画分别预告三大核心概念:
  1. secant_to_tangent.gif  割线 -> 切线（导数的定义，第 05 讲）
  2. riemann_sum.gif        矩形逐渐填满曲线下面积（定积分的定义，第 14 讲）
  3. taylor_sin.gif         多项式逐阶逼近 sin（泰勒公式，第 09 讲）
"""

import math
import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager, rcParams
from matplotlib.animation import FuncAnimation, PillowWriter

# Windows 老控制台兜底：打不出的字符用 "?" 代替而不是崩溃（PS7 / macOS / Linux 无影响）
sys.stdout.reconfigure(errors="replace")

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "animations"


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
            rcParams["font.sans-serif"] = [name]
            break
    else:
        print("警告：未找到可用中文字体，图中文字可能显示为方框"
              "（macOS/Windows 一般自带中文字体，Linux 可安装 Noto Sans CJK）。")
    rcParams["axes.unicode_minus"] = False


def make_secant_animation() -> FuncAnimation:
    """动画 1：割线绕定点转动，最终落在切线上。f(x)=x^2 在 x=3 处。"""
    fig, ax = plt.subplots(figsize=(6.5, 5))
    x = np.linspace(0, 4.5, 300)
    frames = 60

    def draw(frame: int) -> None:
        h = 2 * 0.93**frame          # h 指数式衰减到 ~0
        if frame == frames - 1:
            h = 0.0                  # 最后一帧：h=0，真正的切线
        ax.cla()
        ax.plot(x, x**2, lw=2, color="#1f77b4", label=r"$f(x)=x^2$")
        ax.plot(3, 9, "o", color="black")
        slope = 6 + h                # ((3+h)^2-9)/h = 6+h
        if h > 0:
            ax.plot(3 + h, (3 + h) ** 2, "s", color="#d62728")
            xs = np.linspace(1.5, 4.4, 10)
            ax.plot(xs, slope * (xs - 3) + 9, color="#d62728", lw=1.5)
            ax.set_title(f"割线斜率 = {slope:.3f}    (h = {h:.3f})")
        else:
            xs = np.linspace(1.2, 4.5, 10)
            ax.plot(xs, 6 * (xs - 3) + 9, color="red", lw=2.5)
            ax.set_title("h = 0：割线的极限位置 = 切线，斜率 f'(3) = 6")
        ax.set_xlim(0, 4.6)
        ax.set_ylim(0, 21)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend(loc="upper left")

    anim = FuncAnimation(fig, draw, frames=frames, interval=80)
    anim.save(OUTPUT_DIR / "secant_to_tangent.gif", writer=PillowWriter(fps=12))
    print("已生成 secant_to_tangent.gif")
    return anim


def make_riemann_animation() -> FuncAnimation:
    """动画 2：矩形越来越多，逐渐填满曲线下的面积。f(x)=x^2 在 [0,2]。"""
    fig, ax = plt.subplots(figsize=(6.5, 5))
    x = np.linspace(0, 2.05, 400)
    a, b = 0.0, 2.0
    exact = 8 / 3
    ns = [4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128]

    def draw(i: int) -> None:
        n = ns[i]
        width = (b - a) / n
        midpoints = (np.arange(n) + 0.5) * width
        heights = midpoints**2
        rect_sum = heights.sum() * width
        ax.cla()
        ax.plot(x, x**2, lw=2, color="#1f77b4", label=r"$f(x)=x^2$")
        ax.bar(midpoints, heights, width=width, alpha=0.45,
               color="#ff9896", edgecolor="#d62728", linewidth=0.5)
        ax.set_title(f"n = {n} 个矩形：面积和 = {rect_sum:.4f}")
        ax.text(0.05, 3.35,
                f"精确值 $\\int_0^2 x^2\\,dx$ = 8/3 ≈ 2.6667\n误差 = {abs(rect_sum - exact):.4f}",
                fontsize=10)
        ax.set_xlim(0, 2.1)
        ax.set_ylim(0, 4.2)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend(loc="lower right")

    anim = FuncAnimation(fig, draw, frames=len(ns), interval=1200)
    anim.save(OUTPUT_DIR / "riemann_sum.gif", writer=PillowWriter(fps=1))
    print("已生成 riemann_sum.gif")
    return anim


def make_taylor_animation() -> FuncAnimation:
    """动画 3：泰勒多项式阶数升高，逐阶逼近 sin(x)。"""
    fig, ax = plt.subplots(figsize=(6.5, 5))
    x = np.linspace(-2 * np.pi, 2 * np.pi, 600)
    degrees = [1, 3, 5, 7, 9, 11, 15, 19, 25, 31]

    def taylor_sin(x: np.ndarray, degree: int) -> np.ndarray:
        y = np.zeros_like(x)
        for k in range((degree + 1) // 2):
            y += (-1) ** k * x ** (2 * k + 1) / math.factorial(2 * k + 1)
        return y

    def draw(i: int) -> None:
        degree = degrees[i]
        ax.cla()
        ax.plot(x, np.sin(x), lw=2.5, color="gray", ls="--", label=r"$\sin x$（真身）")
        ax.plot(x, taylor_sin(x, degree), lw=2, color="#1f77b4",
                label=f"泰勒多项式（阶数 {degree}）")
        ax.set_title(f"泰勒多项式逼近 sin(x)：当前阶数 = {degree}")
        ax.set_xlim(-2 * np.pi, 2 * np.pi)
        ax.set_ylim(-3, 3)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend(loc="lower left")

    anim = FuncAnimation(fig, draw, frames=len(degrees), interval=1500)
    anim.save(OUTPUT_DIR / "taylor_sin.gif", writer=PillowWriter(fps=1))
    print("已生成 taylor_sin.gif")
    return anim


def main() -> None:
    setup_chinese_font()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    anims = [
        make_secant_animation(),
        make_riemann_animation(),
        make_taylor_animation(),
    ]

    if matplotlib.get_backend().lower() != "agg":
        print("三个动画窗口已弹出（每个窗口内自动循环播放），关闭窗口即退出。")
        plt.show()
    else:
        plt.close("all")
        print("当前为无显示环境（Agg），仅保存 GIF。")


if __name__ == "__main__":
    main()
