
---
title: "我是如何用 Astro + Mizuki 搭建自己的博客的"
published: 2026-08-19
description: "记录我从选择 Astro 到使用 Mizuki 搭建个人博客的过程，以及中文化、主题配置、内容管理和后续部署规划。"
tags: [Astro, Mizuki, Blog, Git]
category: 建站
draft: false
---

# 我是如何用 Astro + Mizuki 搭建自己的博客的

一直想拥有一个真正属于自己的个人博客。

相比直接使用现成的博客平台，自己搭建网站虽然需要花一些时间，但可以完全控制网站的样式、功能和内容。同时，这个过程本身也可以成为一个学习项目。

所以我决定自己搭一个博客。

这篇文章记录的不是一篇 Astro 官方教程，而是我自己搭建这个博客的过程：为什么最后选择 Astro，为什么选择 Mizuki，以及我是如何从一个主题模板，一点一点把它改成自己的博客的。

---

## 一、为什么想做一个自己的博客

以前接触到的很多内容，往往分散在不同的平台上。

学习笔记可能放在本地，项目记录可能放在 GitHub，生活中的一些东西又可能发在其他平台。

我一直觉得，如果有一个属于自己的地方，把这些东西慢慢记录下来，会是一件挺有意思的事情。

这个博客不一定需要每天更新，也不一定需要写非常正式的文章。

它更像是一个长期维护的个人空间。

以后可以在这里记录：

- 学习过程
- 电气工程
- 电力系统
- 新能源
- 编程
- AI
- 项目开发
- 音乐
- 音游
- Galgame
- 数码设备
- 以及一些生活中的事情

所以我希望这个网站不仅仅是一个“博客模板”，而是一个以后可以不断折腾和完善的小项目。

---

## 二、为什么选择 Astro

在真正开始搭建之前，我考虑过几种不同的方案。

比较常见的方案包括 WordPress、Hexo 和 Astro。

最后我选择了 Astro。

### 1. 比较适合内容型网站

博客最核心的内容其实就是文章。

而 Astro 对 Markdown 和 MDX 的支持非常适合这种场景。

一篇文章基本就是一个 Markdown 文件，例如：

