# PrefixCast

**基于指数加权联合路径与树模型回退的金融概率预测**

[English](README.md)

PrefixCast 是 HaHaHa 队伍在 **Agenthon 2026 Track 2 获得第二名的最终预测系统**。[官方 Final 榜单](https://www.agenthon.net/#leaderboard)显示分数 **−0.9513**，越高越好；核对日期为 2026-11-03。

## 方法

整个系统只有一个预测入口，由程序根据当前任务自动选择执行路径：

| 组件 | 在最终系统中的作用 |
|---|---|
| 指数加权联合路径 | 对满足条件的日频利率和 G10 外汇短期任务，以 40 个观测步的半衰期估计协方差，进行 10% 对角收缩，再采样联合高斯增量路径。 |
| 自回归树模型与残差块采样 | 对范围外的任务，或第一条路径无法执行的情况，在当前任务历史上拟合 XGBoost，并通过对齐的残差块生成预测样本。 |
| 官方统计回退模型 | 树模型执行失败时使用随包提供的官方统计预测器；无效输入仍可能失败。 |

每次成功预测输出 **500 个联合样本**，覆盖所请求的资产和预测期限。仅使用当前任务提供的历史，使用 CPU，无需预训练权重或外部模型服务。文本参数为比赛接口所需，但最终方法不使用文本内容。

**这些组件属于同一个最终方法，不是需要用户选择的几套实验。** 方法文档解释了原始代码标签、适用范围和具体公式。

## 使用

已验证的源码环境为 Linux/x86_64、Python 3.12.15 和固定版本依赖：

```bash
sh scripts/install.sh
# 如需指定解释器：PYTHON=/path/to/python3.12 sh scripts/install.sh
```

按[公开样例流程](docs/PUBLIC_EXAMPLE.md)获取官方输入并运行。文档只有一套执行流程；两个可选输入分别用于检查同一程序的不同路径，不需要修改模型参数。

使用准备好的输入目录时，统一的预测命令为：

```bash
T2_PYTHON="$PWD/.venv/bin/python" ./runtime/forecast \
  --panels "$INPUT/panels/" --text "$INPUT/text/" \
  --asof "$ASOF" --out "$OUTPUT/forecast.parquet"
```

输出为 `forecast.parquet`、`forecast_meta.json` 和 `forecast_rationale.md`。实际执行路径记录在 rationale 和标准输出中。

## 结果与复现

新建 Python 环境中的联合路径样例和树模型样例均通过官方输出检查。这证明了对应案例的运行与格式兼容，不是新增预测性能评估。公开 Docker 配方尚未完成构建验证：此前构建因无法连接 Docker daemon 而未开始。

- [完整方法与代码标签对应关系](docs/METHOD.md)
- [官方结果及验证范围](docs/EVALUATION.md)
- [环境与 Docker 复现说明](docs/REPRODUCIBILITY.md)
- [数据与依赖来源](docs/DATA_AND_DEPENDENCIES.md)
- [提交版本及原镜像身份](docs/FINAL_VERSION.md)

## 目录

`runtime/` 保存未修改的参赛实现；`configs/` 保存依赖与参数说明；`scripts/` 和 `docker/` 提供安装、检查与构建入口；`docs/` 介绍最终方法；`evidence/` 保存公开核验摘要；`provenance/` 集中保存文件哈希和历史追溯材料。

对外名称统一为 PrefixCast。原始运行标识及代码中的历史标签保留，用于与提交版本对应。历史实验记录不作为额外方法或运行选项。

自有代码及发布辅助程序采用 [MIT](LICENSE)。第三方代码保留其原许可证，其中官方共享 toolkit 为 CC-BY-NC-4.0；详见[第三方声明](THIRD_PARTY_NOTICES.md)。
