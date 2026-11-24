#!/usr/bin/env python3
"""将结构化 JSON 早报数据渲染为简约浅色炫酷多栏卡片风单文件 HTML 网页。"""

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

MEDIA_ORDER = ["新智元", "量子位", "机器之心"]

MEDIA_META = {
    "新智元": {
        "row_cls": "row-xzy",
        "brand_cls": "brand-xzy",
        "sub": "AI_era",
        "svg": """<svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M12 2.5L14.4 8.6L20.5 11L14.4 13.4L12 19.5L9.6 13.4L3.5 11L9.6 8.6L12 2.5Z" stroke="white" stroke-width="1.8" stroke-linejoin="round"/>
          <circle cx="12" cy="11" r="2.2" fill="white"/>
          <circle cx="19" cy="4.5" r="1.3" fill="white" opacity="0.85"/>
        </svg>""",
    },
    "量子位": {
        "row_cls": "row-qbit",
        "brand_cls": "brand-qbit",
        "sub": "QbitAI",
        "svg": """<svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <ellipse cx="12" cy="12" rx="9" ry="4.2" transform="rotate(-32 12 12)" stroke="white" stroke-width="1.7"/>
          <ellipse cx="12" cy="12" rx="9" ry="4.2" transform="rotate(32 12 12)" stroke="white" stroke-width="1.7" opacity="0.88"/>
          <circle cx="12" cy="12" r="2.6" fill="white"/>
        </svg>""",
    },
    "机器之心": {
        "row_cls": "row-jqzx",
        "brand_cls": "brand-jqzx",
        "sub": "Synced",
        "svg": """<svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M12 20.2C12 20.2 4.2 15.3 4.2 9.4C4.2 6.6 6.4 4.5 9 4.5C10.5 4.5 11.4 5.3 12 6.3C12.6 5.3 13.5 4.5 15 4.5C17.6 4.5 19.8 6.6 19.8 9.4C19.8 15.3 12 20.2 12 20.2Z" stroke="white" stroke-width="1.8" stroke-linejoin="round"/>
          <path d="M7.5 11.2H10L11.2 8.8L12.8 13.4L14 11.2H16.5" stroke="white" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>""",
    },
}


def format_time_label(published_at: str) -> str:
    """将 2026-11-23 21:30 格式化为更紧凑的 11-23 21:30。"""
    s = (published_at or "").strip()
    if len(s) >= 10 and s[4] == "-" and s[7] == "-":
        return s[5:]
    return s or "近期"


