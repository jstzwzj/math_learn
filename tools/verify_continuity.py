#!/usr/bin/env python3
r"""用数值计算演示第 04 讲：连续性、间断点与闭区间连续函数的性质。

配套笔记: notes/第04讲-连续性与间断点.md
运行（macOS/Linux）: python3 tools/verify_continuity.py
运行（Windows）:     python tools\verify_continuity.py
依赖: 仅 Python 标准库（math、sys、typing），无需安装任何东西
输出: 五组文字对照，不生成文件、不弹窗

  1. 连续与可去间断：比较点附近的值、点本身的值，以及修复后的值
  2. 跳跃、无穷、振荡：用左右逼近和两组特意构造的输入观察间断
  3. 对数的连续性：第二个重要极限两边取对数，结果趋近 1
  4. 闭区间最值与开区间反例：网格采样对照手算结果，观察端点取不到
  5. 二分法与反例：连续多项式找到近似根，跳跃函数只逼近跳点

注意: 数值演示不代替证明；二分法的连续性前提需要调用者检查。
"""

import math
import sys
from typing import Callable, Tuple

# Windows 老控制台兜底：打不出的字符用 "?" 代替而不是崩溃（PS7 / macOS / Linux 无影响）
sys.stdout.reconfigure(errors="replace")


def section(title: str) -> None:
    print(f"\n{'=' * 60}\n{title}\n{'=' * 60}")


def patched_ratio(x: float, value_at_one: float) -> float:
    """非特殊点等于 (x^2-1)/(x-1)，特殊点按指定值返回。"""
    if x == 1.0:
        return value_at_one
    # 先约分成 x+1，避免在 1 附近做两个几乎相等的数的减法。
    return x + 1.0


def jump(x: float) -> float:
    """跳跃函数只输出 -1 或 1，没有零点。"""
    return -1.0 if x < 0.0 else 1.0


def polynomial(x: float) -> float:
    """连续多项式，配套笔记第 6 节的二分对象。"""
    return x**3 - x - 2.0


def bisect_interval(
    function: Callable[[float], float],
    left: float,
    right: float,
    steps: int,
) -> Tuple[float, float]:
    """最多二分 steps 次，返回最后保留的区间（遇到精确零点则两端相等）。

    调用者须确认 function 在整个初始闭区间上连续。
    代码只能检查有限函数值与端点符号，不能据此证明连续性。
    """
    if not (math.isfinite(left) and math.isfinite(right)) or left >= right:
        raise ValueError("需要有限的左右端点，且左端点小于右端点")
    if steps < 0:
        raise ValueError("二分次数不能为负数")

    f_left = function(left)
    f_right = function(right)
    if not (math.isfinite(f_left) and math.isfinite(f_right)):
        raise ValueError("端点函数值必须是有限数")
    if f_left == 0.0:
        return left, left
    if f_right == 0.0:
        return right, right
    # 直接比较符号，避免用乘积判断时出现浮点溢出或下溢。
    if (f_left < 0.0) == (f_right < 0.0):
        raise ValueError("端点必须异号，或某个端点本身就是零点")

    for _ in range(steps):
        midpoint = left / 2.0 + right / 2.0
        if midpoint == left or midpoint == right:
            # 浮点数已无法表示更细的中点，继续循环也不会缩小区间。
            break
        f_midpoint = function(midpoint)
        if not math.isfinite(f_midpoint):
            raise ValueError("中点函数值必须是有限数")
        if f_midpoint == 0.0:
            return midpoint, midpoint

        # 循环不变量：两个端点始终异号，连续时区间内始终有根。
        if (f_left < 0.0) == (f_midpoint < 0.0):
            left = midpoint
            f_left = f_midpoint
        else:
            right = midpoint

    return left, right


