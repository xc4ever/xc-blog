
---
title: "我是如何用 Astro + Mizuki 搭建自己的博客的"
published: 2026-08-19
description: "记录我从选择 Astro 和 Mizuki，到完成博客中文化、配置、内容整理、Git 管理以及最终构建的整个过程。"
tags: [Astro, Mizuki, Blog, Git, Web]
category: 建站
draft: false
---

# 我是如何用 Astro + Mizuki 搭建自己的博客的

一直想拥有一个真正属于自己的个人博客。

相比直接使用现成的博客平台，自己搭建网站虽然麻烦一些，但也意味着可以真正控制网站的样式、内容和代码。

更重要的是，搭建博客本身就是一个学习 Web 开发的过程。

所以最后我选择了：

```text
Astro
+
Mizuki
+
Git
````

从一个现成的 Astro 博客主题开始，一点一点把它改成现在的 **XC's Blog**。

这篇文章记录的不是 Astro 官方教程，而是我自己实际搭建这个博客时做过的事情，以及过程中遇到的一些问题。

---

## 一、为什么想做一个自己的博客

以前接触到的很多东西，总是分散在不同的地方。

学习笔记可能放在本地，项目代码放在 GitHub，生活中的一些记录又可能在其他平台。

所以我一直觉得，如果能有一个真正属于自己的地方，把这些东西慢慢记录下来，应该是一件挺有意思的事情。

这个博客也不一定需要每天更新。

它更像是一个长期维护的个人空间。

以后我可能会在这里记录：

* 电气工程
* 电力系统
* 新能源
* 编程
* AI
* 项目开发
* 音乐
* 音游
* Galgame
* 数码设备
* 学习过程
* 以及一些生活中的事情

所以我希望它最终不只是一个“博客模板”，而是一个会随着我不断学习而一起变化的小项目。

---

## 二、为什么选择 Astro

在开始之前，我考虑过一些比较常见的博客方案，例如 WordPress、Hexo 和 Astro。

最后选择了 Astro。

### 1. Markdown 很适合写博客

博客最重要的东西其实就是文章。

而 Astro 对 Markdown 和 MDX 的支持非常适合这种场景。

一篇文章本质上就是一个 Markdown 文件，例如：

```text
src/content/posts/my-blog/build-this-blog.md
```

文章标题、发布时间、分类、标签等信息都可以写在 Frontmatter 中：

```yaml
---
title: "文章标题"
published: 2026-08-19
description: "文章简介"
tags: [Astro, Blog]
category: 建站
---
```

写文章的时候不需要维护一个复杂的后台系统。

直接编辑 Markdown，然后构建网站即可。

### 2. 静态网站非常适合个人博客

个人博客通常并不需要一个非常复杂的后端。

文章发布以后，大部分内容都是相对固定的。

Astro 可以在构建阶段生成网页，因此部署之后不需要一直运行一个复杂的服务器。

对于个人博客来说，这种方式非常合适。

### 3. 可以深入代码

我比较喜欢 Astro 的另一个原因，是它不会把所有东西都封装起来。

如果以后想修改某个页面，可以继续往下研究：

```text
components
pages
layouts
config
content
utils
```

这些代码最终都会暴露在项目中。

所以这个博客对我来说并不只是一个网站。

它本身也是一个 Web 开发学习项目。

---

## 三、为什么选择 Mizuki

决定使用 Astro 之后，我没有选择从零开始设计整个博客。

如果所有东西都自己实现，需要花大量时间处理：

* 首页
* 文章列表
* 分类
* 标签
* 归档
* 侧边栏
* TOC
* 评论
* 音乐播放器
* Markdown
* 搜索
* 响应式布局
* 各种页面

所以最后选择了一个已经比较完整的 Astro 博客主题：

**Mizuki**。

Mizuki 已经提供了大量个人博客常用功能。

例如：

```text
首页
文章系统
分类
标签
归档
侧边栏
个人资料
友情链接
音乐播放器
About
Markdown 扩展
代码高亮
数学公式
搜索
```

这样就不用从零开始实现整个网站。

但使用现成主题也有一个问题：

如果只知道：

```powershell
pnpm dev
```

而不知道主题内部是怎么工作的，那么以后想修改东西还是会比较麻烦。

因此拿到 Mizuki 之后，我没有马上开始疯狂改页面，而是先把它的项目结构和配置体系摸了一遍。

---

## 四、准备开发环境

我的开发环境是 Windows。

目前主要使用：

```text
Windows
Node.js
pnpm
Git
VS Code
PowerShell
```

项目放在：

```text
D:\Projects\Mizuki
```

进入项目目录：

```powershell
cd D:\Projects\Mizuki
```

然后安装依赖：

```powershell
pnpm install
```

启动开发服务器：

```powershell
pnpm dev
```

之后就可以在浏览器中访问本地开发地址。

到这里，一个能够正常运行的 Mizuki 博客就已经出现了。

但这还只是主题作者的博客。

真正有意思的部分，是接下来开始把它改成自己的。

---

## 五、先认识 Mizuki 的项目结构

刚开始拿到项目的时候，我首先检查了 `src` 目录。

其中比较重要的部分包括：

```text
src/
├── components/
├── config/
├── content/
├── i18n/
├── layouts/
├── pages/
├── styles/
└── utils/
```

对于博客来说，最重要的几个地方是：

```text
src/config/
src/content/
src/pages/
src/components/
```

其中：

```text
src/config/
```

主要负责网站配置。

而：

```text
src/content/
```

负责文章等内容。

至于：

```text
src/pages/
src/components/
```

则更多负责页面和组件本身。

把这几个部分搞清楚以后，后面修改网站就容易很多了。

---

## 六、把网站改成自己的

整个博客最先需要修改的就是：

```text
src/config/siteConfig.ts
```

这是 Mizuki 最重要的配置文件之一。

这里可以设置：

* 网站标题
* 网站副标题
* 网站地址
* 网站语言
* 网站开始日期
* 时区
* 主题色
* Banner
* TOC
* 字体
* 图片优化
* 页面开关
* 其他全局配置

---

## 七、中文化

首先修改网站语言。

最终使用：

```ts
const SITE_LANG = "zh_CN";
```

Mizuki 本身已经提供中文语言文件，因此并不需要自己重新翻译所有界面。

这样网站的大部分系统文字就可以直接使用中文。

这是我第一次真正感受到：

> 一个主题真正好不好用，不只是看页面漂不漂亮，还要看它的配置体系是否完整。

---

## 八、网站名称和域名

网站名称最终改成：

```text
XC's Blog
```

现在网站使用的地址也已经改成：

```text
https://xc4ever.cn/
```

也就是说，现在 `siteConfig.ts` 中已经不是主题作者的示例网址，而是我自己的站点地址。

这一点和刚开始搭建时最大的区别之一，就是博客已经开始真正脱离 Mizuki 的默认模板。

---

## 九、Banner、主题和页面风格

Mizuki 的 Banner 支持桌面端和移动端分别配置。

目前使用本地图片：

```text
/assets/desktop-banner/
```

以及：

```text
/assets/mobile-banner/
```

同时还保留了 Banner 轮播和波浪效果。

首页文字则通过：

```text
homeText
```

控制。

目前使用的是偏日系的文案，例如：

```text
わたしの部屋
```

以及一些日文句子。

我希望这个博客整体不要太像传统意义上的“技术博客”。

它更像一个个人空间：

```text
技术
+
学习
+
兴趣
+
生活
```

所以最终视觉风格也会偏向我自己喜欢的方向。

---

## 十、侧边栏和站点统计

Mizuki 的侧边栏并不是一个巨大的页面文件，而是由多个 Widget 组合起来的。

例如：

```text
Profile
Announcement
Tags
TOC
Site Stats
Calendar
Categories
Music
```

这些组件由配置决定显示在哪里、以什么顺序显示。

在实际修改过程中，我还遇到了一个比较有意思的问题：

**站点统计中的总字数。**

---

## 十一、解决站点总字数统计问题

一开始我尝试直接使用：

```ts
post.data.words
```

于是代码类似：

```ts
const totalWords = posts.reduce(
    (total, post) => total + (post.data.words ?? 0),
    0,
);
```

但是后来检查整个项目之后发现：

```text
post.data.words
```

并不是文章 Collection schema 中定义的字段。

真正的文章字数来自 Markdown 渲染阶段产生的：

```ts
remarkPluginFrontmatter.words
```

例如文章页面本身就是通过：

```ts
const { Content, headings, remarkPluginFrontmatter } =
    await renderPostContent(...)