def render_wechat_section(wechat_items: list[dict]) -> str:
    if not wechat_items:
        return ""

    grouped: dict[str, list[dict]] = {m: [] for m in MEDIA_ORDER}
    for item in wechat_items:
        media = item.get("media", "")
        grouped.setdefault(media, []).append(item)

    rows_html: list[str] = []
    for media in list(grouped.keys()):
        items = grouped[media]
        if not items:
            continue

        # 按推送时间从近到远倒序排列
        items = sorted(
            items,
            key=lambda x: (x.get("published_at") or x.get("date") or ""),
            reverse=True,
        )

        meta = MEDIA_META.get(
            media,
            {
                "row_cls": "row-xzy",
                "brand_cls": "brand-xzy",
                "sub": "WeChat",
                "svg": MEDIA_META["新智元"]["svg"],
            },
        )

        cards: list[str] = []
        for item in items:
            title = item.get("title", "")
            summary = item.get("summary", "")
            pub_raw = item.get("published_at") or item.get("date") or ""
            pub_label = format_time_label(pub_raw)

            wechat_url = item.get("wechat_url") or ""
            article_url = item.get("article_url") or ""
            primary_url = wechat_url if "mp.weixin.qq.com" in wechat_url else (article_url or wechat_url or "#")
            is_wechat_direct = "mp.weixin.qq.com" in primary_url
            btn_cls = "wx-btn" if is_wechat_direct else "link-btn"
            btn_label = "微信原文 ↗" if is_wechat_direct else "阅读原文 ↗"

            extra_links: list[str] = []
            if is_wechat_direct and article_url and article_url != primary_url:
                extra_links.append(
                    f'                <a class="resource-btn" href="{html.escape(article_url)}" target="_blank" rel="noopener noreferrer">同步报道 ↗</a>'
                )

            for res in item.get("resources", []):
                res_label = html.escape(res.get("label", "相关资料"))
                res_url = html.escape(res.get("url", "#"))
                extra_links.append(
                    f'                <a class="resource-btn" href="{res_url}" target="_blank" rel="noopener noreferrer">{res_label} ↗</a>'
                )

            extra_html = "\n".join(extra_links)
            card = f"""            <article class="wechat-card">
              <div class="wechat-meta-top">
                <span class="time-pill">🕒 {html.escape(pub_label)}</span>
              </div>
              <h3 class="wechat-title">{html.escape(title)}</h3>
              <p class="wechat-summary">{html.escape(summary)}</p>
              <div class="card-footer">
                <div class="link-group">
                  <a class="{btn_cls}" href="{html.escape(primary_url)}" target="_blank" rel="noopener noreferrer">{btn_label}</a>
{extra_html}
                </div>
              </div>
            </article>"""
            cards.append(card)

        cards_joined = "\n".join(cards)
        row = f"""        <div class="media-row {meta['row_cls']}">
          <div class="media-brand {meta['brand_cls']}">
            <div class="media-logo">{meta['svg']}</div>
            <div>
              <div class="media-name">{html.escape(media)}</div>
              <div class="media-sub">{meta['sub']}</div>
            </div>
            <span class="media-count">{len(items)} 篇</span>
          </div>
          <div class="media-track-wrap">
            <button class="scroll-arrow left hidden" type="button" aria-label="向左滑动">‹</button>
            <div class="media-cards">
{cards_joined}
            </div>
            <button class="scroll-arrow right hidden" type="button" aria-label="向右滑动">›</button>
          </div>
        </div>"""
        rows_html.append(row)

    rows_joined = "\n\n".join(rows_html)
    return f"""    <section aria-label="中文科研公众号">
      <div class="section-bar">
        <div class="section-title-wrap">
          <span class="section-accent-bar" aria-hidden="true"></span>
          <h2>中文科研公众号</h2>
        </div>
      </div>
      <div class="media-rows">
{rows_joined}
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
        link_text = "GitHub ↗" if "github.com" in url else "原文 ↗"

        card = f"""      <article class="card" data-category="{html.escape(cat)}">
        <div class="card-meta">
          <div class="meta-left">
            <span class="index-num">{idx:02d}</span>
            <span class="tag {tag_cls}">{html.escape(cat)}</span>
          </div>
          <span class="source-label">{html.escape(item.get("source", ""))}</span>
        </div>
        <h3 class="card-title">{html.escape(item.get("title", ""))}</h3>
        <div class="card-body">
          <p class="section-text"><span class="inline-label">亮点：</span>{html.escape(item.get("highlight", ""))}</p>
          <div class="value-box">
            <p class="section-text"><span class="inline-label">价值：</span>{html.escape(item.get("value", ""))}</p>
          </div>
        </div>
        <div class="card-footer">
          <span class="link-domain">{html.escape(domain)}</span>
          <a class="link-btn" href="{html.escape(url)}" target="_blank" rel="noopener noreferrer">{link_text}</a>
        </div>
      </article>"""
        cards_html.append(card)

    wechat_section_html = render_wechat_section(wechat_items)
    main_grid_class = "has-featured" if len(items) % 2 == 1 else ""

    template = template_path.read_text(encoding="utf-8")
    rendered = (
        template.replace("{{DATE_CN}}", date_cn)
        .replace("{{WEEKDAY_CN}}", weekday_cn)
        .replace("{{DATE_ISO}}", date_str)
        .replace("{{SUMMARY_LEAD}}", html.escape(data.get("summary_lead", "")))
        .replace("{{ITEM_COUNT}}", str(len(items)))
        .replace("{{WECHAT_COUNT}}", str(len(wechat_items)))
        .replace("{{MAIN_GRID_CLASS}}", main_grid_class)
        .replace("{{FILTER_BUTTONS}}", "\n        ".join(filter_buttons))
        .replace("{{CARDS_HTML}}", "\n\n".join(cards_html))
        .replace("{{WECHAT_SECTION_HTML}}", wechat_section_html)
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="生成简约浅色炫酷多栏卡片风 AI 早报 HTML")
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
