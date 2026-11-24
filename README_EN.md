<p align="center">
  <a href="./README.md">简体中文</a> | <strong>English</strong>
</p>

# Daily AI Briefing

An automated daily AI digest workflow that runs every morning at **08:30 (Asia/Shanghai)**. It searches key AI developments and trending GitHub open-source projects from the past 24 hours, filters out hype and fluff, curates the top 5 stories with plain-language **highlights** and **technical value**, and renders a clean, light-card single-file HTML briefing for offline reading.

## Directory Structure

```text
.
├── code/
│   ├── SKILL.md               # Agent Skill specification & briefing guidelines
│   ├── template.htm           # Clean light-card single-file HTML template
│   └── generate_briefing.py   # Script to render structured JSON into HTML
├── news/
│   └── AI早报-20261124.htm    # Sample briefing (daily outputs ignored via .gitignore)
├── .gitignore
├── README.md
└── README_EN.md
```

## Features

- **Signal over Noise**: Focuses on LLM releases, research breakthroughs, Agent infrastructure, and GitHub Trending projects.
- **Plain-Language Insights**: Every item includes key highlights, technical takeaways, and clickable source links.
- **Zero-Dependency Single HTML**: Responsive card UI with category filters—just double-click the `.htm` file in any browser.
- **Scheduled Automation**: Generates `news/AI早报-YYYYMMDD.htm` automatically at 08:30 every day.

## Quick Preview

Open [`news/AI早报-20261124.htm`](news/AI早报-20261124.htm) directly in your browser.

## Manual Rendering

```bash
python code/generate_briefing.py data.json
```

Example `data.json`:

```json
{
  "date": "2026-11-24",
  "summary_lead": "Today's focus...",
  "items": [
    {
      "category": "Open Source",
      "source": "owner / repo",
      "title": "Project Title",
      "highlight": "Plain-language summary of what matters",
      "value": "Technical value and why it's worth watching",
      "url": "https://github.com/owner/repo"
    }
  ]
}
```
