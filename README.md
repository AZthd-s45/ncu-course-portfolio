# 南昌大学课程实验作品集

<p align="center">
  <img src="https://www.ncu.edu.cn/images/logo.png" alt="南昌大学校徽" width="160"><br>
  <strong>南昌大学</strong><br>
  <sub>NANCHANG UNIVERSITY · COURSE PORTFOLIO</sub>
</p>

记录一个学期的课程实验、代码与结果。

## 个人信息

| 项目 | 内容 |
| --- | --- |
| 学号 | 1234567 |
| 姓名 | 单 |
| 专业 | 待填写 |

## 实验目录

```text
NCU-course-portfolio/
├── week01_experiment/
├── week02_experiment/
├── week03_experiment/
├── week04_experiment/
├── week05_pendulum_sim/
├── week06_experiment/
├── week07_experiment/
├── week08_experiment/
├── week09_experiment/
├── week10_experiment/
├── week11_experiment/
├── week12_experiment/
├── week13_experiment/
├── week14_experiment/
├── week15_experiment/
└── week16_experiment/
```

每周实验在对应目录中整理；第五周为单摆仿真实验。

## 已完成：Week 05 单摆仿真

已在 `week05_pendulum_sim/` 中实现最小可运行的单摆仿真模型，包含：

- `src/pendulum.py`：仿真核心逻辑、RK4/欧拉步进与结果保存
- `__main__.py`：命令行入口，可直接运行仿真
- `data/default_parameters.json`：默认参数配置
- `results/`：仿真输出目录

运行示例：

```bash
python -m week05_pendulum_sim --theta0 1.57 --total-time 10 --dt 0.01 --output week05_pendulum_sim/results/pendulum.csv --plot
```

输出会生成 CSV 轨迹以及可选的 PNG 图像。