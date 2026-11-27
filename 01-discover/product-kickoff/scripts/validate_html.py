#!/usr/bin/env python3
"""Validate the offline HTML prototype template with only the Python standard library."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path


class TagCollector(HTMLParser):
    """Collect tags and basic nesting information without third-party packages."""

    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.ids: list[str] = []
        self.resources: list[tuple[str, str, str]] = []
        self.style_values: list[str] = []
        self.open_tags: list[str] = []
        self.mismatched_end_tags: list[str] = []

    VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    RESOURCE_ATTRS = {
        "img": ("src", "srcset"),
        "script": ("src",),
        "link": ("href",),
        "iframe": ("src",),
        "video": ("src", "poster"),
        "audio": ("src",),
        "source": ("src", "srcset"),
        "embed": ("src",),
        "object": ("data",),
        "track": ("src",),
        "input": ("src",),
        "image": ("href", "xlink:href"),
        "use": ("href", "xlink:href"),
    }

    def _collect(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            lowered = name.lower()
            if lowered == "id" and value:
                self.ids.append(value)
            elif lowered == "style" and value:
                self.style_values.append(value)
            elif value and lowered in self.RESOURCE_ATTRS.get(tag, ()):
                self.resources.append((tag, lowered, value))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        normalized = tag.lower()
        self.tags.append(normalized)
        self._collect(normalized, attrs)
        if normalized not in self.VOID_TAGS:
            self.open_tags.append(normalized)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        normalized = tag.lower()
        self.tags.append(normalized)
        self._collect(normalized, attrs)

    def handle_endtag(self, tag: str) -> None:
        normalized = tag.lower()
        if normalized not in self.open_tags:
            self.mismatched_end_tags.append(normalized)
            return
        if self.open_tags[-1] != normalized:
            self.mismatched_end_tags.append(normalized)
            while self.open_tags and self.open_tags[-1] != normalized:
                self.open_tags.pop()
        if self.open_tags:
            self.open_tags.pop()


def has_tag(tags: list[str], tag: str) -> bool:
    return tag in tags


def detect_prototype_type(content: str) -> str:
    """Infer the prototype family from stable structural markers."""
    app_markers = ("class=\"phone\"", "class=\"screen\"", "m-header", "m-footer", "data-preview")
    web_markers = ("app-shell", "prototype-pane", "requirements-pane", "table-wrap")
    app_hits = sum(marker in content for marker in app_markers)
    web_hits = sum(marker in content for marker in web_markers)
    if app_hits >= 3:
        return "APP/H5"
    if web_hits >= 2:
        return "Web"
    return "未知"


def print_group(title: str, items: list[str]) -> None:
    print(f"\n{title}")
    if not items:
        print("  （无）")
        return
    for item in items:
        print(f"  - {item}")


def validate_html(path: Path) -> tuple[list[str], list[str], list[str]]:
    passed: list[str] = []
    warnings: list[str] = []
    failed: list[str] = []

    if path.exists():
        passed.append("文件存在")
    else:
        failed.append("文件不存在")
        return passed, warnings, failed

    if path.is_file():
        passed.append("路径指向普通文件")
    else:
        failed.append("路径不是普通文件")
        return passed, warnings, failed

    if path.suffix.lower() in {".html", ".htm"}:
        passed.append("文件扩展名为 HTML")
    else:
        failed.append("文件扩展名不是 .html 或 .htm")

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        failed.append("文件不是 UTF-8 编码，无法稳定读取")
        return passed, warnings, failed
    except OSError as exc:
        failed.append(f"文件读取失败：{exc}")
        return passed, warnings, failed

    if len(content.strip()) >= 200:
        passed.append("文件不是明显的空文件")
    else:
        failed.append("文件内容过少，疑似空文件或占位文件")

    parser = TagCollector()
    try:
        parser.feed(content)
        parser.close()
    except Exception as exc:  # HTMLParser normally tolerates malformed HTML.
        failed.append(f"HTML 标签解析失败：{exc}")

    required_tags = ("html", "head", "body")
    missing_tags = [tag for tag in required_tags if not has_tag(parser.tags, tag)]
    if not missing_tags:
        passed.append("包含 html、head、body 标签")
    else:
        failed.append(f"缺少必要标签：{', '.join(missing_tags)}")

    for tag in ("style", "script"):
        if has_tag(parser.tags, tag):
            passed.append(f"包含 {tag} 标签")
        else:
            failed.append(f"缺少 {tag} 标签")

    remote: list[str] = []
    local: list[str] = []

    def classify(value: str) -> None:
        candidate = value.strip()
        if not candidate or candidate.startswith("#") or candidate.startswith("data:"):
            return
        if re.match(r"(?:https?:)?//", candidate, flags=re.IGNORECASE):
            remote.append(candidate)
        else:
            local.append(candidate)

    for tag, name, value in parser.resources:
        values = [candidate.strip().split(" ")[0] for candidate in value.split(",")] if name == "srcset" else [value]
        for candidate in values:
            classify(candidate)

    style_blocks = re.findall(r"<style\b[^>]*>(.*?)</style\s*>", content, flags=re.IGNORECASE | re.DOTALL)
    for style_text in style_blocks + parser.style_values:
        for match in re.finditer(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", style_text, flags=re.IGNORECASE):
            classify(match.group(1))

    if remote:
        failed.append("发现远程资源引用：" + "；".join(sorted(set(remote))[:5]))
    elif local:
        failed.append("发现 HTML 未内联的本地资源（交付应为单文件）：" + "；".join(sorted(set(local))[:5]))
    else:
        passed.append("未发现远程或本地外部资源引用")

    layout_markers = (
        "app-shell",
        "prototype-pane",
        "requirements-pane",
        "grid-template-columns",
        "左右布局",
    )
    layout_hits = [marker for marker in layout_markers if marker in content]
    if len(layout_hits) >= 2:
        passed.append("包含左右布局相关结构")
    else:
        failed.append("未识别到足够的左右布局相关结构")

    target_keys = re.findall(r'\bdata-review-target\s*=\s*["\']([^"\']+)["\']', content)
    note_keys = set(re.findall(r'\bdata-review-note\s*=\s*["\']([^"\']+)["\']', content))
    if not target_keys or not note_keys or not re.search(r'<svg\b[^>]*\breview-overlay\b', content):
        failed.append("缺少编号旁注、区块锚点或 SVG 连线层")
    elif set(target_keys) != note_keys or len(target_keys) != len(set(target_keys)):
        failed.append("旁注与区块锚点不匹配，或区块锚点重复")
    else:
        passed.append("旁注与区块锚点匹配")

    requirement_markers = ("requirements-pane", "requirement-content", "需求说明")
    requirement_hits = [marker for marker in requirement_markers if marker in content]
    if len(requirement_hits) >= 2:
        passed.append("包含需求说明区域")
    else:
        failed.append("未识别到需求说明区域")

    interaction_patterns = (
        r"addEventListener\s*\(",
        r"onclick\s*=",
        r"function\s+[A-Za-z_$][\w$]*\s*\(",
    )
    interaction_hits = [pattern for pattern in interaction_patterns if re.search(pattern, content)]
    if len(interaction_hits) >= 1:
        passed.append("包含基础交互脚本")
    else:
        failed.append("未识别到基础交互脚本")

    if re.search(r"<!--\s*TEMPLATE_ANNOTATION_SCRIPT\s*-->", content, flags=re.IGNORECASE):
        failed.append("旁注脚本仍是占位注释，需替换为实际脚本")
    script_bodies = re.findall(r"<script\b([^>]*)>(.*?)</script\s*>", content, flags=re.IGNORECASE | re.DOTALL)
    inline_bodies = [body for attrs, body in script_bodies if not re.search(r"\bsrc\s*=", attrs, flags=re.IGNORECASE)]
    paints = [
        body
        for body in inline_bodies
        if "review-overlay" in body and ("createElementNS" in body or "getBoundingClientRect" in body)
    ]
    if paints:
        passed.append("包含内联旁注连线脚本")
    else:
        failed.append("缺少内联旁注连线脚本：页面只显示旁注卡片，不会绘制连线")

    if re.search(r"<form\b", content, flags=re.IGNORECASE):
        if re.search(r"bindDemoForm|preventDefault", content):
            passed.append("表单已阻止默认提交，可在受限预览中工作")
        else:
            warnings.append("表单未阻止默认提交，sandbox 未开启 allow-forms 时提交按钮会失效")

    duplicates = sorted(identifier for identifier, count in Counter(parser.ids).items() if count > 1)
    if duplicates:
        failed.append(f"存在重复 id：{', '.join(duplicates)}")
    else:
        passed.append("未发现重复 id")

    if not re.search(r"<meta\b[^>]+charset=", content, flags=re.IGNORECASE):
        warnings.append("未识别到 charset 声明")
    if not re.search(r"<meta\b[^>]+name=[\"']viewport[\"']", content, flags=re.IGNORECASE):
        warnings.append("未识别到 viewport 声明，桌面适配仍建议人工检查")
    if not re.search(r"<!doctype\s+html", content, flags=re.IGNORECASE):
        warnings.append("未识别到 HTML5 doctype")

    prototype_type = detect_prototype_type(content)
    if prototype_type == "APP/H5":
        app_checks = [
            ("包含手机外壳结构", re.search(r'class=["\'][^"\']*\bphone\b', content, flags=re.IGNORECASE)),
            ("包含手机屏幕结构", re.search(r'class=["\'][^"\']*\bscreen\b', content, flags=re.IGNORECASE)),
            ("包含移动端顶部导航", re.search(r"m-header", content, flags=re.IGNORECASE)),
            ("包含独立滚动内容区", re.search(r"m-list|overflow-y\s*:\s*auto", content, flags=re.IGNORECASE)),
            ("包含底部固定操作区", re.search(r"m-footer|btn-cta", content, flags=re.IGNORECASE)),
            ("包含页面状态预览", re.search(r"data-preview|gotoState|preview", content, flags=re.IGNORECASE)),
            ("包含文案编辑机制", re.search(r"data-k|contenteditable", content, flags=re.IGNORECASE)),
            ("包含 HTML 导出能力", re.search(r"exportHTML|outerHTML", content, flags=re.IGNORECASE)),
        ]
        for label, matched in app_checks:
            if matched:
                passed.append(label)
            else:
                failed.append(f"APP/H5 缺少{label[2:]}")

        collector_unclosed = getattr(parser, "open_tags", [])
        collector_mismatched = getattr(parser, "mismatched_end_tags", [])
        if collector_unclosed or collector_mismatched:
            detail = []
            if collector_unclosed:
                detail.append(f"未闭合 {', '.join(collector_unclosed[-8:])}")
            if collector_mismatched:
                detail.append(f"不匹配结束标签 {', '.join(collector_mismatched[-8:])}")
            failed.append("基础 HTML 标签结构异常：" + "；".join(detail))
        else:
            passed.append("基础 HTML 标签闭合检查通过")

        if re.search(r"<table\b", content, flags=re.IGNORECASE):
            warnings.append("APP/H5 中发现 table 标签，需确认没有把 Web 宽表格直接放入手机区域")
        else:
            passed.append("未发现 Web 宽表格直接放入手机原型的风险")
    elif prototype_type == "未知":
        warnings.append("无法自动判断原型类型，已仅执行通用 HTML 检查")

    if prototype_type != "APP/H5":
        collector_unclosed = getattr(parser, "open_tags", [])
        collector_mismatched = getattr(parser, "mismatched_end_tags", [])
        if collector_unclosed or collector_mismatched:
            detail = []
            if collector_unclosed:
                detail.append(f"未闭合 {', '.join(collector_unclosed[-8:])}")
            if collector_mismatched:
                detail.append(f"不匹配结束标签 {', '.join(collector_mismatched[-8:])}")
            warnings.append("基础 HTML 标签结构待确认：" + "；".join(detail))

    return passed, warnings, failed


def main() -> int:
    parser = argparse.ArgumentParser(description="检查离线需求原型 HTML 的基础结构和交互要素")
    parser.add_argument("html_file", help="待检查的 HTML 文件路径")
    args = parser.parse_args()

    path = Path(args.html_file).expanduser()
    print(f"HTML 校验：{path}")
    try:
        prototype_type = detect_prototype_type(path.read_text(encoding="utf-8")) if path.is_file() else "未知"
    except (OSError, UnicodeDecodeError):
        prototype_type = "未知"
    print(f"原型类型：{prototype_type}")
    passed, warnings, failed = validate_html(path)
    print_group("通过项", passed)
    print_group("警告项", warnings)
    print_group("失败项", failed)

    if failed:
        print("\n最终建议：暂不交付，请先修复失败项。")
        return 1
    print("\n最终建议：静态结构检查通过。仍需在浏览器中离线直开，并在 sandbox=\"allow-scripts\" 预览框内各测一次主操作（按钮点击与回车）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
