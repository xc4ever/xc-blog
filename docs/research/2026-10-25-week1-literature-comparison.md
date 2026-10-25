# 第一周推进：相近论文对照与场景修正

日期：2026-10-25。接续第一天案例笔记。本轮完成论文模型核读及场景草案，不代表完成整周任务或证明研究空白。

继续推进的更新：P5现已取得可读大学公开全文并核读车辆/能源约束，确认固定行驶耗电、返回场站时段充电、禁止场站向电网回送，以及MPC能源管理。又发现TTE 2025的Bertucci等论文已包含载重能耗、装卸、接入、容量与随机仿真，因此下文“载重与接入窗口”的方向降为基础建模要求。最新问题见[场景草案v0.2](2026-10-25-scenario-brief-v02.md)，车型依据见[参数登记](2026-10-25-vehicle-parameters-and-screening.md)。下文阅读状态保留对应轮次记录。

## 1. 阅读范围与访问状态

| 编号 | 文献 | 本轮实际读取程度 |
| --- | --- | --- |
| P1 | Fan等，Energy 341，139296，2025，物流园区重卡与PV/ESS联合调度 | 出版方公开预览：摘要、引言、贡献和章节片段；没有获得全文 |
| P2 | Lou等，IEEE TITS，2026，Graph-Benders路径、装载与V2G | 下载14页公开接收稿，核读系统建模、约束、算法和算例；渲染检查第8页车型及参数；没有复算结果或逐项证明算法 |
| P3 | Yao等，2025，电气化物流与电力系统均衡 | 核读作者预印本HTML的模型、算法及算例；未审计附录证明 |
| P5 | Saklaoui等，IEEE Access，2024，容量受限能源枢纽 | 读取出版方搜索返回摘要及大学仓储书目信息；本轮未获得可直接读取的全文 |
| P6 | Shukla等，CDC 2023接收稿，重型车辆电气化与电压约束 | 核读作者HTML的模型、算例和结论；未复现或审计近似精度 |
| R1 | Öko-Institut，ELV-LIVE第二份报告，2025 | 读取机构发布页及报告能耗、运营和充电相关章节；未下载原始车辆数据 |

原第一日P4灾后商业车辆论文尚未取得全文；本轮不据此填充模型细节。

## 2. 各篇论文告诉我们什么

### P1：基础场景已有非常接近的工作

题名：*Coordinated optimization of logistics scheduling for electric logistics vehicles and energy management in integrated logistics parks with PV and ESS*。

