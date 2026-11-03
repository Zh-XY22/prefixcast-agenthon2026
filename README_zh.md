# PrefixCast

**Joint Financial Forecasting with EWMA Paths and Tree-Based Fallbacks**

队伍 **HaHaHa 获得 Agenthon 2026 Track 2 第二名**。2026-11-03 核对[官网 Final 榜单](https://www.agenthon.net/#leaderboard)，显示分数 **−0.9513**，越高越好。原参赛标识仍为 **QuantPrefixEW40V3**；`runtime/` 中算法、方法标识、参数、路由及输出语义均未修改。

用户已明确确认实际最终提交的整个 ZIP SHA256：`dedcc25dabb09e16304a4281e9feda5afa1e5a4b7cb5b7e391a75ef3737095ab`，与原归档一致。仍未发现归档的平台接收回执，submission ID 为 UNKNOWN。用户确认、官网队伍排名和单次提交回执是不同证据，不相互冒充。完整身份链见 [FINAL_VERSION](docs/FINAL_VERSION.md)。

## 最终程序

当前任务输入 → 适用范围检查 → EW40 联合路径；范围外或历史不足 → 原 CPU B4；B4 失败 → 官方 R0。EW40 只原生处理日频利率/G10外汇1–4步且满足历史条件的输入，不能把全部回退说成原生。500完整联合样本，默认seed1，可用 `QFBENCH_SEED`。无预装学习工件，不读文本，不调用House/外部模型；B4只在当前任务历史内拟合。

## 本轮真实复现检查

新建 Python3.12.15 隔离环境，固定22项依赖全部从 PyPI 直连安装，`pip check`通过，未改版本。仅运行两个官方公开历史样例，均以UID65534、CPU执行：

|公开样例|日期/期限|实际路由|结果|
|---|---|---|---|
|t2-F1-curve-ust1y-001-ps1|2019-01-07，2/3步|EW40原生|500draws，三文件，G0–G3 PASS|
|t2-F1-fx-krw-011-ps1|2017-03-27，1/4步|B4 CPU回退，实际拟合2次|500draws，三文件，G0–G3 PASS|

输入字节、日期和目标未改，未提供realized，未计算性能分数。**公开源码 Docker 构建已尝试，但当前容器无可连接daemon，退出1；没有新构建镜像，也没有新镜像内预测通过记录。** 新环境运行、历史原镜像验收与本轮Docker阻塞分别记录，见 [RELEASE_CHECKS](docs/RELEASE_CHECKS.md)。未重跑104题、未调参、未训练研究模型、未使用GPU、未发布上传。

完整安装、forecast、输出检查、Docker命令见英文 [README](README.md)。安装入口 `sh scripts/install.sh`；Python不在PATH时可用 `PYTHON=/path/to/python3.12 sh scripts/install.sh`。公开配方为 `docker/Dockerfile`；原配方 `docker/Dockerfile.submitted` 保持不变。依赖获取需联网，推理可断网。源码重建不承诺获得原镜像digest。

## 目录和发布边界

- `runtime/`：与原导出逐文件一致的最终实现及官方接口。
- `configs/`：原版本/依赖锁与实际参数说明，未修改算法配置。
- `docker/`、`scripts/`：公开重建与检查包装；不含账号操作。
- `docs/`：方法、身份、复现、评价、数据与许可。
- `evidence/`：公开身份及脱敏检查摘要，无原始私有日志或团队证明。

自有代码MIT；第三方保留原许可与署名，其中官方共享toolkit为CC-BY-NC4.0，整个仓库不能统一宣称MIT。公开包不含生产ZIP、claim/proof、数据、权重、环境、TAR或论文私有归档。GitHub上传本目录内文件，勿上传同级validation或原private-evidence。历史公开回测分数与官网Final结果分开展示，不能相互换算。
