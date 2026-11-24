# 每日 AI 早报（Daily AI Briefing）

每天早上 **08:30（Asia/Shanghai）** 自动联网搜索过去 24 小时内 AI 领域的重要动态与 GitHub Trending 热门开源项目，过滤水文和营销软文，精选最值得关注的 5 条内容，用大白话讲清**核心亮点**与**技术价值**，生成简约浅色卡片风的单文件 HTML 早报，浏览器打开即可离线阅读。

## 目录结构

```text
.
├── code/
│   ├── SKILL.md               # AI 早报生成规范与 Agent Skill 定义
│   ├── template.htm           # 简约浅色卡片风单文件 HTML 模板
│   └── generate_briefing.py   # 将结构化 JSON 渲染为早报 HTML 的脚本
├── news/
│   └── AI早报-20261124.htm    # 示例早报（仅上传 1 天用于展示，每日新增早报已通过 .gitignore 忽略）
├── .gitignore
└── README.md
```

## 特性

- **去噪精选**：聚焦大模型发布、硬核论文/技术突破、Agent 基础设施与 GitHub Trending 热门开源项目，过滤营销水文。
- **大白话解读**：每条均包含「核心亮点」「技术价值」和可点击跳转的原始出处链接。
- **零依赖单文件网页**：简约浅色卡片风，内置分类筛选栏与移动端适配，双击 `.htm` 即可直接查看。
- **定时无人值守**：配合定时自动化任务，每日 08:30 自动生成并保存到 `news/AI早报-YYYYMMDD.htm`。

## 快速预览

下载后直接用浏览器打开 [`news/AI早报-20261124.htm`](news/AI早报-20261124.htm) 即可查看效果。

## 手动渲染示例

```bash
python code/generate_briefing.py data.json
```

`data.json` 结构示例：

```json
{
  "date": "2026-11-24",
  "summary_lead": "今日聚焦...",
  "items": [
    {
      "category": "开源项目",
      "source": "owner / repo",
      "title": "项目标题",
      "highlight": "大白话核心亮点",
      "value": "技术价值说明",
      "url": "https://github.com/owner/repo"
    }
  ]
}
```
