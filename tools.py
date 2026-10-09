"""tools.py - STUDENT IMPLEMENTS.  Source tools for the research agents.   Guide: GUIDE.md, part 1.

Rules for every tool:
  * runs on the HOST (not in the sandbox): API keys must never enter the sandbox;
  * returns a STRING (JSON text of compact records) and NEVER raises:
        "NO RESULTS"  when the source answers with nothing,
        "ERROR: ..."  when the source keeps failing after the retries (the agent then tries another source);
  * the docstring is the tool description the LLM reads: keep it precise (what it does, what it returns, when to use it).
Try your tools without any agent:   python tools.py
"""
import json
import os
import random
import re
import time
import xml.etree.ElementTree as ET

import httpx
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()  # so `python tools.py` also sees EXA_API_KEY

# ---- constants (given) ----
ARXIV_URL = "https://export.arxiv.org/api/query"  # https only: http answers 301
HF_DAILY_URL = "https://huggingface.co/api/daily_papers"
HF_SEARCH_URL = "https://huggingface.co/api/papers/search"
EXA_URL = "https://mcp.exa.ai/mcp"


class RetryableError(Exception):
    """Given. Raise it inside a call to ask with_retry to wait and try again (retry_after in seconds, optional)."""

    def __init__(self, message, retry_after=None):
        super().__init__(message)
        self.retry_after = retry_after


# ---- TODO 1: retry helper ----
def with_retry(fn, *, attempts=5, base=1.0, cap=30.0):
    """Call fn(); when it raises RetryableError, wait and call it again.

    Backoff is exponential (base * 2**attempt) capped at `cap`, plus jitter.
    Honors Retry-After when the server provides it. Never sleeps after the
    last attempt. Non-RetryableError exceptions propagate immediately.
    """
    for attempt in range(attempts):
        try:
            return fn()
        except RetryableError as e:
            if attempt >= attempts - 1:
                raise
            if e.retry_after is not None:
                try:
                    delay = float(e.retry_after)
                except (TypeError, ValueError):
                    delay = base * (2**attempt)
                else:
                    delay = min(delay, cap)
                    if delay < 0:
                        delay = 0.0
                time.sleep(delay)
            else:
                delay = min(base * (2**attempt), cap)
                delay = delay + random.uniform(0, 1.0)
                time.sleep(delay)


def _retry_after_from_headers(headers):
    try:
        raw = headers.get("Retry-After") or headers.get("retry-after")
    except Exception:
        return None
    if raw is None:
        return None
    raw = str(raw).strip()
    try:
        return float(raw)
    except ValueError:
        return None


def _raise_for_retryable(resp):
    if resp.status_code in (429, 500, 502, 503, 504):
        raise RetryableError(
            f"HTTP {resp.status_code} from {resp.request.url if hasattr(resp, 'request') else ''}",
            retry_after=_retry_after_from_headers(resp.headers),
        )


def _clean_ws(text, limit=600):
    collapsed = " ".join(str(text or "").split())
    if len(collapsed) > limit:
        return collapsed[:limit].rstrip() + "…"
    return collapsed


def _redact(text):
    key = os.getenv("EXA_API_KEY", "") or ""
    if key and key in text:
        return text.replace(key, "***")
    return text


_LAST_ARXIV_CALL = 0.0


def _arxiv_throttle():
    global _LAST_ARXIV_CALL
    now = time.monotonic()
    wait = 3.0 - (now - _LAST_ARXIV_CALL)
    if wait > 0:
        time.sleep(wait)
    _LAST_ARXIV_CALL = time.monotonic()