```

然后使用：

```ts
remarkPluginFrontmatter.words
```

显示文章字数。

因此，直接从：

```text
post.data.words
```

读取并不是一个可靠的方法。

---

## 十二、最后采用的字数统计方式

为了让首页的“总字数”和文章页面的中文统计逻辑尽量保持一致，我最后没有继续强行往 Collection data 里塞一个 `words` 字段。

而是在站点统计组件中直接读取文章正文：

```ts
post.body
```

然后进行统计。

首先移除代码块：

````ts
text = text.replace(/```[\s\S]*?```/g, "");
````

再移除行内代码：

```ts
text = text.replace(/`[^`]+`/g, "");
```

之后使用 CJK 字符正则统计中文、日文、韩文等字符：

```ts
const cjkPattern =
    /[\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af\u3000-\u303f\uff00-\uffef]/g;
```

非 CJK 内容则按照空白进行分词。

这样最终得到的总字数更加符合博客实际显示的统计方式。

这次修改也让我更加清楚了 Astro Content 的数据流：

```text
Markdown
    ↓
Content Collection
    ↓
render()
    ↓
remarkPluginFrontmatter
    ↓
文章页面
```

而不是所有文章相关的数据都会自动出现在：

```ts
post.data
```

里面。

---

## 十三、检查 Content Schema

