// Skill data configuration file
// Used to manage data for the skill display page

export interface Skill {
	id: string;
	name: string;
	description: string;
	icon: string; // Iconify icon name
	category: "frontend" | "backend" | "database" | "tools" | "other";
	level: "beginner" | "intermediate" | "advanced" | "expert";
	experience: {
		years: number;
		months: number;
	};
	projects?: string[]; // Related project IDs
	certifications?: string[];
	color?: string; // Skill card theme color
}

export const skillsData: Skill[] = [
	// Programming & Data Analysis
	{
		id: "python",
		name: "Python",
		description:
			"主要用于数据处理、机器学习、负荷预测、实验分析以及项目开发。",
		icon: "logos:python",
		category: "backend",
		level: "intermediate",
		experience: { years: 1, months: 0 },
		projects: ["divf-smart-park"],
		color: "#3776AB",
	},
	{
		id: "matlab",
		name: "MATLAB",
		description:
			"用于数值计算、数学建模、电气工程计算、实验数据处理与可视化。",
		icon: "logos:matlab",
		category: "other",
		level: "intermediate",
		experience: { years: 1, months: 0 },
		color: "#0076A8",
	},
	{
		id: "cpp",
		name: "C/C++",
		description:
			"具备 C/C++ 基础编程能力，主要用于程序设计、算法实现以及工程类实践。",
		icon: "logos:c-plusplus",
		category: "backend",
		level: "beginner",
		experience: { years: 0, months: 8 },
		color: "#00599C",
	},

	// AI & Machine Learning
	{
		id: "machine-learning",
		name: "Machine Learning",
		description:
			"具备机器学习基础，能够将机器学习方法应用于负荷预测和能源数据分析等任务。",
		icon: "mdi:brain",
		category: "other",
		level: "intermediate",
		experience: { years: 0, months: 8 },
		projects: ["divf-smart-park"],
		color: "#7C3AED",
	},
	{
		id: "lstm",
		name: "LSTM",
		description:
			"用于时间序列建模与负荷预测，能够处理具有长期依赖关系的时序数据。",
		icon: "mdi:chart-timeline-variant",
		category: "other",
		level: "intermediate",
		experience: { years: 0, months: 6 },
		projects: ["divf-smart-park"],
		color: "#2563EB",
	},
	{
		id: "gru",
		name: "GRU",
		description:
			"用于时间序列预测与短期波动建模，并参与智慧园区负荷预测模型设计。",
		icon: "mdi:chart-line",
		category: "other",
		level: "intermediate",
		experience: { years: 0, months: 6 },
		projects: ["divf-smart-park"],
		color: "#0891B2",
	},
	{
		id: "divf",
		name: "DIVF",
		description:
			"动态逆方差融合方法，用于融合不同预测模型的结果，提高负荷预测性能与稳定性。",
		icon: "mdi:source-branch",
		category: "other",
		level: "intermediate",
		experience: { years: 0, months: 5 },
		projects: ["divf-smart-park"],
		color: "#9333EA",
	},
	{
		id: "shap",
		name: "SHAP",
		description:
			"用于机器学习模型的可解释性分析，帮助分析不同特征对预测结果的影响。",
		icon: "mdi:chart-bell-curve-cumulative",
		category: "other",
		level: "beginner",
		experience: { years: 0, months: 4 },
		projects: ["divf-smart-park"],
		color: "#EA580C",
	},

	// Data Analysis
	{
		id: "pandas",
		name: "Pandas",
		description:
			"用于结构化数据处理、数据清洗、时间序列分析以及机器学习项目的数据预处理。",
		icon: "simple-icons:pandas",
		category: "other",
		level: "intermediate",
		experience: { years: 0, months: 10 },
		projects: ["divf-smart-park"],
		color: "#150458",
	},
	{
		id: "matplotlib",
		name: "Matplotlib",
		description:
			"用于实验数据可视化、预测结果分析以及工程数据绘图。",
		icon: "simple-icons:matplotlib",
		category: "other",
		level: "intermediate",
		experience: { years: 0, months: 10 },
		projects: ["divf-smart-park"],
		color: "#11557C",
	},

	// Engineering & Energy
	{
		id: "cloudpss",
		name: "CloudPSS",
		description:
			"用于能源系统建模与工业场景应用开发，参与智慧园区能源管理与负荷调度平台建设。",
		icon: "mdi:cloud-outline",
		category: "tools",
		level: "intermediate",
		experience: { years: 0, months: 6 },
		projects: ["divf-smart-park"],
		color: "#2563EB",
	},
	{
		id: "multisim",
		name: "Multisim",
		description:
			"用于电路仿真、电子电路实验以及工程电路分析。",
		icon: "mdi:chip",
		category: "tools",
		level: "intermediate",
		experience: { years: 0, months: 8 },
		color: "#F59E0B",
	},

	// Web Development
	{
		id: "javascript",
		name: "JavaScript",
		description:
			"具备 JavaScript 基础，主要用于网页交互和前端项目开发。",
		icon: "logos:javascript",
		category: "frontend",
		level: "beginner",
		experience: { years: 0, months: 6 },
		color: "#F7DF1E",
	},
	{
		id: "typescript",
		name: "TypeScript",
		description:
			"用于 Astro/Mizuki 博客项目开发，具备 TypeScript 基础使用能力。",
		icon: "logos:typescript-icon",
		category: "frontend",
		level: "beginner",
		experience: { years: 0, months: 5 },
		color: "#3178C6",
	},
	{
		id: "astro",
		name: "Astro",
		description:
			"用于个人博客的静态网站开发，目前使用 Astro 与 Mizuki 搭建个人博客。",
		icon: "logos:astro-icon",
		category: "frontend",
		level: "intermediate",
		experience: { years: 0, months: 3 },
		color: "#FF5D01",
	},
	{
		id: "flask",
		name: "Flask",
		description:
			"用于构建轻量级 Web 后端与项目服务，在智慧园区能源管理平台中负责部分后端功能。",
		icon: "simple-icons:flask",
		category: "backend",
		level: "beginner",
		experience: { years: 0, months: 5 },
		projects: ["divf-smart-park"],
		color: "#555555",
	},

	// Development Tools
	{
		id: "git",
		name: "Git",
		description:
			"用于项目版本管理、代码协作以及 GitHub 项目维护。",
		icon: "logos:git-icon",
		category: "tools",
		level: "intermediate",
		experience: { years: 1, months: 0 },
		color: "#F05032",
	},
	{
		id: "github",
		name: "GitHub",
		description:
			"用于代码托管、项目管理以及个人开源项目展示。",
		icon: "logos:github-icon",
		category: "tools",
		level: "intermediate",
		experience: { years: 1, months: 0 },
		color: "#24292F",
	},
	{
		id: "vscode",
		name: "VS Code",
		description:
			"主要用于前端开发、脚本编写以及日常项目开发。",
		icon: "logos:visual-studio-code",
		category: "tools",
		level: "intermediate",
		experience: { years: 1, months: 0 },
		color: "#007ACC",
	},
	{
		id: "pycharm",
		name: "PyCharm",
		description:
			"主要用于 Python 编程、数据分析、机器学习以及相关项目开发。",
		icon: "logos:pycharm",
		category: "tools",
		level: "intermediate",
		experience: { years: 1, months: 0 },
		color: "#21D789",
	},
];