# ---- TODO 2: arXiv ----
@tool
def arxiv_search(query: str, max_results: int = 10) -> str:
    """Search arXiv papers by keywords, newest first. Returns a JSON list of {id, url, published, title, summary}."""
    try:
        terms = [t for t in re.findall(r"[\w\-]+", query or "", flags=re.UNICODE) if t]
        # drop bare boolean operators so stray AND/OR cannot break the query
        filtered = [t for t in terms if t.upper() not in {"AND", "OR", "NOT"}]
        if not filtered:
            return "NO RESULTS"
        try:
            m = int(max_results)
        except Exception:
            m = 10
        m = max(1, min(30, m))
        search_query = " AND ".join(f"all:{t}" for t in filtered)

        def _do():
            _arxiv_throttle()
            try:
                resp = httpx.get(
                    ARXIV_URL,
                    params={
                        "search_query": search_query,
                        "sortBy": "submittedDate",
                        "sortOrder": "descending",
                        "max_results": m,
                        "start": 0,
                    },
                    timeout=30.0,
                    follow_redirects=True,
                )
            except httpx.TransportError as e:
                raise RetryableError(f"arxiv transport: {e}")
            _raise_for_retryable(resp)
            return resp

        resp = with_retry(_do, attempts=6, base=2.0, cap=60.0)
        try:
            root = ET.fromstring(resp.text)
        except ET.ParseError as e:
            raise RetryableError(f"arxiv parse: {e}")

        ns = {"a": "http://www.w3.org/2005/Atom"}
        records = []
        for entry in root.findall("a:entry", ns):
            id_el = entry.find("a:id", ns)
            pub_el = entry.find("a:published", ns)
            title_el = entry.find("a:title", ns)
            sum_el = entry.find("a:summary", ns)
            if id_el is None or not (id_el.text or "").strip():
                continue
            raw_id = (id_el.text or "").strip()
            last = raw_id.rsplit("/", 1)[-1].strip()
            # strip version suffix vN
            clean_id = re.sub(r"v\d+$", "", last)
            # keep only plausible arxiv ids
            if not re.fullmatch(r"\d+\.\d+|[a-z\-]+/\d+", clean_id):
                # still allow it if it looks like an id, else skip
                if "/" not in clean_id and "." not in clean_id:
                    continue
            url = f"https://arxiv.org/abs/{clean_id}"
            published = (pub_el.text or "").strip()[:10] if pub_el is not None and pub_el.text else ""
            title = _clean_ws(title_el.text if title_el is not None and title_el.text else "", limit=300)
            summary = _clean_ws(sum_el.text if sum_el is not None and sum_el.text else "", limit=600)
            records.append(
                {"id": clean_id, "url": url, "published": published, "title": title, "summary": summary}
            )
        if not records:
            return "NO RESULTS"
        return json.dumps(records, ensure_ascii=False)
    except RetryableError as e:
        return f"ERROR: {type(e).__name__}: {e}"
    except Exception as e:  # noqa: BLE001 - tools never raise
        return f"ERROR: {type(e).__name__}: {e}"


# ---- TODO 3: Hugging Face ----
def _hf_record(item):
    paper = item.get("paper") or {}
    pid = paper.get("id") or item.get("id")
    if not pid:
        return None
    title = paper.get("title") or item.get("title") or ""
    summary = paper.get("ai_summary") or paper.get("summary") or item.get("summary") or ""
    published = paper.get("publishedAt") or item.get("publishedAt") or ""
    if isinstance(published, str):
        published = published[:10]
    else:
        published = ""
    try:
        upvotes = int(paper.get("upvotes", 0) or 0)
    except Exception:
        upvotes = 0
    github = paper.get("githubRepo") or ""
    try:
        stars = int(paper.get("githubStars", 0) or 0)
    except Exception:
        stars = 0
    return {
        "id": str(pid),
        "url": f"https://huggingface.co/papers/{pid}",
        "published": published,
        "title": _clean_ws(title, limit=300),
        "summary": _clean_ws(summary, limit=600),
        "upvotes": upvotes,
        "github": github or "",
        "stars": stars,
    }


@tool
def hf_daily_papers(limit: int = 30, date: str = "", keyword: str = "") -> str:
    """Hugging Face Daily Papers = what is trending in AI research. Returns a JSON list of
    {id, url, published, title, summary, upvotes, github, stars} sorted by upvotes. `date` is YYYY-MM-DD (empty = latest).
    `keyword` filters title/summary; there is no topic search on this endpoint (use hf_search_papers for a topic)."""
    try:
        try:
            lim = int(limit)
        except Exception:
            lim = 30
        lim = max(1, min(100, lim))
        params = {"limit": lim}
        if date and str(date).strip():
            params["date"] = str(date).strip()

        def _do():
            try:
                resp = httpx.get(HF_DAILY_URL, params=params, timeout=30.0, follow_redirects=True)
            except httpx.TransportError as e:
                raise RetryableError(f"hf-daily transport: {e}")
            _raise_for_retryable(resp)
            return resp

        resp = with_retry(_do, attempts=5, base=1.0, cap=30.0)
        try:
            data = resp.json()
        except Exception as e:
            raise RetryableError(f"hf-daily bad json: {e}")
        items = data if isinstance(data, list) else []
        records = []
        for it in items:
            if not isinstance(it, dict):
                continue
            rec = _hf_record(it)
            if rec:
                records.append(rec)
        kw = (keyword or "").strip().lower()
        if kw:
            records = [r for r in records if kw in ((r["title"] + " " + r["summary"]).lower())]
        records.sort(key=lambda r: r.get("upvotes", 0), reverse=True)
        if not records:
            return "NO RESULTS"
        return json.dumps(records, ensure_ascii=False)
    except RetryableError as e:
        return f"ERROR: {type(e).__name__}: {e}"
    except Exception as e:  # noqa: BLE001
        return f"ERROR: {type(e).__name__}: {e}"


