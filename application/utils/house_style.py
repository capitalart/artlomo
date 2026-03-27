from __future__ import annotations
import json, re
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

CONFIG_PATH = "utils/house_style_config.json"

def load_config(path: str = CONFIG_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@dataclass
class Section:
    heading: str
    text: str

def split_into_sections(full_text: str, expected_headings: List[str]) -> List[Section]:
    lines = full_text.replace("\r\n","\n").split("\n")
    sections: List[Section] = []
    current_h = None
    buf: List[str] = []
    def flush():
        nonlocal sections, current_h, buf
        if current_h is not None:
            sections.append(Section(current_h, "\n".join(buf).strip()))
        buf = []
    for line in lines:
        if line.strip() in expected_headings:
            flush(); current_h = line.strip()
        else:
            buf.append(line)
    flush()
    return sections

def word_count(s: str) -> int:
    return len([w for w in re.findall(r"\b[\w’'-]+\b", s)])

def contains_forbidden(text: str, patterns: List[re.Pattern]) -> Optional[str]:
    for p in patterns:
        if p.search(text):
            return p.pattern
    return None

def validate_full_text(text: str, cfg: dict) -> Dict:
    errors: List[str] = []
    warn: List[str] = []
    allowed_emojis = cfg.get("allowedEmojis", [])
    forb_url = re.compile(cfg.get("forbiddenUrlsRegex", ""), re.I) if cfg.get("forbiddenUrlsRegex") else None
    forb_email = re.compile(cfg.get("forbiddenEmailRegex",""), re.I) if cfg.get("forbiddenEmailRegex") else None
    forb_phone = re.compile(cfg.get("forbiddenPhoneRegex",""), re.I) if cfg.get("forbiddenPhoneRegex") else None
    forb = [p for p in [forb_url, forb_email, forb_phone] if p]

    headings = [s["heading"] for s in cfg["sections"]]
    text_norm = text.replace("❓ Frequently Asked Questions", "Frequently Asked Questions")
    sections = split_into_sections(text_norm, headings)
    found_headings = [s.heading for s in sections]
    missing = []
    for s in cfg["sections"]:
        if s.get("optional"): continue
        if s["heading"] not in found_headings:
            missing.append(s["heading"])
    if missing:
        errors.append(f"Missing required sections: {', '.join(missing)}")

    h2sec = {s.heading: s for s in sections}
    for sdef in cfg["sections"]:
        if sdef.get("optional") and sdef["heading"] not in h2sec: continue
        sec = h2sec.get(sdef["heading"])
        if not sec: continue
        txt = sec.text.strip()
        if sdef.get("minWords") and word_count(txt) < sdef["minWords"]:
            errors.append(f"Section '{sdef['heading']}' too short.")
        if sdef.get("maxWords") and word_count(txt) > sdef["maxWords"]:
            warn.append(f"Section '{sdef['heading']}' long; consider tightening.")
        if sdef.get("minLines"):
            if len([l for l in txt.split("\n") if l.strip()]) < sdef["minLines"]:
                errors.append(f"Section '{sdef['heading']}' must contain at least {sdef['minLines']} lines.")
        if sdef.get("minBullets"):
            bullets = [l for l in txt.split("\n") if l.strip().startswith("*")]
            if len(bullets) < sdef["minBullets"]:
                errors.append(f"Section '{sdef['heading']}' needs at least {sdef['minBullets']} bullets.")
            if sdef.get("bulletStartsWith"):
                for b in bullets:
                    if not b.lstrip("* ").startswith(sdef["bulletStartsWith"]):
                        errors.append(f"Section '{sdef['heading']}' bullets must start with {sdef['bulletStartsWith']}.")
        if sdef.get("stepsRequired"):
            for step in sdef["stepsRequired"]:
                if step not in txt: errors.append(f"Section '{sdef['heading']}' missing step {step}.")
        if sdef.get("faqRequired"):
            for q in sdef["faqRequired"]:
                if q.split("?")[0].strip() not in txt:
                    errors.append(f"FAQ missing question about: {q}")
        for phrase in sdef.get("mustMention", []):
            if phrase not in txt: errors.append(f"Section '{sdef['heading']}' must mention: {phrase}")
        for phrase in sdef.get("require", []):
            if phrase not in txt: errors.append(f"Section '{sdef['heading']}' must contain phrase: {phrase}")
        if sdef.get("requireAny") and not any(p in txt for p in sdef["requireAny"]):
            errors.append(f"Section '{sdef['heading']}' must contain one of: {', '.join(sdef['requireAny'])}")
        if sdef.get("requireSomeOf"):
            for group in sdef["requireSomeOf"]:
                if not any(p in txt for p in group):
                    errors.append(f"Section '{sdef['heading']}' must contain at least one of: {', '.join(group)}")
        if sdef.get("numbers"):
            n = sdef["numbers"]
            reqs = [str(int(n["pixelWidth"])), str(int(n["pixelHeight"])), f"{n['sizes'][0]}"]
            if not all(req in txt for req in reqs):
                errors.append(f"Section '{sdef['heading']}' must include pixel dims and sizes list.")
            if f"{n['maxPrintInches'][0]}" not in txt or f"{n['maxPrintInches'][1]}" not in txt:
                errors.append(f"Section '{sdef['heading']}' must include max print inches.")
        if sdef.get("etsyLinkRequired"):
            if "etsy.com" not in txt:
                errors.append(f"Section '{sdef['heading']}' must include Etsy link.")
            if forb_url and forb_url.search(txt):
                errors.append(f"Section '{sdef['heading']}' contains non-Etsy URL.")
        ep = sdef.get("emojiPolicy", {"maxInSection": 0})
        used = [ch for ch in sec.text if ch in "".join(allowed_emojis)]
        if len(used) > ep.get("maxInSection", 0):
            errors.append(f"Section '{sdef['heading']}' uses too many emojis.")
        if ep.get("allowed"):
            for ch in used:
                if ch not in ep["allowed"]:
                    errors.append(f"Section '{sdef['heading']}' uses disallowed emoji '{ch}'.")

    if forb:
        bad = contains_forbidden(text, forb)
        if bad: errors.append("Output contains forbidden contact/URL patterns.")

    # literal Etsy URL / markdown restrictions
    etsy_literal = cfg.get("etsyUrlLiteral", "")
    literal_re = re.compile(cfg.get("literalEtsyUrlRegex","")) if cfg.get("literalEtsyUrlRegex") else None
    forbid_md = cfg.get("forbidMarkdownLinks", True)
    if forbid_md:
        if re.search(r"\[[^\]]+\]\([^)]+\)", text):
            errors.append("Output contains a markdown link. Print the full URL literally instead.")
        if re.search(r"<a\s+[^>]*>", text, flags=re.I):
            errors.append("Output contains an HTML link. Print the full URL literally instead.")
    cta_name = "🚀 Explore My Work"
    cta_sec = next((s for s in sections if s.heading == cta_name), None)
    if cta_sec:
        cta_txt = cta_sec.text
        if etsy_literal and etsy_literal not in cta_txt:
            errors.append(f"Section '{cta_name}' must include the full literal Etsy URL: {etsy_literal}")
        if literal_re and not literal_re.search(cta_txt):
            errors.append(f"Section '{cta_name}' must show the Etsy URL with 'https://' and no modifications.")
        if re.search(r"(?<!https?://)\\brobincustance\.etsy\.com\\b", cta_txt):
            errors.append(f"Section '{cta_name}' must include 'https://' before the Etsy URL.")

    return {"ok": not errors, "errors": errors, "warnings": warn}
