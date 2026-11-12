# VizReport

**单文件·零依赖·富交互报告生成器**

> [English Documentation](README.md) · [在线演示](https://magicalyu.github.io/vizreport)

## 什么是 VizReport？

VizReport 是一个 Claude Code / Agent Skill，把任何调研、分析或项目数据转化为**自包含的交互式 HTML 报告**。无需构建工具、无需 CDN、无需服务器——一个 `.html` 文件，双击即开。

## 快速开始

```bash
npx skills add MagicalYuYu/vizreport
```

然后对 Claude 说「把这次调研做成可视化报告」即可。

也可以手动使用：下载 `templates/report.template.html`，修改其中的 JSON 数据岛，浏览器打开。

## 核心特性

- **13 种内容块**：段落 / 列表 / 统计卡 / 图表（柱状/条形/折线/圆环）/ 卡片墙 / 表格 / 提示框 / 引文 / 图片 / 时间线 / 流程图 / 思维导图
- **全交互**：搜索 / 三态排序 / 行筛选 + 列筛选 / 章节折叠 / 主题切换 / 宽度滑条 / 字号调节 / 可拖拽目录
- **纯 SVG 图表**：悬停显示详情（数值+占比+基数），零外部依赖
- **双布局**：叙事报告（report）+ 清单看板（cardwall），Agent 自动路由
- **报告索引**：一键生成全部报告的统一索引页
- **离线可用**：零网络请求，2018 年后的任何浏览器都能打开

## 许可

MIT