@tool
def hf_search_papers(query: str, limit: int = 10) -> str:
    """Search Hugging Face papers by topic. Returns a JSON list of
    {id, url, published, title, summary, upvotes, github, stars}."""
    try:
        q = (query or "").strip()
        if not q:
            return "NO RESULTS"
        try:
            lim = int(limit)
        except Exception:
            lim = 10
        lim = max(1, min(50, lim))

        def _do():
            try:
                resp = httpx.get(
                    HF_SEARCH_URL, params={"q": q, "limit": lim}, timeout=30.0, follow_redirects=True
                )
            except httpx.TransportError as e:
                raise RetryableError(f"hf-search transport: {e}")
            _raise_for_retryable(resp)
            return resp

        resp = with_retry(_do, attempts=5, base=1.0, cap=30.0)
        try:
            data = resp.json()
        except Exception as e:
            raise RetryableError(f"hf-search bad json: {e}")
        items = data if isinstance(data, list) else []
        records = []
        for it in items:
            if not isinstance(it, dict):
                continue
            rec = _hf_record(it)
            if rec:
                records.append(rec)
        if not records:
            return "NO RESULTS"
        return json.dumps(records, ensure_ascii=False)
    except RetryableError as e:
        return f"ERROR: {type(e).__name__}: {e}"
    except Exception as e:  # noqa: BLE001
        return f"ERROR: {type(e).__name__}: {e}"


# ---- TODO 4: web search / fetch through the Exa MCP endpoint ----
def _exa_endpoint():
    key = (os.getenv("EXA_API_KEY") or "").strip()
    if key:
        # key goes in query string per GUIDE 1.4
        return f"{EXA_URL}?exaApiKey={key}"
    return EXA_URL


def _is_exa_rate_limited(result_obj, text):
    try:
        meta = result_obj.get("_meta") if isinstance(result_obj, dict) else None
    except Exception:
        meta = None
    if isinstance(meta, dict):
        for k, v in meta.items():
            kl = str(k).lower()
            if "rate" in kl or "limit" in kl or "quota" in kl or "429" in kl:
                if v is True or (isinstance(v, (int, float)) and v != 0) or (
                    isinstance(v, str) and v.strip() not in ("", "false", "False", "0")
                ):
                    return True
            if isinstance(v, str) and ("rate limit" in v.lower() or "too many requests" in v.lower()):
                return True
        # stringified meta check
        try:
            ms = json.dumps(meta).lower()
            if "rate limit" in ms and ("exceed" in ms or "too many" in ms or "retry" in ms or "quota" in ms):
                return True
        except Exception:
            pass
    tl = (text or "").lower()
    # text-level signal: free-tier limit notice (not a real page about rate limiting research)
    if "rate limit" in tl and any(
        s in tl for s in ["exceed", "too many requests", "try again", "retry", "quota", "upgrade", "per second", "/sec"]
    ):
        return True
    if "429" in tl and "exa" in tl:
        return True
    return False


