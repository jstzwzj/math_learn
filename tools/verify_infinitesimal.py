#!/usr/bin/env python3
"""用数值计算验证第 02 讲的结论：等价无穷小与极限运算法则。

运行（macOS/Linux）: python3 tools/verify_infinitesimal.py
运行（Windows）:     python tools\verify_infinitesimal.py
依赖: 仅标准库 math，无需安装任何东西

四个验证:
  1. 六个常用等价无穷小（x->0 时每个比值都应趋于 1）
  2. 高阶无穷小：x^2 比 x 消失得更快（高数版复杂度分析）
  3. 等价替换实战：lim_{x->0} sin(3x)/tan(2x) = 3/2
  4. 经典陷阱：(tan(x)-sin(x))/x^3 —— 加减中乱换等价无穷小会丢掉答案
"""

import math
import sys

# Windows 老控制台兜底：打不出的字符用 "?" 代替而不是崩溃（PS7 / macOS / Linux 无影响）
sys.stdout.reconfigure(errors="replace")


def section(title: str) -> None:
    print(f"\n{'=' * 50}\n{title}\n{'=' * 50}")


# ---------------------------------------------------------------
section("1. 常用等价无穷小：x->0 时，每个比值都应趋于 1")

# ln(1+x) 用 log1p、e^x-1 用 expm1：这两个函数专门为"相近数相减"设计，
# 它们存在的理由正是第 4 节要演示的"灾难性抵消"。
equivalences = [
    ("sin(x) / x",            lambda x: math.sin(x) / x),
    ("tan(x) / x",            lambda x: math.tan(x) / x),
    ("(1-cos(x)) / (x^2/2)",  lambda x: (1 - math.cos(x)) / (x**2 / 2)),
    ("ln(1+x) / x",           lambda x: math.log1p(x) / x),
    ("(e^x - 1) / x",         lambda x: math.expm1(x) / x),
    ("(sqrt(1+x)-1) / (x/2)", lambda x: (math.sqrt(1 + x) - 1) / (x / 2)),
]

for x in [0.1, 0.01, 0.001, 0.0001]:
    print(f"\nx = {x}")
    for name, f in equivalences:
        print(f"  {name:<24} = {f(x):.9f}")

print("\n观察：x 每缩小 10 倍，所有比值都更贴近 1。'等价'不是约等于，是比值的极限 = 1。")

# ---------------------------------------------------------------
section("2. 高阶无穷小：x^2 比 x 消失得更快")

for x in [0.1, 0.01, 0.001, 0.0001]:
    print(f"x = {x:<8}  x^2 = {x**2:.10f}    比值 x^2/x = {x:g}  -> 0")

print("\n观察：x^2/x -> 0，说明 x^2 是 x 的高阶无穷小（记作 x^2 = o(x)）。")
print("类比复杂度：n 和 100n 同阶，n^2 比 n 高阶——那边比'长得快'，这边比'消失快'。")

# ---------------------------------------------------------------
section("3. 等价替换实战：lim_{x->0} sin(3x)/tan(2x)")

print("替换依据：sin(3x) ~ 3x，tan(2x) ~ 2x，所以极限 = 3x/2x = 3/2 = 1.5\n")
for x in [0.1, 0.01, 0.001, 0.0001]:
    value = math.sin(3 * x) / math.tan(2 * x)
    print(f"x = {x:<8}  sin(3x)/tan(2x) = {value:.9f}")

print("\n观察：确实逼近 1.5。等价替换把三角函数极限'秒'成了小学除法。")

# ---------------------------------------------------------------
section("4. 经典陷阱：(tan(x)-sin(x))/x^3 —— 加减中不能乱换等价无穷小")

print("错误做法：tan(x)~x、sin(x)~x 代入 -> (x-x)/x^3 = 0")
print("正确做法：tan(x)-sin(x) = sin(x)(1-cos(x))/cos(x) ~ x*(x^2/2)/1 = x^3/2，极限 = 1/2\n")
for x in [0.1, 0.01, 0.001, 0.0001]:
    direct = (math.tan(x) - math.sin(x)) / x**3
    print(f"x = {x:<8}  直接算 = {direct:.9f}    （错误替换得 0，正确答案 0.5）")

print("\n观察：直接算稳稳逼近 0.5，而'两项都换成 x'得到 0——差之毫厘，谬以千里。")
print("原因：tan(x) 与 sin(x) 的差全藏在被丢掉的高阶项里，换完等于把答案扔了。")
print("这就是浮点数里的'灾难性抵消'，math.log1p / math.expm1 正是为躲开它而设计的。")
