"""check_citations.py - STUDENT IMPLEMENTS `check`.   Runs INSIDE the sandbox (standard library only).

research.py uploads this file to the sandbox and the lead agent runs it with the `execute` tool:
    python3 /tmp/work/research/check_citations.py [report.md] [sources.json]
It must exit 0 and print "OK: ..." when the report is consistent, else print each problem and exit 1.
"""
import json
import os
import re
import sys

REPORT = "/tmp/work/report/report.md"
SOURCES = "/tmp/work/research/sources.json"

_REF_HEADING = re.compile(r"(?m)^##[ \t]+References[ \t]*$")
_CODE = re.compile(r"(```.*?```|`[^`\n]*`)", re.DOTALL)
# [3], [1, 2], [1-3], [1–3]; not a markdown link [3](url)
_GROUP = re.compile(r"\[(\d+(?:\s*[,–-]\s*\d+)*)\](?!\()")
_LINKDEF = re.compile(r"(?m)^[ \t]*\[\d+\][ \t]*:.*$")
_REF_LINE = re.compile(r"^\s*\[(\d+)\]\s*(.*)$")
_URL = re.compile(r"https?://\S+")


def _group_numbers(group):
    numbers = []
    for part in re.split(r"\s*,\s*", group):
        span = re.fullmatch(r"(\d+)\s*[–-]\s*(\d+)", part)
        if span:
            a, b = int(span.group(1)), int(span.group(2))
            if 0 <= b - a <= 200:
                numbers.extend(range(a, b + 1))
            else:
                numbers.extend([a, b])
        else:
            numbers.append(int(part))
    return numbers


def _strip_code(text):
    # odd indexes are code spans: drop them so [n] inside code is not counted
    parts = _CODE.split(text)
    return "".join(p for i, p in enumerate(parts) if i % 2 == 0)


def check(report_text, sources):
    """Return a list of problem strings (empty list = OK)."""
    problems = []
    if not isinstance(sources, list) or len(sources) == 0:
        return ["no sources in sources.json"]

    by_n = {}
    seen_n = set()
    seen_url = {}
    for entry in sources:
        if not isinstance(entry, dict):
            problems.append(f"source entry is not an object: {entry!r}")
            continue
        n = entry.get("n")
        url = entry.get("url")
        if not isinstance(n, int) or isinstance(n, bool):
            problems.append(f"source n={n!r} is not an int")
            continue
        if n in seen_n:
            problems.append(f"duplicate source number [{n}]")
        seen_n.add(n)
        by_n[n] = entry
        if not isinstance(url, str) or not (
            url.startswith("http://") or url.startswith("https://")
        ):
            problems.append(f"source [{n}] has bad url: {url!r}")
        else:
            norm = url.strip()
            if norm in seen_url:
                problems.append(
                    f"duplicate url {norm} in sources [{seen_url[norm]}] and [{n}]"
                )
            else:
                seen_url[norm] = n

    matches = list(_REF_HEADING.finditer(report_text or ""))
    if not matches:
        problems.append("missing ## References heading")
        body = report_text or ""
        ref_text = ""
    else:
        body = report_text[: matches[-1].start()]
        ref_text = report_text[matches[-1].end():]

    # citations in body only, code spans removed, markdown links excluded.
    # Reference-style link definitions ([1]: https://...) are NOT citations: drop those
    # lines first so a body of bare URL definitions cannot pass as cited.
    body_text = _LINKDEF.sub("", _strip_code(body))
    cited = set()
    for m in _GROUP.finditer(body_text):
        for num in _group_numbers(m.group(1)):
            cited.add(num)

    for n in sorted(cited):
        if n not in by_n:
            problems.append(f"[{n}] cited but missing from sources.json")
    for n in sorted(by_n):
        if n not in cited:
            problems.append(f"source [{n}] never cited")

    # reference lines: lines starting with [n]
    ref_lines = {}
    dup_ref = set()
    if matches:
        for line in ref_text.splitlines():
            m = _REF_LINE.match(line)
            if not m:
                continue
            num = int(m.group(1))
            rest = m.group(2)
            if num in ref_lines:
                dup_ref.add(num)
            ref_lines[num] = rest
        for n in sorted(by_n):
            if n not in ref_lines:
                problems.append(f"source [{n}] has no reference line")
        for num in sorted(ref_lines):
            if num not in by_n:
                problems.append(f"reference [{num}] is not a source in sources.json")
        for num in sorted(dup_ref):
            problems.append(f"reference [{num}] appears more than once")
        for num, rest in sorted(ref_lines.items()):
            if num not in by_n:
                continue
            urls = _URL.findall(rest)
            # strip trailing punctuation attached to URLs
            cleaned = [u.rstrip(").,;]") for u in urls]
            if len(cleaned) != 1:
                problems.append(
                    f"reference [{num}] must contain exactly one URL, found {len(cleaned)}"
                )
            elif cleaned[0] != by_n[num].get("url"):
                problems.append(
                    f"reference [{num}] URL mismatch: {cleaned[0]} != {by_n[num].get('url')}"
                )
    return problems