[出版方预览](https://www.sciencedirect.com/science/article/pii/S0360544225049382)，DOI：10.1016/j.energy.2025.139296。

公开预览确认：重卡从一级物流园向下级节点配送，结合时间窗、部分充电、PV、固定储能及园区其他负荷，采用ALNS-MILP联合求解；明确包含固定储能退化。

**判断**：园区、重卡、光储充、物流能源联合优化已被覆盖。不能把更换园区名称当作贡献。车辆V2G、车载电池退化和电网拓扑等细节尚需全文核对；预览没提到不等于原文没有。

### P2：要纠正“这是一篇重卡算例论文”的理解

题名：*A graph-benders decomposition for integrated electric trucks routing, cargo loading and V2G scheduling*。

[大学仓储与接收稿入口](https://eprints.gla.ac.uk/389854/)，DOI：10.1109/TITS.2026.3707595。[本地个人阅读副本](sources/lou-2026-graph-benders.pdf)，不放入公开博客。

接收稿第3—5页联合安排路径、分担货量、到达时间和充放电；第8页明确主算例采用中型卡车、固定每公里耗电。电力交互由节点价格和功率参数表示，主体模型未见配电网电压、潮流和线路约束。

**判断**：可借鉴离散车辆任务与能量连续性，不照搬车型或固定耗电参数；SOC区间限制也不等于显式退化成本。其图预处理限制反向行驶与循环，重复短驳场景需另建可往返的任务表示。

### P3：大车队均衡不等于10辆车可执行排班

题名：*Integrated equilibrium model for electrified logistics and power systems*。

[作者HTML全文](https://arxiv.org/html/2505.04532v1)。2025年预印本。

模型以位置、离散SOC等状态表示车辆，采用PU-MDP与DC-OPF求物流—节点电价均衡，算例为1000辆车，并使用大车队连续流近似。末期设置带高惩罚的“回库/补满”抽象动作。

**判断**：可借鉴运营主体和节点映射；10辆车应逐辆检查可执行性，不能把连续流或惩罚动作直接解释为真实回库。MDP、Bellman求解并不自动等于学习环境动态的Model-based RL。DC-OPF也不能验证电压幅值。

### P5：接网容量不足与滚动修正也已有研究

题名：*Coordinated Optimization of Logistics Electric Fleet and Energy Management System of Constrained Energy Hub*。

[IEEE出版方](https://ieeexplore.ieee.org/document/10713382/)，DOI：10.1109/ACCESS.2024.3477915；[大学公开副本入口](https://research.tue.nl/files/343535212/Coordinated_Optimization_of_Logistics_Electric_Fleet_and_Energy_Management_System_of_Constrained_Energy_Hub.pdf)。

摘要确认：容量受限能源枢纽中的物流车辆调度，采用MPC与路径算法，考虑负荷和可再生出力不确定性，比较多种充电策略。

**判断**：不能把“容量受限+滚动优化”当作空白。它应成为重要基准阅读对象；实际车型、V2G和电网内部模型仍需核读全文。

### P6：电压进入车辆调度框架已有先例

题名：*Voltage Constrained Heavy Duty Vehicle Electrification: Formulation and Case Study*。

[作者HTML全文](https://arxiv.org/html/2311.14861v1)，作者为Apurv Shukla、Rayan El Helou、Le Xie，预印本注明CDC 2023接收。

该文建立时间—能量扩展交通网络，联合电网运行与车辆路径；电力侧线性化AC模型并惩罚电压偏差，算例为IEEE 24节点输电网络和大规模重型车辆。

**判断**：电压约束本身不是新贡献；园区逐辆物流任务与局部配电网仍是不同研究边界，但需要更广检索确认。文中稳态电压优化不能等同于暂态、电压控制器动态或保护动作研究。

### R1：实际车辆接入窗口有直接工程证据

题名：*Real-world data analysis of energy consumption, activity and charging patterns of battery electric trucks operating in Germany*。

[机构发布页](https://www.oeko.de/publikation/real-world-data-analysis-of-energy-consumption-activity-and-charging-patterns-of-battery-electric-trucks-operating-in-germany/)，[报告](https://www.oeko.de/fileadmin/oekodoc/Real-world-data-analysis-of-battery-electric-trucks.pdf)，2025-07-21。

报告基于19辆车、5家伙伴；能耗章节讨论车重、速度、温度与高差。运营章节说明：有的场站装卸时可充电，有的必须移至集中充电位；单班和双班运行的补能条件不同。

**判断**：接入窗口不能由“停车”直接推出。研究应检查装卸、位置、接口与移车时间。报告可支持建模结构，但境外区域配送数据不能直接标定国内特定重卡；公开报告也不等于开放原始数据。

## 3. 当前覆盖关系

“确认”只表示本轮可读内容明确包含；“待核对”不等于没有。

| 内容 | P1 | P2 | P3 | P5 | P6 |
| --- | --- | --- | --- | --- | --- |
| 路径与充电协同 | 确认 | 确认 | 确认 | 确认 | 确认 |
| 车辆反向放电 | 待核对 | 确认 | 所读动作未含 | 待核对 | 扩展网络定义含放电弧，电网耦合细节需谨慎核查 |
| 货量/载重约束 | 预览提及容量需求，细节待核对 | 确认 | 主要以配送次数抽象 | 待核对 | 所读模型以出行要求为主 |
| 载重影响行驶耗电 | 待核对 | 主算例固定耗电 | 简化能量单位 | 待核对 | 本轮未确认 |
| 场站接网容量与预测误差 | 待核对 | 不能由节点功率替代 | 网络线路约束；非学习式预测模型 | 摘要确认 | 网络模型；非目标园区实参 |
| 电压幅值 | 待核对 | 主体模型未见 | DC模型不含 | 待核对 | 确认，稳态近似 |
| 生产与扩建任务共用车队 | 未确认 | 未确认 | 未确认 | 未确认 | 未确认 |
| Model-based RL | 所读方法不是 | 所读方法不是 | 所读方法不是 | MPC不自动等同MBRL | 所读方法不是 |

最后两行的“未确认”只构成继续调查的入口，不能据此宣布研究空白。

## 4. 对选题的具体修正

暂定问题从“工业园区10辆重卡参与电网”收窄为：

> 在承担多趟短驳任务的工业园区中，如何根据车辆位置、载重耗电和可接入时间，安排10辆重卡的任务与补能，并判断其可提供的电力服务是否可信？

这是工作问题，不是最终论文题目。最先检查的机制是：把所有停车时间当成可接入时间、把行驶耗电当成常数，是否会错误估计下一任务可行性和对外服务能力。

需要区分三种结果：

1. 简化模型与更真实模型差异很小：该机制可能不值得作为核心。
2. 差异明显，但传统优化足够解决：可继续研究场景和模型，尚无理由强加RL。
3. 差异来自持续变化且难以标定的动态，现有滚动优化受到明确影响：再比较模型学习与Model-based RL。

同时保留生产与扩建并存的方向。只有查证任务兼容和资源共享，才能把建设物资任务加入同一车队；若只是货量增加，就应与一般需求增长场景比较，检验“扩建”是否改变机制。

## 5. 本轮形成的决定与未决事项

- 已确认：基础联合优化、V2G、电压、容量约束和MPC均有前人工作，需要精确定位问题。
- 已纠正：P2主算例不是重卡；P3不适合作为10辆逐车调度的直接模板。
- 已形成：以任务决定可接入窗口为核心的候选场景，另见场景草案。
- 仍缺：P1/P5全文，国内重卡车型与任务数据，同车队承担生产及建设运输的证据。
- 尚未完成：仿真、数据标定、基准算法比较、创新性确认。
