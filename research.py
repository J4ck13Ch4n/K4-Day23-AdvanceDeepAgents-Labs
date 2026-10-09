"""research.py - STUDENT IMPLEMENTS.  The main script.   Guide: GUIDE.md, part 3.

Usage:  python research.py "survey about world model"
Result: reports/<slug>.md   reports/<slug>.sources.json   reports/<slug>.meta.json
"""
import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

from agents import FINALIZER_PATH, REPORT_PATH, SOURCES_PATH, VALIDATOR_PATH, WORKDIR, build_lead_agent
from model import make_model
from sandbox import download, open_sandbox, upload

ROOT = Path(__file__).parent
REPORTS = ROOT / "reports"
VALIDATOR_SOURCE = ROOT / "check_citations.py"
FINALIZER_SOURCE = ROOT / "finalize_citations.py"   # provided: uploaded next to your validator


def slugify(topic):
    """Turn a topic into a safe file name: lower case, runs of non-word characters become one "-", max 60 chars,
    never empty (fall back to "topic"). The topic is user input: "../../x" must not escape reports/."""
    text = (topic or "").strip().lower()
    if not text:
        return "topic"
    slug = re.sub(r"[^\w]+", "-", text, flags=re.UNICODE)
    slug = slug.strip("-")
    if len(slug) > 60:
        slug = slug[:60].strip("-")
    if not slug:
        return "topic"
    return slug


def build_prompt(topic):
    """The user message sent to the lead agent."""
    t = (topic or "").strip()
    return (
        f'Do a deep-research survey on the topic: "{t}".\n\n'
        "Follow your system-prompt workflow exactly: plan with write_todos into >=3 sub-questions, "
        "delegate to `researcher` subagents in parallel with full context (topic, sub-question, families, "
        "notes path, note format), verify their notes, merge into sources.json (cover >=3 source families), "
        f"write the report body to {REPORT_PATH} per REPORT_TEMPLATE.md (no ## References by hand), "
        "run the finalizer, run the validator until OK, and spot-check with `citation-checker`.\n"
        "Topic again (verbatim): " + t
    )


def _iter_tool_calls(messages):
    for m in messages or []:
        calls = None
        if isinstance(m, dict):
            calls = m.get("tool_calls") or m.get("toolCalls")
            # langchain messages sometimes nest under additional_kwargs
            if not calls and isinstance(m.get("additional_kwargs"), dict):
                calls = m["additional_kwargs"].get("tool_calls")
        else:
            calls = getattr(m, "tool_calls", None)
            if not calls:
                add = getattr(m, "additional_kwargs", None)
                if isinstance(add, dict):
                    calls = add.get("tool_calls")
        if not calls:
            continue
        for c in calls:
            name = None
            if isinstance(c, dict):
                name = c.get("name")
                if not name and isinstance(c.get("function"), dict):
                    fn = c["function"].get("name", "")
                    # openai format "functions.task" or "task"
                    name = fn.split(".")[-1] if fn else None
            else:
                name = getattr(c, "name", None)
                if not name and getattr(c, "function", None):
                    try:
                        fn = c.function.get("name", "") if isinstance(c.function, dict) else getattr(c.function, "name", "")
                        name = fn.split(".")[-1] if fn else None
                    except Exception:
                        name = None
            if name:
                yield name


def summarize(messages, elapsed, model_name):
    """Return {"model", "elapsed_s", "subagent_calls", "tool_calls": {name: count}, "tokens": {"input", "output"}}."""
    counter = Counter()
    subagent_calls = 0
    for name in _iter_tool_calls(messages):
        counter[name] += 1
        if name == "task":
            subagent_calls += 1
    in_tok = 0
    out_tok = 0
    for m in messages or []:
        usage = None
        if isinstance(m, dict):
            usage = m.get("usage_metadata") or m.get("usageMetadata")
            resp_meta = m.get("response_metadata")
            if usage is None and isinstance(resp_meta, dict):
                usage = resp_meta.get("usage") or resp_meta.get("token_usage")
        else:
            usage = getattr(m, "usage_metadata", None)
            if usage is None:
                resp_meta = getattr(m, "response_metadata", None)
                if isinstance(resp_meta, dict):
                    usage = resp_meta.get("token_usage") or resp_meta.get("usage")
        if not isinstance(usage, dict):
            continue
        try:
            in_tok += int(usage.get("input_tokens", 0) or 0)
            out_tok += int(usage.get("output_tokens", 0) or 0)
        except Exception:
            continue
    return {
        "model": model_name,
        "elapsed_s": round(float(elapsed), 1),
        "subagent_calls": subagent_calls,
        "tool_calls": dict(counter),
        "tokens": {"input": in_tok, "output": out_tok},
    }