```text
src/content/posts/my-blog/build-this-blog.md
````

文章内容、标题、发布时间、标签等信息都可以直接写在 Markdown 文件中。

这样写博客的时候不需要维护一个复杂的后台系统。

### 2. 静态网站很适合个人博客

个人博客并不需要非常复杂的后端。

文章发布以后，网站的大部分内容都是相对固定的。

Astro 可以在构建的时候生成静态页面，因此部署之后不需要一直运行一个复杂的后端服务。

对于个人博客来说，这种方式非常合适。

### 3. 可以自己折腾

我比较喜欢 Astro 的一点，是它不会把所有东西都封装得特别死。

如果以后想修改页面，可以继续深入组件、配置和项目结构。

这也意味着：

> 这个博客不仅是一个网站，也是一个可以拿来学习 Web 开发的项目。

所以相比直接注册一个现成的博客平台，我更希望从代码、Git、部署一直做到域名，把整个过程自己走一遍。

---

## 三、为什么选择 Mizuki

决定使用 Astro 之后，我没有选择从零开始设计博客页面，而是找了一个已经比较完整的 Astro 博客主题。

最后选择了 Mizuki。

Mizuki 已经提供了很多个人博客常用的功能，例如：

* 首页
* 文章系统
* 标签
* 分类
* 归档
* 侧边栏
* 个人资料
* 友情链接
* 音乐播放器
* About 页面
* Markdown 扩展
* 代码高亮
* 数学公式
* 评论系统支持

如果全部自己实现，需要花很多时间。

使用现成主题以后，就可以把主要精力放在内容和个性化修改上。

不过使用主题也有一个问题。

如果只会运行：

```powershell
pnpm dev
```

而不知道主题内部是怎么组织的，那么以后想改东西还是会比较麻烦。

所以拿到 Mizuki 之后，我首先做的事情不是马上改页面，而是先把它的项目结构和配置文件大致摸清楚。

---

## 四、准备开发环境

我的开发环境是 Windows。

主要使用：

* Node.js
* pnpm
* Git
* VS Code

项目最终放在：

```text
D:\Projects\Mizuki
```

### 1. 获取 Mizuki

首先使用 Git 获取 Mizuki 项目。

拿到项目以后进入项目目录：

```powershell
cd D:\Projects\Mizuki
```

这样以后所有操作都在这个目录下进行。

### 2. 安装依赖

进入项目目录以后安装项目依赖：

```powershell
pnpm install
```

第一次安装会下载项目需要的各种依赖。

### 3. 启动开发服务器

依赖安装完成以后：

```powershell
pnpm dev
```

Astro 启动成功以后会出现类似：

```text
astro v7.1.3 ready
Local http://localhost:3000/
```

然后直接在浏览器打开：

```text
http://localhost:3000/
```

就可以看到博客。

到这里，一个可以正常运行的 Mizuki 博客就已经搭起来了。

不过此时看到的还是主题作者准备好的模板。

接下来才是真正的个性化过程。

---

## 五、认识 Mizuki 的项目结构

刚开始拿到项目时，我没有直接修改文件，而是先看看里面有哪些东西。

其中比较重要的目录包括：

```text
src/
├── components/
├── config/
├── content/
├── i18n/
├── layouts/
├── pages/
└── styles/
```

对于一个博客来说，最值得关注的是两个地方：

```text
src/config/
```

和：

```text
src/content/
```

前者主要负责网站的各种配置。

后者主要负责博客内容。

所以后面的修改基本也是围绕这两个目录展开的。

---

## 六、第一次修改网站：siteConfig

首先查看：

```text
src/config/siteConfig.ts
```

这是整个网站最重要的配置文件之一。

这里可以设置网站标题、语言、网址等信息。

我首先把网站语言修改成中文。

最终使用：

```ts
const SITE_LANG = "zh_CN";
```

Mizuki 本身已经提供了中文语言文件：

```text
src/i18n/languages/
├── en.ts
├── ja.ts
├── zh_CN.ts
└── zh_TW.ts
```

同时 `translation.ts` 中也已经注册了中文：

```text
zh_cn: zh_CN
zh_tw: zh_TW
ja: ja
```

因此使用：

```text
zh_CN
```

就可以正常启用中文。

网站主体也随之完成了基本中文化。

### 网站名称

网站名称最终准备使用：

```text
XC's Blog
```

这也是以后网站逐渐个性化的核心之一。

### siteURL

Mizuki 中还有：

```text
siteURL
```

目前项目中仍然保留主题模板提供的网址。

暂时没有修改。

原因很简单：

现在网站还处于本地开发和修改阶段，还没有正式部署，也还没有确定最终使用的独立域名。

所以现在没有必要提前修改。

等以后真正拥有自己的域名以后，再统一修改。

---

## 七、修改个人资料

接下来查看：

```text
src/config/profileConfig.ts
```

这里负责个人资料相关的信息。

主题原本使用的是模板作者的信息，包括名字和个人简介。

我首先把头像换成了自己的头像。

而名称、Bio 等文字则准备等网站整体风格确定以后再统一修改。

这样做可以避免网站还没确定风格，就反复修改个人资料。

---

## 八、调整导航栏

接下来查看：

```text
src/config/navBarConfig.ts
```

Mizuki 默认已经提供了比较丰富的导航结构。

大致包括：

```text
Home
Archive

Links
├── GitHub
├── Bilibili
└── Gitee

My
├── Anime
├── Diary
├── Gallery
└── Devices

About
├── About
└── Friends

