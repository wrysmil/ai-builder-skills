#!/usr/bin/env python3
"""Validate the seven-section kickoff PRD and its traceability tables."""

import argparse
import json
import re
from pathlib import Path

SECTIONS = (
    '开工建议', '业务边界与现状', '证据与痛点', '一期范围与验收',
    '底座匹配与路径比较', '验证计划', '开工条件与待决事项',
)
SCHEMAS = {
    'E': (3, ('编号', '证据', '来源与局限')),
    'P': (3, ('编号', '痛点', '关联证据')),
    'C': (4, ('编号', '能力', '来源')),
    'R': (4, ('编号', '需求', '来源', '优先级', '状态')),
    'AC': (4, ('验收编号', '验收标准', '覆盖需求')),
    '覆盖矩阵': (4, ('需求编号', '验收编号', '验收状态')),
}
IDENTIFIER = re.compile(r'(?<![A-Za-z0-9_])(?:AC|[EPCR])[0-9]+(?![A-Za-z0-9_])')
DRAFT = '待确认'
INACTIVE = {'已作废', '已移出一期'}


def cells(line):
    return [part.strip().strip('`') for part in re.split(r'(?<!\\)\|', line.strip().strip('|'))]


def scan(text):
    sections, tables = [], {}
    section = 0
    fence = None
    header = None
    kind = None
    for line in text.splitlines():
        stripped = line.strip()
        marker = re.match(r'(`{3,}|~{3,})', stripped)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and stripped == token:
                fence = None
            header = kind = None
            continue
        if fence:
            continue
        heading = re.fullmatch(r'##\s+([1-7])[.、]\s*(.+)', stripped)
        if heading:
            section = int(heading[1])
            sections.append((section, heading[2].strip(' 🧭🔎🧪')))
        if not stripped.startswith('|'):
            header = kind = None
            continue
        row = cells(stripped)
        match = next((key for key, (at, fields) in SCHEMAS.items() if at == section and set(fields) <= set(row)), None)
        if match:
            kind, header = match, row
            tables.setdefault(kind, [])
        elif kind and not all(re.fullmatch(r':?-{3,}:?', cell) for cell in row):
            tables[kind].append(dict(zip(header, row)))
    return sections, tables


def check(text):
    sections, tables = scan(text)
    issues = []
    expected_sections = list(enumerate(SECTIONS, 1))
    if sections != expected_sections:
        expected_headings = '、'.join(f'「{number}. {title}」' for number, title in expected_sections)
        issues.append(f'七节标题缺失、重复或顺序不符。二级标题依次应为 {expected_headings}。')
    for kind in ('R', 'AC', '覆盖矩阵'):
        if kind not in tables:
            issues.append(f'缺少 {kind} 表。')
    rows = {}
    for kind, entries in tables.items():
        key = '需求编号' if kind == '覆盖矩阵' else '验收编号' if kind == 'AC' else '编号'
        prefix = 'R' if kind == '覆盖矩阵' else kind
        indexed = rows[kind] = {}
        for row in entries:
            label = row.get(key, '')
            if not re.fullmatch(rf'{prefix}[1-9][0-9]*', label):
                issues.append(f'{kind} 表编号无效：{label or "空白"}。请使用 {prefix}1 这类无前导零的编号。')
            elif label in indexed:
                issues.append(f'{kind} 表编号重复：{label}')
            else:
                indexed[label] = row
    sources = {}
    for kind, field, allowed in (('P', '关联证据', 'E'), ('C', '来源', 'EP'), ('R', '来源', 'EPC')):
        for label, row in rows.get(kind, {}).items():
            links = set(IDENTIFIER.findall(row.get(field, '')))
            for link in sorted(links):
                if link[0] not in allowed or link not in rows.get(link[0], {}):
                    issues.append(f'{label} 的来源 {link} 未定义或类型不符。')
            sources[label] = links

    def reaches_evidence(label):
        if label.startswith('E'):
            return label in rows.get('E', {})
        return any(reaches_evidence(link) for link in sources.get(label, ()) if link[0] + label[0] in ('EP', 'EC', 'PC', 'ER', 'PR', 'CR'))

    requirements = rows.get('R', {})
    if not requirements:
        issues.append('缺少有效的 R 需求。')
    coverage = {label: set() for label in requirements}
    for label, row in rows.get('AC', {}).items():
        links = set(IDENTIFIER.findall(row.get('覆盖需求', '')))
        if not links:
            issues.append(f'{label} 没有对应需求。')
        if not row.get('验收标准', '').strip():
            issues.append(f'{label} 缺少验收标准。')
        for link in sorted(links):
            if link in coverage:
                coverage[link].add(label)
            else:
                issues.append(f'{label} 引用了不存在的需求 {link}。')
    matrix = rows.get('覆盖矩阵', {})
    for label in matrix.keys() - requirements.keys():
        issues.append(f'覆盖矩阵引用了不存在的需求 {label}。')
    for label, row in requirements.items():
        status = row.get('状态', '')
        if not status or not row.get('需求', '') or not row.get('优先级', ''):
            issues.append(f'{label} 的需求、优先级或状态缺失。')
        if status not in INACTIVE and status != DRAFT and not reaches_evidence(label):
            issues.append(f'{label} 无法追溯到证据或用户确认的约束。')
        if label not in matrix:
            if status not in INACTIVE:
                issues.append(f'{label} 缺少覆盖矩阵行。')
            continue
        actual = set(IDENTIFIER.findall(matrix[label].get('验收编号', '')))
        expected = coverage[label]
        if actual != expected:
            issues.append(f'{label} 的矩阵应为 {", ".join(sorted(expected)) or "空白"}。')
        if not expected and status not in INACTIVE:
            if status != DRAFT or matrix[label].get('验收状态') != '待补':
                issues.append(f'{label} 缺少验收标准，待确认草稿可在矩阵标「待补」。')
    return issues, {name: len(entries) for name, entries in rows.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        issues, counts = check(args.path.read_text(encoding='utf-8-sig'))
    except (OSError, UnicodeError) as error:
        parser.exit(2, f'{error}\n')
    if args.json:
        print(json.dumps({'ok': not issues, 'issues': issues, 'counts': counts}, ensure_ascii=False))
    elif issues:
        print('\n'.join(issues))
    else:
        print('七节结构、来源编号与双向验收覆盖检查通过。')
    return int(bool(issues))


if __name__ == '__main__':
    raise SystemExit(main())