为了进一步确认文章的数据结构，我又检查了：

```text
src/content.config.ts
```

这里定义了：

```ts
const postsCollection = defineCollection(...)
```

文章 Frontmatter 中支持的字段包括：

```text
title
published
updated
draft
description
image
tags
category
lang
pinned
comment
priority
author
sourceLink
licenseName
licenseUrl
```

此外还存在页面加密相关字段：

```text
encrypted
password
passwordHint
hideHomeContent
```

以及：

```text
alias
permalink
```

等字段。

这也说明 Mizuki 的文章系统并不是简单地读取几个 Markdown 属性，而是通过 Astro Content Collection 对文章数据进行统一定义和校验。

---

## 十四、检查文章加载器

随后又继续检查了：

```text
src/loaders/post-loader.ts
```

这个文件负责对文章进行额外处理。

其中一个重要作用，是读取 Markdown 文件本身，然后检查：

```text
published
updated
```

是否是只有日期而没有具体时间的 Frontmatter。

最终生成：

```text
_publishedDateOnly
_updatedDateOnly
```

这样的内部字段。

也就是说，Mizuki 在文章加载阶段还做了一层自己的数据处理。

这也是为什么在修改主题时，最好不要只盯着页面组件。

有时候真正的数据来源其实在：

```text
loader
→ content collection
→ renderer
→ page
```

这一整条链路上。

---

## 十五、文章渲染流程

之后又检查了：

```text
src/utils/content-renderer.ts
```

这里使用：

```ts
render(post)
```

把文章内容渲染出来。

文章页面最终可以拿到：

```ts
Content
headings
remarkPluginFrontmatter
```

其中：

```text
Content
```

负责文章正文。

而：

```text
remarkPluginFrontmatter
```

则包含 Markdown 插件处理过程中生成的信息，例如：

```text
words
minutes
excerpt
```

因此文章页面显示的：

```text
字数
阅读时间
摘要
```

并不是简单从 Frontmatter 读取的。

---

## 十六、清理主题自带的示例内容

Mizuki 原本自带了不少示例文章。

例如：

