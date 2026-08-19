export type AIToolCategory =
	| "chat"
	| "coding"
	| "image"
	| "audio"
	| "video"
	| "writing"
	| "search"
	| "other";

export type AIToolFrequency =
	| "daily"
	| "weekly"
	| "occasional"
	| "experimental";

export type LocaleString = Partial<
	Record<"en" | "zh_CN" | "zh_TW" | "ja", string>
>;

export function getLocaleString(value: LocaleString, lang: string): string {
	return value[lang as keyof LocaleString] ?? value["en"] ?? "";
}

export interface AITool {
	id: string;
	name: string;
	description: LocaleString;
	icon: string;
	category: AIToolCategory;
	frequency: AIToolFrequency;
	url?: string;
	usage?: LocaleString;
	tags?: string[];
	color?: string;
}

export const aiToolsData: AITool[] = [
	{
		id: "chatgpt",
		name: "ChatGPT",
		description: {
			en: "A general-purpose AI assistant for reasoning, writing, learning, research, and everyday problem solving.",
			zh_CN: "通用型 AI 助手，主要用于学习、推理、写作、资料整理、编程与日常问题解决。",
		},
		icon: "simple-icons:openai",
		category: "chat",
		frequency: "daily",
		usage: {
			en: "Daily: learning, reasoning, writing, research, programming",
			zh_CN: "每天：学习、推理、写作、资料整理、编程与项目开发",
		},
		tags: ["LLM", "Reasoning", "Research", "Coding"],
		color: "#10A37F",
	},

	{
		id: "claude",
		name: "Claude",
		description: {
			en: "An AI assistant focused on reasoning, long-context understanding, writing, and software development.",
			zh_CN: "注重推理、长上下文理解、写作与软件开发的 AI 助手。",
		},
		icon: "simple-icons:anthropic",
		category: "chat",
		frequency: "weekly",
		usage: {
			en: "Weekly: reasoning, writing, coding, long-context tasks",
			zh_CN: "每周：复杂推理、写作、编程与长上下文任务",
		},
		tags: ["LLM", "Reasoning", "Coding"],
		color: "#D97757",
	},

	{
		id: "gemini",
		name: "Gemini",
		description: {
			en: "Google's multimodal AI assistant for research, reasoning, writing, and working with different types of content.",
			zh_CN: "Google 的多模态 AI 助手，用于资料检索、推理、写作以及多类型内容处理。",
		},
		icon: "simple-icons:googlegemini",
		category: "chat",
		frequency: "weekly",
		usage: {
			en: "Weekly: research, multimodal tasks, comparison",
			zh_CN: "每周：资料检索、多模态任务与模型对比",
		},
		tags: ["LLM", "Multimodal", "Research"],
		color: "#4285F4",
	},

	{
		id: "deepseek",
		name: "DeepSeek",
		description: {
			en: "An AI assistant used for reasoning, mathematics, programming, and technical problem solving.",
			zh_CN: "用于推理、数学、编程以及技术问题分析的 AI 助手。",
		},
		icon: "simple-icons:deepseek",
		category: "chat",
		frequency: "weekly",
		usage: {
			en: "Weekly: mathematics, reasoning, programming",
			zh_CN: "每周：数学、逻辑推理、编程与技术问题",
		},
		tags: ["LLM", "Reasoning", "Coding", "Math"],
		color: "#4D6BFE",
	},

	{
		id: "github-copilot",
		name: "GitHub Copilot",
		description: {
			en: "An AI coding assistant integrated into development environments for code completion and software development.",
			zh_CN: "集成于开发环境中的 AI 编程助手，用于代码补全、理解与软件开发。",
		},
		icon: "simple-icons:githubcopilot",
		category: "coding",
		frequency: "occasional",
		usage: {
			en: "Occasionally: code completion and development assistance",
			zh_CN: "偶尔：代码补全与开发辅助",
		},
		tags: ["Coding", "IDE", "Developer Tool"],
		color: "#24292F",
	},
];