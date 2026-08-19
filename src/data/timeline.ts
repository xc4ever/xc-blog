import type { TimelineItem } from "../components/features/timeline/types";

export const timelineData: TimelineItem[] = [
	{
		id: "xjtu-2023",
		title: "进入西安交通大学少年班",
		description:
			"进入西安交通大学少年班学习，开始系统接触大学阶段的数学、物理、计算机与工程基础课程。",
		type: "education",
		startDate: "2023-09-01",
		location: "西安",
		organization: "西安交通大学",
		skills: ["数学", "物理", "计算机基础", "工程基础"],
		achievements: [
			"进入西安交通大学少年班",
			"开始大学阶段的专业学习与工程实践",
		],
		icon: "material-symbols:school",
		color: "#2563EB",
		featured: true,
	},

	{
		id: "robomaster",
		title: "参与 RoboMaster 训练",
		description:
			"大学阶段参与 RoboMaster 相关训练，在团队协作与工程实践中接触机器人系统、嵌入式开发与工程项目流程。",
		type: "project",
		startDate: "2024-01-01",
		endDate: "2024-12-31",
		location: "西安",
		organization: "西安交通大学",
		skills: ["机器人", "工程实践", "团队协作", "编程"],
		achievements: [
			"参与 RoboMaster 学校训练",
			"积累工程实践与团队协作经验",
		],
		icon: "material-symbols:smart-toy",
		color: "#7C3AED",
	},

	{
		id: "electrical-engineering",
		title: "进入电气工程专业学习",
		description:
			"进入电气工程相关专业学习，逐渐将兴趣与实践方向聚焦到电力系统、能源系统以及人工智能在电气工程中的应用。",
		type: "education",
		startDate: "2025-09-01",
		location: "西安",
		organization: "西安交通大学",
		skills: ["电气工程", "电力系统", "新能源", "能源系统"],
		achievements: [
			"开始系统学习电气工程专业课程",
			"逐渐明确电力能源方向的学习兴趣",
		],
		icon: "material-symbols:bolt",
		color: "#F59E0B",
		featured: true,
	},

	{
		id: "mcm-award",
		title: "美国大学生数学建模竞赛 M 奖",
		description:
			"参加美国大学生数学建模竞赛，在团队协作中完成数学建模、数据分析与问题求解。",
		type: "achievement",
		startDate: "2025-01-01",
		location: "西安",
		skills: ["数学建模", "数据分析", "Python", "团队协作"],
		achievements: [
			"获得美国大学生数学建模竞赛 M 奖",
			"积累数学建模与数据分析实践经验",
		],
		icon: "material-symbols:emoji-events",
		color: "#7C3AED",
		featured: true,
	},

	{
		id: "electrical-electronic-competition",
		title: "高校电气电子大赛省级三等奖",
		description:
			"参加高校电气电子相关竞赛，将电路、电气工程与实际工程问题结合，在团队项目中完成系统设计与实验验证。",
		type: "achievement",
		startDate: "2025-01-01",
		location: "西安",
		organization: "高校电气电子大赛",
		skills: ["电路", "电子技术", "电气工程", "工程实践"],
		achievements: [
			"获得省级三等奖",
			"完成电气电子类工程实践与实验验证",
		],
		icon: "material-symbols:emoji-events",
		color: "#EA580C",
		featured: true,
	},

	{
		id: "divf-smart-park",
		title: "智慧园区能量管理与负荷调度平台",
		description:
			"参与面向“源网荷储”协同运行的智慧园区能源管理项目，负责负荷预测算法设计、数据治理、多粒度 LSTM/GRU 模型、DIVF 动态融合策略及实验分析。",
		type: "project",
		startDate: "2026-04-01",
		endDate: "2026-08-01",
		location: "西安",
		organization: "团队项目",
		skills: [
			"Python",
			"LSTM",
			"GRU",
			"DIVF",
			"Flask",
			"CloudPSS",
			"SHAP",
			"负荷预测",
		],
		achievements: [
			"完成智慧园区能源管理与负荷调度平台",
			"负责 DIVF 动态融合负荷预测算法设计",
			"完成数据治理、模型训练与实验分析",
			"项目获得省级三等奖",
		],
		icon: "material-symbols:bolt",
		color: "#059669",
		featured: true,
	},


];