```text
src/content/posts/
├── content-pipeline-fixture.mdx
├── draft.md
├── encrypted-post.md
├── image-grid-demo.md
├── markdown-extended.md
├── markdown-mermaid.md
├── markdown-tutorial.md
├── video.md
└── guide/
    ├── cover.webp
    └── index.md
```

这些文章主要是为了展示主题功能。

例如：

```text
Markdown
Mermaid
图片网格
视频
草稿
页面功能
```

所以并不是所有内容都应该直接删除。

有些示例其实很有参考价值。

---

## 十七、保留真正有用的 Markdown 示例

其中比较有价值的是：

```text
markdown-tutorial.md
```

它展示了大量 Markdown 功能：

* 标题
* 段落
* 引用
* 列表
* 代码块
* 表格
* 链接
* 图片
* 删除线
* 自动链接
* 转义
* HTML
* 语法高亮

所以我没有简单地把它删除，而是进行了中文化处理。

例如：

```markdown
## Block Elements
```

改成：

```markdown
## 块级元素
```

而示例代码本身仍然尽量保留。

这样它就不再只是主题作者留下的 Example，而变成了一个可以长期作为自己写 Markdown 文章时参考的文档。

---

## 十八、建立自己的文章目录

为了把主题自带内容和自己的文章区分开，我建立了：

```text
src/content/posts/my-blog/
```

例如这篇文章本身就可以放在：

```text
src/content/posts/my-blog/build-this-blog.md
```

这样以后目录会更加清晰：

```text
src/content/posts/
├── markdown-tutorial.md
├── guide/
└── my-blog/
    └── build-this-blog.md
```

以后自己的建站记录、开发记录等文章都可以放在这里。

---

## 十九、关于独立 Content Git 仓库

在检查 Mizuki 项目时，我还发现了：

```text
scripts/sync-content.js
```

这个脚本支持把博客内容独立到另外一个 Git 仓库。

理论上可以形成：

```text
Mizuki 项目 Git
        +
Content Git
```

这样代码和内容可以分别维护。

项目也会尝试寻找：

```text
content/
```

目录。

如果没有配置：

```text
CONTENT_REPO_URL
```

则继续使用本地：

```text
src/content/
```

---

## 二十、没有 Content 仓库并不是错误

开发过程中曾经看到过类似：

```text
内容目录不存在
未设置 CONTENT_REPO_URL
将使用本地内容
```

刚开始看到这种提示，确实容易以为项目出了问题。

后来检查了同步脚本以后才确认：

**这只是一个可选功能。**

目前博客完全可以直接使用：

```text
src/content/
```

因此现在：

```text
没有独立 Content 仓库
没有 CONTENT_REPO_URL
没有额外的 .env
```

都没有问题。

对于目前这种个人博客来说，一个 Git 仓库管理整个项目反而更加简单。

---

## 二十一、Git 管理整个博客

目前项目采用的是：

```text
一个 Git 仓库
        ↓
整个 Mizuki 项目
```

也就是说：

```text
代码
+
配置
+
文章
+
图片
```

一起进行版本管理。

而不是：

```text
Mizuki Git
+
Content Git
```

这种拆分方式。

目前没有必要把事情搞得太复杂。

以后如果博客内容越来越多，或者真的需要多人协作，再考虑独立 Content 仓库也不迟。

---

## 二十二、为什么我觉得 Git 很重要

这个博客从一开始就不是单纯“下载一个主题然后改文件”。

我希望把整个过程都作为一个完整的开发项目来做。

所以 Git 对我来说非常重要。

例如完成一部分功能以后，可以：

```powershell
git add .
git commit -m "update blog config"
```

如果之后某次修改把网站弄坏了，也可以通过 Git 找到之前的版本。

以后再接入 GitHub，就可以形成：

```text
本地开发
   ↓
Git commit
   ↓
GitHub
   ↓
自动构建
   ↓
网站部署
```

这样博客就真正拥有了一套比较完整的开发流程。

---

## 二十三、最后的构建测试

