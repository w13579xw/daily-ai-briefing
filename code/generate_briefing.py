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

MEDIA_CLASS_MAP = {
    "新智元": "media-xzy",
    "量子位": "media-qbit",
    "机器之心": "media-jqzx",
}


def render_wechat_section(wechat_items: list[dict]) -> str:
    if not wechat_items:
        return ""

    cards: list[str] = []
    for idx, item in enumerate(wechat_items, start=1):
        media = item.get("media", "AI 媒体")
        media_cls = MEDIA_CLASS_MAP.get(media, "media-other")
        article_url = item.get("article_url", "#")
        article_label = item.get("article_label") or "推文原文 ↗"

        resource_links: list[str] = []
        for res in item.get("resources", []):
            res_label = html.escape(res.get("label", "相关资料"))
            res_url = html.escape(res.get("url", "#"))
            resource_links.append(
                f'          <a class="resource-btn" href="{res_url}" target="_blank" rel="noopener noreferrer">{res_label} ↗</a>'
            )

        resources_html = "\n".join(resource_links)
        card = f"""        <article class="card wechat-card">
          <div class="card-meta">
            <div class="meta-left">
              <span class="index-num">W{idx:02d}</span>
              <span class="tag {media_cls}">{html.escape(media)}</span>
            </div>
            <span class="source-label">{html.escape(item.get("date", ""))}</span>
          </div>
          <h3 class="card-title">{html.escape(item.get("title", ""))}</h3>
          <div class="section-block">
            <p class="section-text">{html.escape(item.get("summary", ""))}</p>
          </div>
          <div class="card-footer">
            <div class="link-group">
              <a class="link-btn" href="{html.escape(article_url)}" target="_blank" rel="noopener noreferrer">{html.escape(article_label)}</a>
{resources_html}
            </div>
          </div>
        </article>"""
        cards.append(card)

    cards_joined = "\n\n".join(cards)
    return f"""    <section class="wechat-section" aria-label="中文科研公众号精选">
      <div class="section-heading">
        <h2>中文科研公众号精选</h2>
        <span>新智元 · 量子位 · 机器之心（附推文原文与论文/代码资料）</span>
      </div>
      <div class="cards">
{cards_joined}
      </div>
    </section>"""


def render_briefing(data: dict, template_path: Path, output_path: Path) -> None:
    date_str = data.get("date") or dt.date.today().strftime("%Y-%m-%d")
    parsed_date = dt.date.fromisoformat(date_str)
    date_cn = f"{parsed_date.year}年{parsed_date.month}月{parsed_date.day}日"
    weekday_cn = WEEKDAYS_CN[parsed_date.weekday()]

    items: list[dict] = data.get("items", [])
    wechat_items: list[dict] = data.get("wechat_items", [])

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

    wechat_section_html = render_wechat_section(wechat_items)

    template = template_path.read_text(encoding="utf-8")
    rendered = (
        template.replace("{{DATE_CN}}", date_cn)
        .replace("{{WEEKDAY_CN}}", weekday_cn)
        .replace("{{DATE_ISO}}", date_str)
        .replace("{{SUMMARY_LEAD}}", html.escape(data.get("summary_lead", "")))
        .replace("{{ITEM_COUNT}}", str(len(items)))
        .replace("{{WECHAT_COUNT}}", str(len(wechat_items)))
        .replace("{{FILTER_BUTTONS}}", "\n      ".join(filter_buttons))
        .replace("{{CARDS_HTML}}", "\n\n".join(cards_html))
        .replace("{{WECHAT_SECTION_HTML}}", wechat_section_html)
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
