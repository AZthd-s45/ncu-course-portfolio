# Week 05 · 单摆仿真实验（Pendulum Simulation）

## 1. 实验者信息

| 项目 | 内容 |
| --- | --- |
| 姓名 | 单 |
| 学号 | 1234567 |
| 周次 | 第 5 周 |
| 子模块目录 | `week05_pendulum_sim/` |

## 2. 实验概述

该实验实现了一个单摆的数值仿真，用于研究角度与时间的关系，基于常见的非线性摆动方程：

θ'' + (g / L) sin(θ) + c θ' = 0

其中：

- L：摆长（m）
- g：重力加速度（m/s²）
- c：阻尼系数
- θ：摆角（rad）

## 3. 目录结构

```text
week05_pendulum_sim/
├── README.md
├── __init__.py
├── __main__.py
├── requirements.txt
├── src/
│   ├── __init__.py
│   └── pendulum.py
├── data/
│   └── default_parameters.json
├── results/
│   └── pendulum.csv
```

## 4. 运行说明

在仓库根目录执行：

```bash
python -m week05_pendulum_sim --length 1.0 --gravity 9.81 --theta0 1.57 --total-time 10 --dt 0.01 --output week05_pendulum_sim/results/pendulum.csv --plot
```

也可以直接在代码中使用：

```python
from week05_pendulum_sim.src import simulate_pendulum

result = simulate_pendulum(length=1.0, gravity=9.81, theta0=1.57, total_time=10.0)
print(result[0])
print(result.theta[:5])
```

## 5. 结果说明

输出文件 `week05_pendulum_sim/results/pendulum.csv` 记录时间、角度和角速度；如果启用 `--plot`，还会生成同目录下的 `pendulum.png`。未指定 `--output` 时，CSV 默认保存在该子模块的 `results/` 目录。