在完成这一轮修改之后，我最终运行了：

```powershell
pnpm build
```

这次构建完整通过。

最终结果包括：

```text
19 page(s) built
Build Complete!
```

Sitemap 也正常生成：

```text
sitemap-index.xml
```

之后 Pagefind 搜索索引也正常生成：

```text
Indexed 1 language
Indexed 4 pages
Indexed 1239 words
```

同时还通过了页面样式检查：

```text
Verified homepage styles
Verified about page styles
```

字体加载检查也正常：

```text
Font loading check passed
```

这意味着目前这套博客至少已经能够完整通过一次正式的生产构建。

---

## 二十四、现在的博客已经是什么状态？

从最开始的：

```text
一个刚下载下来的 Mizuki 模板
```

到现在：

```text
XC's Blog
```

中间其实改了不少东西。

目前已经完成的主要工作包括：

* Astro + Mizuki 本地环境搭建
* pnpm 依赖安装
* Git 项目管理
* 网站中文化
* 网站标题修改
* 独立域名配置
* Banner 配置
* 主题视觉配置
* Sidebar 检查与调整
* 音乐播放器配置
* Markdown 功能检查
* Content Collection 检查
* 文章 Loader 检查
* 文章渲染流程检查
* 站点统计字数计算修复
* 示例文章整理
* Markdown 教程中文化
* 自己的 `my-blog` 文章目录建立
* 独立 Content Git 机制研究
* 生产环境构建测试
* Sitemap 生成
* Pagefind 搜索索引生成

其中有些事情看起来很小，但实际上让我对这个项目的理解深入了很多。

---

## 二十五、这次搭博客最大的收获

其实到最后，我觉得这个项目最大的收获并不是“拥有了一个博客”。

而是第一次比较完整地走了一遍一个 Web 项目的流程：

```text
选择技术栈
    ↓
获取开源项目
    ↓
安装依赖
    ↓
本地运行
    ↓
阅读项目结构
    ↓
修改配置
    ↓
修改组件
    ↓
处理内容
    ↓
排查 Bug
    ↓
Git 版本管理
    ↓
生产构建
    ↓
准备部署
```

尤其是在处理站点字数统计的时候，我第一次比较完整地追踪了：

```text
Markdown
   ↓
Astro Content
   ↓
Loader
   ↓
render()
   ↓
remarkPluginFrontmatter
   ↓
页面组件
```

这比单纯修改几个 CSS 要有意思得多。

因为当真正理解数据是怎么流动的以后，以后再遇到类似问题，就不会只能靠“改一个试一下”。

---

## 二十六、接下来准备做什么

现在博客已经从：

```text
“能跑起来的 Mizuki 模板”
```

进入了：

```text
“真正属于 XC 的个人博客”
```

下一步不会再急着大规模修改主题。

接下来更重要的是开始产生真正属于自己的内容。

例如：

```text
学习笔记
电气工程
电力系统
AI
项目开发
编程
音乐
音游
Galgame
数码设备
```

同时继续完善：

* Profile
* Navbar
* Announcement
* Banner
* About
* Friends
* Projects
* Timeline
* 标签与分类
* GitHub
* 自动部署

以及把剩余的主题示例内容逐渐清理干净。

---

## 二十七、从模板到自己的博客

现在回头看，这个过程其实挺有意思。

一开始只是：

```text
下载 Mizuki
↓
pnpm install
↓
pnpm dev
```

然后慢慢开始：

```text
看配置
↓
看组件
↓
看 Content
↓
看 Loader
↓
看 Renderer
↓
修改代码
↓
解决问题
↓
Git 管理
↓
Build
```

最后它才逐渐变成：

```text
XC's Blog
```

我希望这个网站最终不会只是一个“套了 Mizuki 主题的个人网站”。

它可以是一个长期维护的个人空间。

以后无论是学习电气工程、研究电力系统、做 AI 项目，还是记录音乐、游戏、设备和生活，都可以慢慢放到这里。

而这个博客本身，也会成为我学习和折腾的一部分。

