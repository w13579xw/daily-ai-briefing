<p align="center">
  <strong>简体中文</strong> | <a href="./README_EN.md">English</a>
</p>

# 每日 AI 早报（Daily AI Briefing）

每天早上 **08:30（Asia/Shanghai）** 自动联网搜索过去 24 小时内 AI 领域的重要动态、GitHub Trending 热门开源项目，以及 **新智元、量子位、机器之心** 等科研微信公众号的高价值推文，用大白话讲清**核心亮点**与**技术价值**，并附上推文原文链接与论文/开源仓库等相关资料链接，生成简约浅色卡片风的单文件 HTML 早报，浏览器打开即可离线阅读。

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
├── README.md
└── README_EN.md
```

## 特性

- **双板块炫酷浅色多栏排版**：
  - **中文科研公众号（上方，横排三行 + 左侧专属 Logo）**：依次按 **新智元 · 量子位 · 机器之心** 横向排布前一天全部文章，优先附微信公众号原文链接（未索引时自动提供搜狗微信精准直达 + 同步报道）及对应的**论文 / GitHub / Hugging Face 等相关资料链接**。
  - **前沿动态 & GitHub 热门（下方，5 条 2 列矩阵）**：聚焦大模型发布、硬核技术突破、Agent 基础设施与 GitHub Trending 开源项目，每条含大白话核心亮点、技术价值与原始链接。
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
      "category": "GitHub 热门",
      "source": "owner / repo",
      "title": "项目标题",
      "highlight": "大白话核心亮点",
      "value": "技术价值说明",
      "url": "https://github.com/owner/repo"
    }
  ],
  "wechat_items": [
    {
      "media": "量子位",
      "date": "2026-11-24",
      "title": "推文标题",
      "summary": "大白话要点摘要",
      "article_url": "https://example.com/article",
      "resources": [
        { "label": "Hugging Face 模型", "url": "https://huggingface.co/..." },
        { "label": "GitHub 仓库", "url": "https://github.com/..." }
      ]
    }
  ]
}
```
