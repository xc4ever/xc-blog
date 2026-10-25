# 首个合成算例：固定运输任务下的连续供电能力

后续已加入固定储能与有限发车调整，入口为run_comparisons.py，结果见comparison_results.json及[对照报告](../../2026-10-25-storage-and-logistics-comparison.md)。以下原基准定义不变，新对照明确采用完全预知延误和相同的期末SOC要求。

在项目根目录运行新对照：

```powershell
python -c "import sys,runpy; sys.path[:0]=['D:/Projects/Mizuki/tmp/research-python','D:/Projects/Mizuki/docs/research/experiments/service-window']; runpy.run_path('docs/research/experiments/service-window/run_comparisons.py',run_name='__main__')"
```

这是机制检查，不是实际车队、园区配电网仿真、辅助服务市场产品或新算法。车辆双向设备能力是假设。正常、延误两种情况分别完全预知各自任务后优化，因此是确定性能力上限，不是在线决策效果。

## 运行

需要Python、NumPy和SciPy的milp求解器。本次采用Python 3.12、SciPy 1.18.1、NumPy 2.5.4，求解库放在项目临时目录，不更改全局环境。

在项目根目录运行：

```powershell
python -c "import sys,runpy; sys.path.insert(0,'D:/Projects/Mizuki/tmp/research-python'); runpy.run_path('docs/research/experiments/service-window/run_baseline.py',run_name='__main__')"
```

如果当前Python环境已经安装依赖，可直接运行本目录run_baseline.py。重新运行会更新本目录results.json和两份排程CSV。临时依赖目录不进Git。

## 具体设置

所有假设在config.json内。10辆车，每车423 kWh，SOC初始80%、期末至少80%、全程20%—90%。容量参考官方车型选项，但将其视为可用容量是额外假设。每车每天三次固定运输，每次1.5小时、54 kWh；另在整个16小时期间计2 kW辅助用电。排程起点为06:00，步长30分钟，车辆按五组错峰。

车辆仅返场后接入5个假设双向接口；充电上限200 kW/车、放电100 kW/车、充放电效率各95%，站点净进口余量600 kW、净输出限制500 kW。允许不同车辆同时充放电，禁止同车同时充放电，总占用接口不超过5个。

服务定义为14:00—16:00车队在场站连接点的**恒定净输出**，即总放电减总充电，不是相对基线的负荷削减，也不是备用容量。缺少电力网络拓扑，不能验证电压、线路、电能质量、孤岛或保护。

延误仅延长第二趟的离场时间，不增加行驶能量；辅助耗电始终已计入。没有临时新增运输任务，没有路线和车辆任务重分配，没有固定储能或光伏。该设计用于隔离位置可用性机制。

## 求解与检查

混合整数线性模型逐车跟踪每个时段的能量和充放电；接口占用、充放电互斥使用二元变量。首先最大化恒定输出，再在保留最大输出的容差内最小化总充放电量，避免任意循环。

数值检查：逐时能量守恒、SOC上下界及期末目标、不可用时充放电为零、单车充放电互斥、接口总数、场站净功率、服务输出约束及整数容差。求解器必须报告最优状态，达到时间限制不会被当成最优。

另核查不提供服务时的能量需求，和取消反向功能后的净输出为零。延误敏感性检查0、30、60、90分钟，记录每个服务时段可返场车辆数，以定位能力上限的原因。

脚本没有独立实现另一套仿真器；大部分检查基于约束残差，并额外独立检查整日逐车能量收支。还不能称为完整环境验证。

## 结果解释限制

若延误案例无法履行正常案例的承诺，只说明固定任务和现有设备假设下不存在可行解；不代表引入任务调整、固定储能、移动供电设施后仍不可行。500 kW受配置中的输出上限和接口数量约束，不能外推成10辆车的通用能力。

期末SOC一致避免消耗免费初始电量；但不计算退化、电费或收益。跨车辆任务调度、场站负荷、光伏和网络仍需进一步场景证据。固定储能比较见run_comparisons.py；在线机制见下节。

## 新增：只充电的在线顺序回放

`run_online.py`独立于旧的反向输出实验：每步根据已公布的返回延误和当前电量求解，只执行当前动作。输出`online_results.json`。目标使用合成的尽早补能权重，不是电价。包含配对事件公布前动作一致性、实际不可用时充电为零、SOC、接口及功率和整日能量检查。

在本目录依赖路径已加入Python搜索路径的情况下运行此脚本；本项目现有环境的完整命令：

```powershell
python -c "import sys,runpy; sys.path[:0]=['D:/Projects/Mizuki/tmp/research-python','D:/Projects/Mizuki/docs/research/experiments/service-window']; runpy.run_path('docs/research/experiments/service-window/run_online.py',run_name='__main__')"
```

新结果只验证事件因果性与合成充电可行性，未实现换电、任务改派、故障恢复或学习。详见上级目录`2026-10-25-online-replay-results.md`。

`run_request_scan.py`以同一环境运行（将上述命令中的脚本名替换），扫描3个窗口及4个进口上限，输出`request_scan_results.json`。另执行名义固定计划，真实不可接入时取消充电并记录期末缺口，不暗中修复；该对照不是强补救策略。扫描表与限制见`2026-10-25-request-scan-results.md`。

`run_simple_repair.py`在生成扫描结果后运行，输出`simple_repair_results.json`。初始名义优化后不再在线求解，只在可用接口与功率内偿还被取消的充电；检查实际约束、期末能量及事件公布前动作一致性。10组原可行条件均可由该规则完成，详见`2026-10-25-simple-repair-results.md`。