def main() -> None:
    section("1. 连续与可去间断：点附近的趋势，要与点本身接上")
    print("连续例子 f(x)=x^2，目标 f(1)=1：")
    for h in [0.1, 0.01, 0.001, 0.0001]:
        print(f"h={h:<7g}  f(1-h)={(1-h)**2:.8f}  f(1+h)={(1+h)**2:.8f}")

    print("\n可去间断 g：x!=1 时 g(x)=(x^2-1)/(x-1)=x+1，g(1)=0：")
    for h in [0.1, 0.01, 0.001, 0.0001]:
        print(f"h={h:<7g}  g(1-h)={patched_ratio(1-h, 0.0):.8f}"
              f"  g(1+h)={patched_ratio(1+h, 0.0):.8f}")
    print(f"点本身：g(1)={patched_ratio(1.0, 0.0):.1f}，与附近逼近的 2 不同。")
    print(f"补上正确值：g(1)={patched_ratio(1.0, 2.0):.1f}，现在与极限接上了。")
    print("只修改一个点，不会改变原来的极限；但可以改变是否连续。")

    section("2. 跳跃、无穷、振荡：修改一个点的值也修不好")
    print("跳跃函数 j(x)：左侧恒为 -1，右侧恒为 1：")
    for h in [0.1, 0.01, 0.001]:
        print(f"h={h:<7g}  j(-h)={jump(-h):+.1f}  j(h)={jump(h):+.1f}")
    print("左右极限都有限，却不同，所以双侧极限不存在。")

    print("\n无穷间断 1/x：输入越接近 0，输出的绝对值越大：")
    for h in [0.1, 0.01, 0.001, 0.0001]:
        print(f"h={h:<7g}  1/(-h)={-1/h:>9.1f}  1/h={1/h:>9.1f}")

    print("\n振荡 sin(1/x)：不是乱抽样，而是构造两组都从正侧趋于 0 的输入：")
    for n in [1, 10, 100, 1000]:
        x_n = 1.0 / (2.0 * math.pi * n + math.pi / 2.0)
        y_n = 1.0 / (2.0 * math.pi * n + 3.0 * math.pi / 2.0)
        print(f"n={n:<4}  x_n={x_n:.8e}  sin(1/x_n)={math.sin(1/x_n):+.6f}"
              f"  y_n={y_n:.8e}  sin(1/y_n)={math.sin(1/y_n):+.6f}")
    print("数学上两组输出恒为 +1 与 -1；浮点计算可能有微小舍入误差。")
    print("沿两组趋于 0 的输入得到不同结果，右极限不可能存在。")

    section("3. 极限穿过对数：为什么第 03 讲可以两边取 ln？")
    print("ln 在正数 e 处连续，所以底数趋近 e 时，其对数趋近 ln(e)=1。")
    print("用 log1p(x) 稳定计算 ln(1+x)，避免小量相加丢失精度：\n")
    for h in [0.1, 0.01, 0.001, 0.0001]:
        for x in [-h, h]:
            logarithm = math.log1p(x) / x
            value = math.exp(logarithm)
            print(f"x={x:+.4f}  (1+x)^(1/x)={value:.10f}"
                  f"  ln(1+x)/x={logarithm:.10f}")
    print(f"对照：e={math.e:.10f}，ln(e)={math.log(math.e):.1f}。")

    section("4. 闭区间上的最值：对照手算结果，而不是把采样当证明")
    print("f(x)=x(1-x) 在 [0,1] 上连续。手算：最大值 0.25，最小值 0。")
    print("将区间分成 n 等份，采样包含两个端点：\n")
    for n in [5, 10, 100]:
        points = [i / n for i in range(n + 1)]
        values = [x * (1.0 - x) for x in points]
        x_at_max = max(points, key=lambda x: x * (1.0 - x))
        print(f"n={n:<3}  网格最小值={min(values):.6f}"
              f"  网格最大值={max(values):.6f}  最大值的一个采样点={x_at_max:.2f}")
    print("观察：n=5 的网格没采到 x=0.5，所以漏掉了真正的最大值。")
    print("n 为偶数时采到了中点，才与手算最大值一致。有限网格不能代替定理。")

    print("\n开区间反例：f(x)=x 在 (0,1) 上连续，没有最大值；输出能逼近 1，却取不到 1：")
    for n in [10, 100, 1000, 10000]:
        x = 1.0 - 1.0 / n
        print(f"n={n:<5}  x=1-1/n={x:.8f}  f(x)={x:.8f} < 1")
    print("所有输入和输出都小于 1；任意候选最大值还可以被更大的输出超过。")
    print("同理，0 只能逼近，也取不到。这里说的是精确实数，不是舍入后的显示值。")

    section("5. 同一段二分代码：连续函数逼近根，跳跃函数只逼近跳点")
    print("连续例子 f(x)=x^3-x-2：f(1)=-2，f(2)=4，区间内至少有一个根。")
    print("理论上的根误差上界来自区间半宽，每次减半；残差不保证每一步都变小：\n")
    for steps in [0, 1, 2, 4, 8, 10, 16]:
        left, right = bisect_interval(polynomial, 1.0, 2.0, steps)
        midpoint = (left + right) / 2.0
        width = right - left
        print(f"次数={steps:>2}  中点={midpoint:.9f}  宽度={width:.9f}"
              f"  半宽={width/2:.9f}  残差={polynomial(midpoint):+.6e}")

    print("\n反例 j(x)=-1（x<0），j(x)=1（x>=0），在 [-1,1] 上端点异号。")
    print("故意违反连续性前提，看看相同的符号更新会发生什么：\n")
    for steps in [0, 1, 2, 4, 8, 10, 16]:
        left, right = bisect_interval(jump, -1.0, 1.0, steps)
        midpoint = (left + right) / 2.0
        print(f"次数={steps:>2}  中点={midpoint:+.9f}  宽度={right-left:.9f}"
              f"  残差={jump(midpoint):+.1f}")
    print("区间越来越窄，但残差的绝对值始终为 1：它没有零点！")
    print("这不是二分更新写错了，而是连续性前提不满足。")
    print("端点符号检查只能检查异号，不能证明函数连续。")

    print("\n动手：把二分对象换成 lambda x: math.cos(x)-x，初始区间改为 [0,1]。")
    print("先按笔记练习 5 检查连续与异号，再看中点是否逼近 0.739085。")
    print("本脚本的所有数值结果都用于观察和核对，不代替数学证明。")


if __name__ == "__main__":
    main()
