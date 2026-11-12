# VizReport

**单文件·零依赖·富交互报告生成器**

> [English](README.md) | [在线演示](https://magicalyuyu.github.io/vizreport/)

## 为什么需要 VizReport？

AI Agent 产出的调研报告通常是 Markdown——大段纯文本、无图表、无排序、无导航。读到第五份的时候，眼睛已经花了。

VizReport 解决两个问题：

- **可视化**：柱状图/折线图/圆环图（纯 SVG 零依赖，悬停显示详情）、可排序筛选的表格、时间线、流程图、思维导图
- **交互性**：粘滞目录、章节折叠、主题切换、字号调节、宽度滑条——读者的每一次操作都是即时的

## 效果

所有功能可以直接在[在线演示](https://magicalyuyu.github.io/vizreport/)中体验——那个页面本身就是一份 VizReport 报告。

## 安装

```bash
npx skills add MagicalYuYu/vizreport
```

然后对 Agent 说「把这次调研做成可视化报告」。

也可以手动使用：下载 `templates/` 里的模板，修改 JSON 数据岛，浏览器打开。

## 与 Markdown 的区别

| 方面 | Markdown | VizReport |
|------|----------|-----------|
| 图表 | 原生不支持 | 交互式 SVG（悬停显示数值与占比） |
| 表格 | 静态，不可排序 | 三态排序 + 行筛选 + 列筛选 |
| 导航 | 只能滚动 | 粘滞目录 + 可折叠章节 |
| 主题 | 依赖阅读器 | 亮色/暗色切换，跨文件记忆 |
| 字号 | 依赖阅读器 | 内置五档调节 |
| 分享 | 需要 Markdown 渲染器 | 双击任何 HTML 文件 |
| 离线 | 取决于查看器 | 零网络请求 |

## 浏览器兼容

Chrome、Firefox、Safari、Edge（2018 年及以后）。手机自适应。完全离线可用。

## 许可

MIT
