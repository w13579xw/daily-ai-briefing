#!/usr/bin/env python3
"""将结构化 JSON 早报数据渲染为简约浅色卡片风的单文件 HTML 网页。"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
from pathlib import Path
from urllib.parse import urlparse

WEEKDAYS_CN = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

TAG_CLASS_MAP = {
    "行业动态": "tag-industry",
    "开源模型": "tag-model",
    "模型发布": "tag-model",
    "技术突破": "tag-research",
    "开源项目": "tag-github",
    "GitHub 热门": "tag-github",
    "工具生态": "tag-tool",
}


def render_briefing(data: dict, template_path: Path, output_path: Path) -> None:
    date_str = data.get("date") or dt.date.today().strftime("%Y-%m-%d")
    parsed_date = dt.date.fromisoformat(date_str)
    date_cn = f"{parsed_date.year}年{parsed_date.month}月{parsed_date.day}日"
    weekday_cn = WEEKDAYS_CN[parsed_date.weekday()]

    items: list[dict] = data.get("items", [])
    categories: list[str] = []
    for item in items:
        cat = item.get("category", "行业动态")
        if cat not in categories:
            categories.append(cat)

    filter_buttons = [
        f'<button class="filter-btn active" data-filter="all">全部 ({len(items)})</button>'
    ]
    for cat in categories:
        esc_cat = html.escape(cat)
        filter_buttons.append(
            f'<button class="filter-btn" data-filter="{esc_cat}">{esc_cat}</button>'
        )

    cards_html: list[str] = []
    for idx, item in enumerate(items, start=1):
        cat = item.get("category", "行业动态")
        tag_cls = TAG_CLASS_MAP.get(cat, "tag-industry")
        url = item.get("url", "#")
        domain = item.get("domain") or urlparse(url).netloc or url
        link_text = "访问 GitHub 仓库 ↗" if "github.com" in url else "查看原始链接 ↗"

        card = f"""      <article class="card" data-category="{html.escape(cat)}">
        <div class="card-meta">
          <div class="meta-left">
            <span class="index-num">{idx:02d}</span>
            <span class="tag {tag_cls}">{html.escape(cat)}</span>
          </div>
          <span class="source-label">{html.escape(item.get("source", ""))}</span>
        </div>
        <h2 class="card-title">{html.escape(item.get("title", ""))}</h2>
        <div class="section-block">
          <div class="section-label">核心亮点</div>
          <p class="section-text">{html.escape(item.get("highlight", ""))}</p>
        </div>
        <div class="value-box">
          <div class="section-label">技术价值</div>
          <p class="section-text">{html.escape(item.get("value", ""))}</p>
        </div>
        <div class="card-footer">
          <span class="link-domain">{html.escape(domain)}</span>
          <a class="link-btn" href="{html.escape(url)}" target="_blank" rel="noopener noreferrer">
            {link_text}
          </a>
        </div>
      </article>"""
        cards_html.append(card)

    template = template_path.read_text(encoding="utf-8")
    rendered = (
        template.replace("{{DATE_CN}}", date_cn)
        .replace("{{WEEKDAY_CN}}", weekday_cn)
        .replace("{{DATE_ISO}}", date_str)
        .replace("{{SUMMARY_LEAD}}", html.escape(data.get("summary_lead", "")))
        .replace("{{ITEM_COUNT}}", str(len(items)))
        .replace("{{FILTER_BUTTONS}}", "\n      ".join(filter_buttons))
        .replace("{{CARDS_HTML}}", "\n\n".join(cards_html))
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="生成简约浅色卡片风 AI 早报 HTML")
    parser.add_argument("input_json", type=Path, help="输入 JSON 文件路径")
    parser.add_argument(
        "-t",
        "--template",
        type=Path,
        default=Path(__file__).with_name("template.htm"),
        help="HTML 模板路径",
    )
    parser.add_argument("-o", "--output", type=Path, help="输出 HTML 文件路径")
    args = parser.parse_args()

    data = json.loads(args.input_json.read_text(encoding="utf-8"))
    date_compact = (data.get("date") or dt.date.today().strftime("%Y-%m-%d")).replace("-", "")
    output_path = args.output or (
        Path(__file__).resolve().parent.parent / "news" / f"AI早报-{date_compact}.htm"
    )
    render_briefing(data, args.template, output_path)
    print(f"已生成早报: {output_path}")


if __name__ == "__main__":
    main()
