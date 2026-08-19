---
title: "如何在 Mizuki 中撰写博客文章"
published: 2026-08-19
description: "这是一篇用于介绍 Mizuki 博客文章结构与 Frontmatter 写法的示例文章。"
image: "./cover.webp"
tags: ["Mizuki", "博客", "Markdown"]
category: 教程
draft: false
---

欢迎来到 **XC's Blog**！

这篇文章主要用于介绍 Mizuki 中博客文章的基本结构，以及常用的 Frontmatter 配置。

以后在 `src/content/posts/` 中创建 Markdown 或 MDX 文件，就可以用这种方式来撰写博客文章。

## Frontmatter

每篇文章开头都需要使用 Frontmatter 来描述文章的基本信息。

一个常见的写法如下：

```yaml
---
title: "一篇示例文章"
published: 2026-08-19
updated: 2026-08-19
description: "这是文章的简短介绍。"
image: "./cover.webp"
tags: ["示例", "教程"]
category: 教程
draft: false
---
```

### 常用字段

| 字段 | 说明 |
| --- | --- |
| `title` | 文章标题 |
| `published` | 文章发布日期 |
| `updated` | 文章最后修改日期 |
| `pinned` | 是否将文章置顶 |
| `priority` | 置顶文章的优先级，数字越小优先级越高 |
| `description` | 文章简介，会显示在文章列表等位置 |
| `image` | 文章封面图片 |
| `tags` | 文章标签 |
| `category` | 文章分类 |
| `licenseName` | 本篇文章使用的许可证 |
| `author` | 文章作者 |
| `sourceLink` | 文章内容的来源或参考链接 |
| `draft` | 是否为草稿，设置为 `true` 时不会正常显示 |

## 文章应该放在哪里？

博客文章应该放在：

```text
src/content/posts/
```

例如：

```text
src/content/posts/
├── example.md
└── guides/
    ├── cover.webp
    └── index.md
```

你也可以为一篇文章单独创建一个文件夹，并把文章封面等资源放在里面。

例如：

```text
src/content/posts/my-first-post/
├── cover.webp
└── index.md
```

这时在文章中使用：

```yaml
image: "./cover.webp"
```

就可以引用同一个文件夹中的 `cover.webp`。

## 图片的使用

Mizuki 支持多种图片路径写法。

### 使用文章目录中的图片

```yaml
image: "./cover.webp"
```

### 使用 `public` 目录中的图片

```yaml
image: "/images/cover.webp"
```

### 使用网络图片

```yaml
image: "https://example.com/cover.webp"
```

对于自己的博客，通常更推荐使用本地图片，这样以后迁移博客或更换部署平台时会更加方便。

## 草稿

如果文章还没有准备好发布，可以将：

```yaml
draft: true
```

设置为草稿状态。

完成文章后，再修改为：

```yaml
draft: false
```

这样就可以正式发布。

## 关于这篇文章

这篇文章本身只是一个简单的写作参考。

以后，这里会真正记录 XC 的学习、技术、生活以及各种折腾的过程。