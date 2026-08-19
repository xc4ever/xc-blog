// Project data configuration file
// Used to manage data for the project display page

export interface Project {
	id: string;
	title: string;
	description: string;
	image: string;
	category: "web" | "mobile" | "desktop" | "other";
	techStack: string[];
	status: "completed" | "in-progress" | "planned";
	liveDemo?: string;
	sourceCode?: string;
	visitUrl?: string;
	startDate: string;
	endDate?: string;
	featured?: boolean;
	tags?: string[];
	showImage?: boolean;
}

export const projectsData: Project[] = [
	{
		id: "divf-smart-park",
		title: "智慧园区能量管理与负荷调度平台",
		description:
			"团队项目。面向“源网荷储”协同运行的智慧园区场景，构建基于双输入 LSTM/GRU 与 DIVF 动态融合算法的负荷预测方案，并结合 Flask 与 CloudPSS 搭建能源管理平台，实现负荷预测、运行监测、风险预警、成本分析与储能调度等功能。本人主要负责负荷预测算法设计、数据治理、多粒度 LSTM/GRU 模型、DIVF 动态融合策略及实验分析。",
		image: "",
		category: "web",
		techStack: [
			"Python",
			"LSTM",
			"GRU",
			"DIVF",
			"Flask",
			"CloudPSS",
			"SHAP",
		],
		status: "completed",
		startDate: "2026-04-01",
		endDate: "2026-08-01",
		featured: true,
		tags: [
			"团队项目",
			"电力系统",
			"新能源",
			"人工智能",
			"负荷预测",
			"能源管理",
			"省级三等奖",
		],
		showImage: false,
	},
];

// Get project statistics
export const getProjectStats = () => {
	const total = projectsData.length;
	const completed = projectsData.filter((p) => p.status === "completed").length;
	const inProgress = projectsData.filter(
		(p) => p.status === "in-progress",
	).length;
	const planned = projectsData.filter((p) => p.status === "planned").length;

	return {
		total,
		byStatus: {
			completed,
			inProgress,
			planned,
		},
	};
};

// Get projects by category
export const getProjectsByCategory = (category?: string) => {
	if (!category || category === "all") {
		return projectsData;
	}
	return projectsData.filter((p) => p.category === category);
};

// Get featured projects
export const getFeaturedProjects = () => {
	return projectsData.filter((p) => p.featured);
};

// Get all tech stacks
export const getAllTechStack = () => {
	const techSet = new Set<string>();
	projectsData.forEach((project) => {
		project.techStack.forEach((tech) => {
			techSet.add(tech);
		});
	});
	return Array.from(techSet).sort();
};