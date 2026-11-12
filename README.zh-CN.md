<p align="center">
  <img src="docs/assets/social-preview.png" alt="VizReport" width="100%">
</p>

<h1 align="center">VizReport</h1>

<p align="center"><strong>富交互报告。单文件。零依赖。</strong></p>

<p align="center"><sub><a href="README.md">English</a> · <a href="https://magicalyuyu.github.io/vizreport/">在线演示</a></sub></p>

---

## 问题所在

AI Agent 产出的调研报告是 Markdown 格式。几百行纯文本，没有图表，没有可排序的表格，没有导航——只能无尽滚动。读到当天第五份报告时，眼睛已经花了。

我们做 VizReport 是因为受够了这些：

- **可视化差距**：Markdown 渲染出来就是纯文本段落。数字混在一起，趋势没有图表就看不见。
- **交互差距**：你不能排序 Markdown 表格，不能按标签筛选，不能折叠不需要的章节，不能调整字号。
- **分享摩擦**：发一个 `.md` 文件对方得装渲染器。发一个 VizReport 对方双击就能打开。就这么多。

## 解决方案

VizReport 是一个 Agent Skill，把同样的内容转化为**自包含的交互式 HTML 文件**：

- 图表渲染为纯 SVG，悬停显示数据详情（无 CDN，离线可用）
- 表格支持三态排序、关键字筛选、按列值筛选
- 粘滞目录树，章节可折叠
- 亮色/暗色主题切换，偏好跨文件持久化
- 内容宽度像素级调节，五档字号控制
- 全部在一个 `.html` 文件里，约 50-80 KB

你正在阅读的这个页面（[在线演示](https://magicalyuyu.github.io/vizreport/)）就是一份 VizReport 文件。上面描述的每个功能都可以在那个页面上直接体验。

## 效果展示

![VizReport 演示](docs/assets/demo.gif)

![VizReport 功能](docs/assets/screenshot-features.png)

## 快速开始

### 安装为 Claude Code Skill

```bash
npx skills add MagicalYuYu/vizreport
```

然后对 Agent 说：

> 把这次调研做成可视化报告

Skill 会自动选择合适的布局（叙事报告或清单看板），生成数据，输出单个 HTML 文件。

### 手动使用（无需 Agent）

从 `templates/` 目录下载模板，用文本编辑器打开，找到 `<script id="aos-data">` 块，把 JSON 替换为你的内容，保存后浏览器打开。

## 内容块类型

VizReport 支持十三种内容块：

| 类别 | 内容块 |
|------|--------|
| 文本 | 标题（两级，自动进目录）、段落（加粗/代码/链接）、列表、引文 |
| 数据 | 统计卡、图表（柱状/条形/折线/圆环）、表格 |
| 视觉 | 时间线（路线图/里程碑）、流程图（工序/演化路径）、思维导图（概念图/结构发散） |
| 媒体 | 图片（带图注与降级占位）、提示框（信息/警告/危险/成功） |

所有图表渲染为内联 SVG，零外部依赖。所有表格开箱即用支持排序和筛选。

## 与 Markdown 的区别

| 方面 | Markdown | VizReport |
|------|----------|-----------|
| 图表 | 原生不支持 | 交互式 SVG，悬停显示数值与占比 |
| 表格 | 静态，不可排序 | 三态排序 + 行筛选 + 按列筛选 |
| 导航 | 只能线性滚动 | 粘滞目录树 + 可折叠章节 |
| 主题 | 依赖阅读器 | 亮色/暗色切换，跨访问记忆 |
| 字号 | 依赖阅读器 | 内置五档控制 |
| 分享 | 需要 Markdown 渲染器 | 双击任何 HTML 文件 |
| 离线 | 取决于查看器 | 零网络请求 |

## 浏览器兼容

Chrome、Firefox、Safari、Edge（2018 年及以后）。手机自适应响应式布局。完全离线可用。

## 架构

```
+-------------------------------------------+
|            单个 HTML 文件                  |
+-------------------------------------------+
|  <script id="aos-data">                   |
|    { meta, blocks: [...] }  ← 你的数据    |
|  </script>                                |
|  <style> CSS 令牌 + 主题 </style>         |
|  <script> 渲染器 (原生 JS) </script>      |
+-------------------------------------------+
        无构建步骤 · 无 CDN · 无服务器
```

## 报告索引

为你所有的报告生成一个可搜索的索引页：

```bash
python scripts/build_index.py
```

生成自包含的 `showcase-index.html`，支持卡片/列表/详细三种视图。搜索、置顶、隐藏、内嵌预览全部内置。

## 许可

MIT