def _exa_call(tool_name, arguments):
    def _do():
        url = _exa_endpoint()
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
        }
        try:
            resp = httpx.post(
                url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                },
                timeout=60.0,
            )
        except httpx.TransportError as e:
            raise RetryableError(_redact(f"exa transport: {e}"))
        if resp.status_code in (429, 500, 502, 503, 504):
            raise RetryableError(
                _redact(f"exa HTTP {resp.status_code}"),
                retry_after=_retry_after_from_headers(resp.headers),
            )
        # SSE: find data: lines
        texts = []
        result_obj = None
        try:
            body = resp.text
        except Exception as e:
            raise RetryableError(_redact(f"exa read body: {e}"))
        for line in body.splitlines():
            s = line.strip()
            if not s.startswith("data:"):
                continue
            data_part = s[len("data:"):].strip()
            if not data_part or data_part == "[DONE]":
                continue
            try:
                evt = json.loads(data_part)
            except Exception:
                continue
            # JSON-RPC response or notification
            if isinstance(evt, dict) and "result" in evt:
                result_obj = evt["result"]
                if isinstance(result_obj, dict) and "error" in result_obj and "content" not in result_obj:
                    # some servers nest error inside result
                    err = result_obj.get("error")
                    raise RetryableError(_redact(f"exa error: {err}"))
            if isinstance(evt, dict) and "error" in evt and "result" not in evt:
                raise RetryableError(_redact(f"exa json-rpc error: {evt['error']}"))
        if result_obj is None:
            # maybe plain JSON (not SSE)
            try:
                plain = json.loads(body)
                if isinstance(plain, dict) and "error" in plain and "result" not in plain:
                    raise RetryableError(_redact(f"exa json-rpc error: {plain['error']}"))
                if isinstance(plain, dict) and "result" in plain:
                    result_obj = plain["result"]
            except RetryableError:
                raise
            except Exception:
                pass
        if result_obj is None:
            raise RetryableError(_redact(f"exa empty response: {body[:200]}"))
        if isinstance(result_obj, dict) and "error" in result_obj and "content" not in result_obj:
            raise RetryableError(_redact(f"exa error: {result_obj['error']}"))
        # collect text parts
        content = result_obj.get("content", []) if isinstance(result_obj, dict) else []
        for part in content if isinstance(content, list) else []:
            if isinstance(part, dict) and part.get("type") == "text" and isinstance(part.get("text"), str):
                texts.append(part["text"])
        combined = "\n".join(texts).strip()
        if _is_exa_rate_limited(result_obj, combined):
            raise RetryableError(_redact("exa rate limited (free tier _meta flag); retry"))
        return combined

    return with_retry(_do, attempts=6, base=2.0, cap=60.0)


@tool
def web_search(query: str, objective: str = "", num_results: int = 5) -> str:
    """Search the web (Exa). Describe the ideal page in natural language. Returns clean text of the top results with URLs."""
    try:
        q = (query or "").strip()
        if not q:
            return "NO RESULTS"
        try:
            n = int(num_results)
        except Exception:
            n = 5
        n = max(1, min(10, n))
        obj = (objective or "").strip() or f"Find authoritative pages about: {q}"
        try:
            text = _exa_call("web_search_exa", {"query": q, "objective": obj, "numResults": n})
        except RetryableError as e:
            return _redact(f"ERROR: {type(e).__name__}: {e}")
        except Exception as e:  # noqa: BLE001
            return _redact(f"ERROR: {type(e).__name__}: {e}")
        if not text.strip():
            return "NO RESULTS"
        return text[:8000]
    except Exception as e:  # noqa: BLE001
        return _redact(f"ERROR: {type(e).__name__}: {e}")


@tool
def web_fetch(url: str) -> str:
    """Read the full content of one web page (e.g. an arXiv abstract page) as markdown. Long pages are truncated."""
    try:
        u = (url or "").strip()
        if not u or not (u.startswith("http://") or u.startswith("https://")):
            return "NO RESULTS"
        try:
            text = _exa_call("web_fetch_exa", {"urls": [u]})
        except RetryableError as e:
            return _redact(f"ERROR: {type(e).__name__}: {e}")
        except Exception as e:  # noqa: BLE001
            return _redact(f"ERROR: {type(e).__name__}: {e}")
        if not text.strip():
            return "NO RESULTS"
        return text[:12000]
    except Exception as e:  # noqa: BLE001
        return _redact(f"ERROR: {type(e).__name__}: {e}")


# ---- TODO 5: registry (the researcher subagent gets exactly these) ----
SOURCE_TOOLS = [arxiv_search, hf_daily_papers, hf_search_papers, web_search, web_fetch]


if __name__ == "__main__":
    for name, fn, args in [
        ("arxiv_search", arxiv_search, {"query": "world model", "max_results": 3}),
        ("hf_daily_papers", hf_daily_papers, {"limit": 20}),
        ("hf_search_papers", hf_search_papers, {"query": "world model", "limit": 3}),
        ("web_search", web_search, {"query": "survey paper on world models", "num_results": 2}),
        ("web_fetch", web_fetch, {"url": "https://arxiv.org/abs/1803.10122"}),
    ]:
        try:
            print(f"== {name}\n{fn.invoke(args)[:400]}\n")
        except NotImplementedError as exc:
            print(f"== {name}: not implemented yet ({exc})\n")