Others
├── Projects
├── Skills
├── AI Tools
└── Timeline
```

这些页面不一定全部需要保留。

因为这是一个个人博客，并不是为了把主题提供的所有功能都打开。

所以后面会根据实际使用情况逐渐精简。

目前先把结构摸清楚，没有急着全部删除。

---

## 九、调整侧边栏

侧边栏主要涉及：

```text
src/config/sidebarConfig.ts
```

以及相关的 Sidebar Layout 配置。

目前左侧大致包括：

```text
Profile
Announcement
Tags
TOC
```

右侧包括：

```text
Site Stats
Calendar
Categories
Music
```

这里有一个比较容易搞混的地方。

`sidebarConfig` 并不一定决定组件里面具体显示什么内容。

它更主要负责：

* 哪些组件显示
* 显示在左边还是右边
* 显示顺序
* 布局
* 响应式行为

至于具体的公告、个人信息、标签等内容，则由各自的配置文件和文章数据决定。

---

## 十、公告

公告配置位于：

```text
src/config/announcementConfig.ts
```

主题原本提供的是模板内容。

例如：

```text
ブログへようこそ！これはサンプルの告知です
```

并且带有：

```text
Learn More
```

以及：

```text
/about/
```

这样的链接。

这些内容后面都会替换成自己的公告。

目前暂时没有急着设计，因为公告内容最好等网站正式确定以后再写。

---

## 十一、配置网易云音乐播放器

Mizuki 自带音乐播放器。

这一点对我来说比较有吸引力，因为我平时比较常使用网易云音乐。

音乐配置主要位于：

```text
src/config/musicConfig.ts
```

目前使用网易云音乐：

```ts
mode: "local",
server: "netease",
type: "playlist",
```

通过歌单 ID 加载歌曲。

### 一个小问题

之前修改歌单 ID 后，发现播放器没有马上按照预期变化。

所以没有继续盲目修改配置，而是直接去检查播放器的实现。

最后确认播放器的 `loadPlaylist()` 会读取：

```text
musicPlayerConfig.id
musicPlayerConfig.server
musicPlayerConfig.type
musicPlayerConfig.meting_api
```

也就是说，真正影响播放器加载内容的不只是一个歌单 ID，而是这些配置共同决定的。

确认这一点以后，播放器的问题也就比较容易定位了。

现在播放器已经可以正常使用。

以后还可以继续对播放器进行个性化调整。

---

## 十二、Banner 和壁纸

Mizuki 的首页 Banner 也可以进行修改。

目前 Banner 使用：

```text
/assets/desktop-banner/1.webp
/assets/desktop-banner/2.webp
/assets/desktop-banner/3.webp
/assets/desktop-banner/4.webp
```

移动端也有对应的 Banner 图片。

除了图片之外，Banner 上面还有：

```text
homeText
```

用于显示标题和副标题。

主题默认使用的是比较普通的博客文案。

但我不太想使用这种：

```text
Welcome to my blog
```

之类的宣传语。

我更希望这里以后放一些自己真正喜欢的内容。

目前比较倾向于使用一些 Galgame 中印象比较深刻的句子。

这部分以后会单独整理，而不是随便找几句话填进去。

---

## 十三、继续检查其他配置

在熟悉网站结构以后，我又把 `src/config/` 中其他配置大致检查了一遍。

包括：

```text
footerConfig.ts
licenseConfig.ts
sakuraConfig.ts
fullscreenWallpaperConfig.ts
commentConfig.ts
relatedPostsConfig.ts
randomPostsConfig.ts
shareConfig.ts
permalinkConfig.ts
markdownConfig.ts
expressiveCodeConfig.ts
pioConfig.ts
```

一些目前的设置如下。

### Footer

暂时关闭：

```ts
enable: false
```

### License

目前使用：

```text
CC BY-NC-SA 4.0
```

### Sakura

暂时关闭：

```ts
enable: false
```

### 全屏壁纸

目前开启：

```ts
enable: true
```

并使用与 Banner 相关的图片。

### 评论

目前暂时关闭：

```ts
enable: false
```

以后如果需要，可以再接入评论系统。

### Related Posts

相关文章功能开启：

```text
maxCount: 5
```

### Random Posts

随机文章开启：

```text
maxCount: 5
```

### Share

分享功能目前开启。

### Permalink

目前暂时没有启用自定义永久链接格式：

```text
enable: false
```

### Markdown

图片网格、WikiLink、PlantUML 等功能已经开启。

### Expressive Code

代码块增强基本保持默认设置。

### Pio

目前开启了看板娘：

```text
enable: true
position: "left"
```

使用的模型为：

```text
/pio/models/NOIR/noir.model3.json
```

---

## 十四、开始处理博客内容

配置基本摸清楚以后，我开始进入：

```text
src/content/
```

这个目录。

最开始里面有不少 Mizuki 自带的示例文章：

```text
src/content/
├── posts/
│   ├── content-pipeline-fixture.mdx
│   ├── draft.md
│   ├── encrypted-post.md
│   ├── image-grid-demo.md
│   ├── markdown-extended.md
│   ├── markdown-mermaid.md
│   ├── markdown-tutorial.md
│   ├── video.md
│   └── guide/
│       ├── cover.webp
│       └── index.md
│
└── spec/
    ├── about.md
    └── friends.md