NOTES_DIR = "/tmp/work/research/notes"
MIN_WORDS = 1000
_NAME = re.compile(
    r"\b(?:[A-Z][a-z]+[A-Z]\w*|[A-Z][A-Za-z]*-[A-Z0-9]\w*|[A-Za-z]+-\d\w*|[A-Z]{4,}[A-Za-z0-9]*)\b"
)
_NUM = re.compile(r"\b\d[\d,.]*\d\b")
_CITE = re.compile(r"\[(\d+)\]")
_NOTE_URL = re.compile(r"(?mi)^\s*[-*]?\s*url:\s*(\S+)")
_COMMON = {"TL;DR", "NOTE"}


def _norm(text):
    return (text or "").lower().replace(",", "")


def _note_blocks(notes_text):
    """Map every url found in the notes to the text of its block ('## title' up to the next '## ')."""
    blocks = {}
    for chunk in re.split(r"(?m)^(?=##\s)", notes_text or ""):
        m = _NOTE_URL.search(chunk)
        if m:
            blocks[m.group(1).strip().rstrip(").,;")] = _norm(chunk)
    return blocks


def check_grounding(report_text, notes_text, sources=None):
    """Names and numbers in the report body must come from the researcher notes (no claims from memory).

    A sentence that cites [n] must find its names/numbers in the notes block of source n (url match), so a claim
    cannot borrow a fact from a different paper. Sentences without a citation are checked against all notes."""
    body = _REF_HEADING.split(report_text or "")[0]
    body = _LINKDEF.sub("", _strip_code(body))
    notes = _norm(notes_text)
    blocks = _note_blocks(notes_text)
    url_of = {s.get("n"): str(s.get("url", "")).strip() for s in (sources or []) if isinstance(s, dict)}
    problems = set()
    for line in body.splitlines():
        if line.lstrip().startswith("#"):
            continue
        for sent in re.split(r"(?<=[.!?])\s+", line):
            cited = [int(n) for n in _CITE.findall(sent)]
            clean = _GROUP.sub(" ", sent)
            scope = " ".join(blocks.get(url_of.get(n, ""), "") for n in cited).strip()
            where = "in the notes of the sources it cites" if scope else "in no researcher note"
            haystack = scope or notes
            for tok in _NAME.findall(clean) + _NUM.findall(clean):
                if re.fullmatch(r"(19|20)\d\d", tok) or tok in _COMMON:
                    continue
                if _norm(tok) not in haystack:
                    problems.add(f"'{tok}' appears {('with ' + ''.join(f'[{n}]' for n in cited)) if cited else ''} "
                                 f"but is not {where}: delete the claim or cite the source that states it")
    return sorted(problems)


TOPIC_PATH = "/tmp/work/topic.txt"
_STOP = {"survey", "about", "and", "for", "of", "the", "use", "with", "in", "on", "a", "an", "to"}


def check_relevance(notes_text, sources, topic):
    """Every source must match most of the topic's key terms in its own notes block (drops off-topic papers)."""
    terms = []
    for w in re.findall(r"[A-Za-z]+", topic or ""):
        w = w.lower()
        if w not in _STOP and w[:5] not in terms:
            terms.append(w[:5])
    if not terms:
        return []
    need = -(-2 * len(terms) // 3)  # ceil(2/3 * terms)
    blocks = _note_blocks(notes_text)
    problems = []
    for src in sources:
        text = blocks.get(str(src.get("url", "")).strip())
        if text is None:
            continue
        hit = sum(1 for t in terms if t in text)
        if hit < need:
            problems.append(f"source [{src.get('n')}] looks off-topic (matches {hit} of {len(terms)} topic terms): "
                            "remove it and every sentence that cites it")
    return problems


def _read_notes(notes_dir=NOTES_DIR):
    try:
        names = sorted(os.listdir(notes_dir))
    except OSError:
        return None
    parts = []
    for name in names:
        with open(os.path.join(notes_dir, name), encoding="utf-8", errors="ignore") as f:
            parts.append(f.read())
    return "\n".join(parts)


def main(argv):
    report_path = argv[1] if len(argv) > 1 else REPORT
    sources_path = argv[2] if len(argv) > 2 else SOURCES
    try:
        with open(report_path, encoding="utf-8") as f:
            report = f.read()
        with open(sources_path, encoding="utf-8") as f:
            sources = json.load(f)
    except (OSError, ValueError) as exc:
        print(f"cannot read inputs: {exc}")
        return 1
    problems = check(report, sources)
    notes = _read_notes() if len(argv) <= 1 else None  # grounding only in the sandbox run
    if notes:
        problems += check_grounding(report, notes, sources)
        try:
            with open(TOPIC_PATH, encoding="utf-8") as f:
                problems += check_relevance(notes, sources, f.read())
        except OSError:
            pass
        words = len(_REF_HEADING.split(report)[0].split())
        if words < MIN_WORDS:
            problems.append(f"report body has {words} words (< {MIN_WORDS}): add more comparisons and facts "
                            "stated in the notes of the cited sources, then re-run finalizer and validator")
    if problems:
        print("\n".join(problems))
        return 1
    print(f"OK: {len(sources)} sources, all citations resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
