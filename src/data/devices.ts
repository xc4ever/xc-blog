// 设备数据配置文件

export interface Device {
	name: string;
	image: string;
	specs: string;
	description: string;
	link: string;
}

// 设备类别类型，支持品牌和自定义类别
export type DeviceCategory = Record<string, Device[]> & {
	自定义?: Device[];
};

export const devicesData: DeviceCategory = {
	Apple: [
		{
			name: "iPhone 17 Pro Max",
			image: "",
			specs: "iPhone / Pro Max",
			description:
				"目前使用的手机，主要用于日常通讯、影音娱乐、移动办公与随身使用。",
			link: "https://www.apple.com.cn/iphone-17-pro/",
		},
	],

	Huawei: [
		{
			name: "HUAWEI FreeBuds Pro 3",
			image: "",
			specs: "FreeBuds Pro 3",
			description:
				"日常使用的无线耳机，主要用于音乐、视频与日常影音。",
			link: "https://consumer.huawei.com/cn/audio/freebuds-pro-3/",
		},
	],

	ASUS: [
		{
			name: "华硕天选 6 Pro 锐龙版",
			image: "",
			specs: "天选 6 Pro / AMD Ryzen",
			description:
				"目前使用的电脑，主要用于编程、课程学习、工程项目与日常工作。",
			link: "https://www.asus.com.cn/laptops/for-gaming/tuf-gaming/",
		},
	],
};