```

这些内容大部分都是主题为了展示功能而提供的 Example。

所以后面需要逐渐清理。

---

## 十五、认识文章的 Frontmatter

`guide/index.md` 是一个比较有用的示例。

它介绍了一篇 Mizuki 文章通常应该怎么写，以及 Frontmatter 中可以有哪些字段。

例如：

```yaml
---
title: "An Example Article"
published: 2026-08-01
updated: 2026-08-08
description: "A short summary for previews."
image: ./cover.webp
tags: [Example, Guide]
category: Guides
draft: false
---
```

其中：

* `title`：文章标题
* `published`：发布时间
* `updated`：更新时间
* `description`：文章简介
* `image`：文章封面
* `tags`：标签
* `category`：分类
* `draft`：是否为草稿

这些内容以后写自己的文章时都会用到。

因此这篇文章暂时保留下来作为参考，并进行了中文化。

---

## 十六、汉化 Markdown 教程

另外一个比较完整的示例是：

```text
src/content/posts/markdown-tutorial.md
```

这原本是一篇英文 Markdown 教程。

它展示了很多 Markdown 语法，包括：

* 段落
* 标题
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

因为这些内容以后写博客时确实很有用，所以没有直接删除。

而是决定把它完整汉化。

例如原来的：

```markdown
## Block Elements
```

会改成：

```markdown
## 块级元素
```

原来的 Markdown 示例代码则尽量保留，因为它们本身就是教程的一部分。

这样既可以保留主题自带的 Markdown 功能演示，也可以作为以后自己写文章时的参考。

---

## 十七、Mizuki 的独立 Content Git 仓库

在处理 `src/content` 的过程中，还发现 Mizuki 支持另一种内容管理方式。

项目中存在：

```text
scripts/sync-content.js
```

这个脚本支持使用一个独立的 Content Git 仓库。

它默认寻找：

```text
D:\Projects\Mizuki\content
```

然后把里面的内容同步到：

```text
src/content/posts
src/content/spec
src/data
public/images
```

理论上可以变成：

```text
Mizuki 项目
+
独立 Content 仓库
```

两个 Git 仓库分别管理。

---

## 十八、为什么暂时不用独立 Content 仓库

启动项目的时候出现过：

```text
内容目录不存在：D:\Projects\Mizuki\content
警告：未设置 CONTENT_REPO_URL，将使用本地内容
```

一开始看到这个提示容易以为是项目出错了。

后来检查了：

```text
scripts/sync-content.js
```

才发现这其实只是一个可选功能。

如果没有配置：

```text
CONTENT_REPO_URL
```

项目就继续使用本地：

```text
src/content/
```

因此这个提示不是网站运行错误。

目前也不需要专门创建：

```text
D:\Projects\Mizuki\content
```

更不需要为了它额外建立一个 Git 仓库。

---

## 十九、为什么现在不使用 .env

之前也检查过项目根目录下有没有：

```text
.env
```

使用：

```powershell
Get-Content .\.env
```

结果显示：

```text
找不到路径，因为该路径不存在
```

这也是正常的。

因为我们目前根本没有启用独立 Content 仓库。

所以现在：

```text
没有 .env
没有 CONTENT_REPO_URL
没有独立 Content 仓库
```

都没有问题。

目前直接使用：

```text
src/content/
```

管理博客文章即可。

以后如果真的需要把文章独立成第二个 Git 仓库，再考虑启用这个功能。

---

## 二十、建立自己的文章目录

在逐渐清理模板内容以后，我准备建立一个专门存放自己文章的目录：

```text
src/content/posts/my-blog/
```

通过 PowerShell 创建：

```powershell
New-Item -ItemType Directory .\src\content\posts\my-blog -Force
```

最终目录变成：

```text
src/content/posts/
│
├── markdown-tutorial.md
│
├── guide/
│   ├── cover.webp
│   └── index.md
│
└── my-blog/
```

以后自己的文章就可以放在：

```text
my-blog/
```

里面。

例如这篇文章本身：

```text
my-blog/build-this-blog.md
```

这样主题自带的示例文章和自己真正写的文章就可以区分开。

---

## 二十一、Git：整个项目的版本管理

这个博客从一开始就使用 Git 管理。

这里需要区分两个概念。

目前使用的是：

```text
一个 Git 仓库
        ↓