MIN_BODY_WORDS = 1000
MIN_SOURCES = 6
_CANONICAL = {
    "arxiv": re.compile(r"^https://arxiv\.org/abs/[^/\s]+$"),
    "hf-daily": re.compile(r"^https://huggingface\.co/papers/[^/\s]+$"),
    "hf-search": re.compile(r"^https://huggingface\.co/papers/[^/\s]+$"),
}


def _quality_problems(report_text, sources):
    """Quality gate (reject only, never edits): enough substance and canonical URLs per family."""
    problems = []
    body = re.split(r"(?m)^##[ \t]+References[ \t]*$", report_text)[0]
    words = len(body.split())
    if words < MIN_BODY_WORDS:
        problems.append(f"body has {words} words (< {MIN_BODY_WORDS})")
    if len(sources) < MIN_SOURCES:
        problems.append(f"only {len(sources)} sources (< {MIN_SOURCES})")
    for s in sources:
        pattern = _CANONICAL.get(s.get("source"))
        if pattern and not pattern.match(str(s.get("url", ""))):
            problems.append(f"non-canonical {s.get('source')} url {s.get('url')}")
    return problems


def save_outputs(backend, topic, messages, elapsed, model_name, reports_dir=REPORTS):
    """Download the report from the sandbox and write the three files into reports_dir. Return the report path."""
    files = download(backend, [REPORT_PATH, SOURCES_PATH])
    report_bytes = files.get(REPORT_PATH)
    sources_bytes = files.get(SOURCES_PATH)
    if not report_bytes or not report_bytes.strip():
        raise RuntimeError("report.md missing or empty in sandbox")
    if not sources_bytes:
        raise RuntimeError("sources.json missing in sandbox")
    try:
        report_text = report_bytes.decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"sources/report decode failed: {e}")
    try:
        sources = json.loads(sources_bytes.decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"sources.json is not valid JSON: {e}")
    if not isinstance(sources, list) or len(sources) == 0:
        raise RuntimeError("sources.json is empty or not a list")
    # Host-side acceptance gate (no editing, only reject): the run is a failure unless the
    # downloaded report already passes our citation validator and covers >= 3 families.
    # A failed run must never overwrite good files, so raise BEFORE writing anything.
    try:
        sys.path.insert(0, str(ROOT))
        from check_citations import check as _validate
    except Exception as e:
        raise RuntimeError(f"cannot load validator: {e}")
    problems = _validate(report_text, sources)
    if problems:
        raise RuntimeError(f"citation check failed: {problems[0]}")
    families = sorted({str(s.get("source", "")) for s in sources if isinstance(s, dict) and s.get("source")})
    if len(set(families) & {"arxiv", "hf-daily", "hf-search", "web"}) < 3:
        raise RuntimeError(f"only {len(set(families) & {'arxiv', 'hf-daily', 'hf-search', 'web'})} source families: {families}")

    quality = _quality_problems(report_text, sources)
    if quality:
        raise RuntimeError(f"quality gate failed: {'; '.join(quality)}")

    slug = slugify(topic)
    reports_dir = Path(reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    summary = summarize(messages, elapsed, model_name)
    meta = {
        "topic": topic,
        "model": summary.get("model"),
        "elapsed_s": summary.get("elapsed_s"),
        "subagent_calls": summary.get("subagent_calls"),
        "tool_calls": summary.get("tool_calls"),
        "tokens": summary.get("tokens"),
        "n_sources": len(sources),
        "source_families": families,
    }
    (reports_dir / f"{slug}.sources.json").write_bytes(
        json.dumps(sources, ensure_ascii=False, indent=2).encode("utf-8")
    )
    (reports_dir / f"{slug}.meta.json").write_bytes(
        json.dumps(meta, ensure_ascii=False, indent=2).encode("utf-8")
    )
    (reports_dir / f"{slug}.md").write_bytes(report_text.encode("utf-8"))
    return reports_dir / f"{slug}.md"


def _model_name():
    return (os.getenv("LAB_MODEL") or os.getenv("OPENAI_DEPLOYMENT_MODEL") or "").strip()


def _patch_backend(backend, *, attempts=5, base=2.0, cap=30.0):
    """Wrap backend execute/upload/download with retry for flaky Daytona sessions.

    The Daytona API occasionally resets connections under rapid agent file ops
    ("Failed to create session"). Retrying here is safe: execute is idempotent
    enough for our file/script runs, and BaseSandbox implements ls/read/write
    on top of execute, so one wrapper covers almost everything.
    """
    import functools
    import random as _random

    def _is_transient(exc):
        name = type(exc).__name__
        msg = str(exc).lower()
        keys = (
            "connection reset",
            "connection aborted",
            "failed to create session",
            "read timed out",
            "timeout",
            "temporarily",
            "connection",
            "session",
            "503",
            "502",
            "504",
            "429",
        )
        return (
            "daytona" in name.lower()
            or "timeout" in name.lower()
            or "connection" in name.lower()
            or any(k in msg for k in keys)
        )

    def _wrap(fn):
        @functools.wraps(fn)
        def _inner(*args, **kwargs):
            last = None
            for attempt in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:  # noqa: BLE001
                    last = exc
                    if not _is_transient(exc) or attempt >= attempts - 1:
                        raise
                    time.sleep(min(base * (2**attempt), cap) + _random.uniform(0, 1.0))
            raise last  # pragma: no cover

        return _inner

    for meth in ("execute", "upload_files", "download_files", "aexecute", "aupload_files", "adownload_files"):
        if hasattr(backend, meth):
            try:
                setattr(backend, meth, _wrap(getattr(backend, meth)))
            except Exception:
                pass
    return backend


def main(topic):
    """Return the process exit code (0 ok, 1 failed run, 2 no topic)."""
    if not (topic or "").strip():
        print('Usage: python research.py "<topic>"', file=sys.stderr)
        return 2
    topic = topic.strip()
    try:
        model = make_model()
    except Exception as e:
        print(f"FAILED: cannot build model: {e}", file=sys.stderr)
        return 1
    model_name = _model_name()
    attempts = int(os.getenv("RESEARCH_ATTEMPTS", "3"))
    for attempt in range(1, attempts + 1):
        code = _run_once(topic, model, model_name)
        if code == 0:
            return 0
        print(f"attempt {attempt}/{attempts} failed", file=sys.stderr)
    return 1


def _run_once(topic, model, model_name):
    """One full run in a fresh sandbox. A rejected run never overwrites existing reports."""
    start = time.monotonic()
    try:
        with open_sandbox() as backend:
            _patch_backend(backend)
            backend.execute(f"mkdir -p {WORKDIR}/research/notes {WORKDIR}/report")
            upload(
                backend,
                {
                    VALIDATOR_PATH: VALIDATOR_SOURCE.read_bytes(),
                    FINALIZER_PATH: FINALIZER_SOURCE.read_bytes(),
                },
            )
            agent = build_lead_agent(backend, model)
            result = agent.invoke(
                {"messages": [{"role": "user", "content": build_prompt(topic)}]},
                config={"recursion_limit": 1000},
            )
            messages = result.get("messages", []) if isinstance(result, dict) else getattr(result, "messages", [])
            elapsed = time.monotonic() - start
            try:
                out = save_outputs(backend, topic, messages, elapsed, model_name)
            except RuntimeError as e:
                print(f"FAILED: {e}", file=sys.stderr)
                return 1
    except Exception as e:  # noqa: BLE001 - sandbox/agent errors become exit 1
        print(f"FAILED: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    print(f"saved report to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(" ".join(sys.argv[1:])))