整个 Mizuki 项目
```

而不是：

```text
Mizuki Git 仓库
        +
Blog Content Git 仓库
```

后者虽然 Mizuki 支持，但目前没有必要。

对于现在这个阶段来说，一个仓库更加简单：

```text
项目代码
+
配置
+
文章
+
图片
```

一起进行版本管理。

以后每完成一部分修改，就可以通过 Git 保存一个版本。

这样如果某次修改把网站改坏了，也可以比较容易地回退。

---

## 二十二、未来准备使用 GitHub

现在博客主要还是本地开发。

后面的计划是：

```text
本地 Mizuki
      ↓
Git
      ↓
GitHub
      ↓
部署平台
      ↓
正式网站
```

这样以后：

* 本地修改
* Git 提交
* GitHub 保存
* 部署平台自动构建

整个流程就可以串起来。

这也是我选择 Git 管理整个项目的主要原因之一。

---

## 二十三、独立域名

现在 `siteConfig.ts` 中仍然保留着主题原本的：

```text
siteURL
```

暂时没有修改。

这是因为目前还没有确定最终的域名和部署方案。

未来如果购买一个真正属于自己的域名，例如：

```text
https://example.com/
```

那么再修改：

```ts
siteURL: "https://example.com/"
```

同时配置：

```text
DNS
+
部署平台
+
域名
```

这样博客才真正从本地项目变成一个公开的网站。

---

## 二十四、现在博客已经走到哪一步了？

到现在为止，整个过程已经从最初的：

```text
一个 Mizuki 模板
```

逐渐变成：

```text
XC's Blog
```

目前已经完成或者基本完成：

* Astro 本地运行
* Mizuki 安装
* 中文化
* 网站基本配置
* 头像替换
* Navbar 结构检查
* Sidebar 结构检查
* 网易云音乐播放器配置
* Banner / 壁纸结构检查
* Markdown 配置检查
* About 页面处理
* Markdown 教程汉化
* 写作结构示例整理
* `my-blog` 文章目录建立
* Git 作为整个项目的版本管理

目前还没有正式完成的部分包括：

* 最终 Profile 文案
* Navbar 最终结构
* Announcement
* Banner 最终图片和文字
* Galgame 名句
* Friends 页面
* Example 内容彻底清理
* 第一批正式博客文章
* GitHub 仓库
* 网站部署
* 独立域名

---

## 二十五、接下来

接下来不会再急着修改大量配置。

目前项目已经完成了从：

```text
“能跑起来的 Mizuki 模板”
```

到：

```text
“开始属于 XC 的个人博客”
```

这个阶段。

下一步主要就是继续清理主题自带的 Example 内容，然后开始真正写自己的文章。

以后如果需要，还可以继续完善：

* 首页视觉风格
* Banner
* 个人资料
* 导航栏
* 音乐播放器
* 文章分类
* 标签
* About 页面
* Friends 页面
* GitHub
* 自动部署
* 独立域名

我希望这个博客最终不是一个“套了个主题的个人网站”，而是一个能够长期维护的个人空间。

以后无论是学习电气工程、做项目、研究 AI，还是记录音乐、游戏和生活，都可以慢慢放到这里。

**博客本身也会成为我学习和折腾的一部分。**

```
```
