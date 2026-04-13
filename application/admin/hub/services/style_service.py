from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json
from ....common.utilities.files import ensure_dir, write_json_atomic


DEFAULTS = {
    "primary_color": "#2e4057",
    "secondary_color": "#8ca0b3",
    "accent_color": "#1A1A1A",
    "background_color": "#f8f9fb",
    "card_background": "#ffffff",
    "text_color": "#1f2a36",
    "text_secondary": "#666666",
    "font_family": "'Outfit', sans-serif",
    "font_heading": "'Outfit', sans-serif",
    "base_font_size": "16px",
    "card_radius": "12px",
    "border_color": "#E5E5E5",
    "border_width": "1px",
    "grid_gap": "3rem",
    "letter_spacing_heading": "0.02em",
    "button_padding": "12px 24px",
    "artlomo_btn_text": "#333333",
    "artlomo_btn_bg": "transparent",
    "artlomo_btn_shadow": "4px 4px 0px rgba(0, 0, 0, 0.1)",
    "artlomo_btn_hover_bg": "#1A1A1A",
    "artlomo_btn_hover_text": "#ffffff",
    "artlomo_save_bg": "#1A1A1A",
    "artlomo_save_text": "#ffffff",
    "artlomo_danger": "#c8252d",
    "danger_color": "#c8252d",
    "artlomo_lock_border_light": "rgba(0, 0, 0, 0.55)",
    "artlomo_lock_border_dark": "rgba(255, 255, 255, 0.55)",
}


class StyleService:
    def __init__(self, themes_dir: Path, generated_css_path: Path) -> None:
        self.themes_root = themes_dir
        self.system_dir = themes_dir / "system"
        self.user_dir = themes_dir / "user"
        self.active_path = self.user_dir / "current_style.json"
        self.generated_css_path = generated_css_path
        self.presets_css_dir = self.generated_css_path.parent / "presets"
        ensure_dir(self.system_dir)
        ensure_dir(self.user_dir)
        ensure_dir(self.generated_css_path.parent)
        ensure_dir(self.presets_css_dir)
        self._migrate_legacy_default()
        self._migrate_flat_presets_to_twin()
        self._ensure_active_css()

    def _ensure_active_css(self) -> None:
        if not self.active_path.exists():
            return
        try:
            raw = self._load_json(self.active_path)
            if isinstance(raw, dict):
                self._write_css(raw)
        except Exception:
            return

    def _migrate_legacy_default(self) -> None:
        legacy_default = self.themes_root / "default.json"
        if self.active_path.exists() or (not legacy_default.exists()):
            return
        try:
            raw = json.loads(legacy_default.read_text(encoding="utf-8"))
            if not isinstance(raw, dict):
                return
            merged = self._merged(raw)
            merged["name"] = str(raw.get("name") or "default").strip() or "default"
            merged["folder"] = "user"
            merged["saved_at"] = raw.get("saved_at") or datetime.now(timezone.utc).isoformat()
            write_json_atomic(self.active_path, merged)
        except Exception:
            return

    def list_presets(self) -> dict[str, list[str]]:
        root: list[str] = []
        for p in self.themes_root.glob("*.json"):
            root.append(p.stem)
        system = sorted([p.stem for p in self.system_dir.glob("*.json")])
        user: list[str] = []
        for p in self.user_dir.glob("*.json"):
            if p.stem in {"current_style", "original_look_backup"}:
                continue
            user.append(p.stem)
        return {"Root": sorted(set(root)), "System": system, "User": sorted(user)}

    def load_preset(self, name: str, *, folder: str | None = None) -> dict[str, Any]:
        preset_name = (name or "").strip()
        if not preset_name:
            raise FileNotFoundError("Preset name is required")

        search: list[tuple[str, Path]]
        if folder == "root":
            search = [("root", self.themes_root)]
        elif folder == "system":
            search = [("system", self.system_dir)]
        elif folder == "user":
            search = [("user", self.user_dir)]
        else:
            search = [("root", self.themes_root), ("system", self.system_dir), ("user", self.user_dir)]

        for f, base in search:
            path = base / f"{preset_name}.json"
            if not path.exists():
                continue
            raw = self._load_json(path)
            if not isinstance(raw, dict):
                raw = {}

            saved_at = raw.get("saved_at")
            custom_css = raw.get("custom_css") if isinstance(raw.get("custom_css"), str) else ""

            light_raw = raw.get("light") if isinstance(raw.get("light"), dict) else None
            dark_raw = raw.get("dark") if isinstance(raw.get("dark"), dict) else None
            if light_raw is None and dark_raw is None:
                merged = self._merged(raw)
                if merged.get("danger_color") is None and merged.get("artlomo_danger"):
                    danger_val = merged.get("artlomo_danger")
                    if danger_val is not None:
                        merged["danger_color"] = danger_val
                twin = self._as_twin(preset_name, folder=f, saved_at=saved_at, light_values=merged)
                if custom_css:
                    twin["custom_css"] = custom_css
                return twin

            if light_raw is not None or dark_raw is not None:
                base_values = {k: v for k, v in raw.items() if k in DEFAULTS}
                light_vals = self._merged({**base_values, **(light_raw or {})})
                dark_vals = self._merged({**base_values, **(dark_raw or {})})
                if light_vals.get("danger_color") is None and light_vals.get("artlomo_danger"):
                    light_danger = light_vals.get("artlomo_danger")
                    if light_danger is not None:
                        light_vals["danger_color"] = light_danger
                if dark_vals.get("danger_color") is None and dark_vals.get("artlomo_danger"):
                    dark_danger = dark_vals.get("artlomo_danger")
                    if dark_danger is not None:
                        dark_vals["danger_color"] = dark_danger
                out = {
                    "name": preset_name,
                    "folder": f,
                    "saved_at": saved_at,
                    "light": light_vals,
                    "dark": dark_vals,
                }
                if custom_css:
                    out["custom_css"] = custom_css
                return out

        raise FileNotFoundError(f"Preset not found: {preset_name}")

    def apply_preset(self, folder: str, name: str) -> dict[str, Any]:
        preset = self.load_preset(name, folder=folder)
        self._write_css(preset)
        write_json_atomic(self.active_path, preset)
        return preset

    def save_root_preset(self, name: str, values: dict[str, str], *, mode: str = "save") -> Path:
        preset_name = self._sanitize_name(name)
        if not preset_name:
            raise ValueError("Preset name is required")
        if preset_name == "default":
            raise ValueError("Cannot overwrite default")

        json_path = self.themes_root / f"{preset_name}.json"

        if mode == "copy" and json_path.exists():
            base = preset_name
            i = 2
            while (self.themes_root / f"{base}_{i}.json").exists():
                i += 1
            preset_name = f"{base}_{i}"
            json_path = self.themes_root / f"{preset_name}.json"

        saved_at = datetime.now(timezone.utc).isoformat()
        merged = self._merged(values)
        if merged.get("danger_color") is None and merged.get("artlomo_danger"):
            danger_val = merged.get("artlomo_danger")
            if danger_val is not None:
                merged["danger_color"] = danger_val
        twin = self._as_twin(preset_name, folder="root", saved_at=saved_at, light_values=merged)

        write_json_atomic(json_path, twin)
        self._write_css(twin)
        write_json_atomic(self.active_path, twin)
        return json_path

    def save_root_preset_twin(
        self,
        name: str,
        *,
        light: dict[str, str],
        dark: dict[str, str],
        custom_css: str = "",
        mode: str = "save",
    ) -> Path:
        preset_name = self._sanitize_name(name)
        if not preset_name:
            raise ValueError("Preset name is required")
        if preset_name == "default":
            raise ValueError("Cannot overwrite default")

        json_path = self.themes_root / f"{preset_name}.json"

        if mode == "copy" and json_path.exists():
            base = preset_name
            i = 2
            while (self.themes_root / f"{base}_{i}.json").exists():
                i += 1
            preset_name = f"{base}_{i}"
            json_path = self.themes_root / f"{preset_name}.json"

        saved_at = datetime.now(timezone.utc).isoformat()
        light_vals = self._merged(light or {})
        dark_vals = self._merged(dark or {})
        if light_vals.get("danger_color") is None and light_vals.get("artlomo_danger"):
            light_danger = light_vals.get("artlomo_danger")
            if light_danger is not None:
                light_vals["danger_color"] = light_danger
        if dark_vals.get("danger_color") is None and dark_vals.get("artlomo_danger"):
            dark_danger = dark_vals.get("artlomo_danger")
            if dark_danger is not None:
                dark_vals["danger_color"] = dark_danger

        twin = {
            "name": preset_name,
            "folder": "root",
            "saved_at": saved_at,
            "light": light_vals,
            "dark": dark_vals,
        }

        if custom_css:
            twin["custom_css"] = custom_css

        write_json_atomic(json_path, twin)
        self._write_css(twin)
        write_json_atomic(self.active_path, twin)
        return json_path

    def save_preset(self, name: str, values: dict[str, str]) -> Path:
        preset_name = self._sanitize_name(name)
        if not preset_name:
            raise ValueError("Preset name is required")

        system_names = set(self.list_presets().get("System") or [])
        if preset_name in system_names:
            base = preset_name
            preset_name = f"{base}-custom"
            i = 2
            while preset_name in system_names:
                preset_name = f"{base}-custom-{i}"
                i += 1

        return self.save_theme({"name": preset_name, "values": values})

    def _sanitize_name(self, raw: str) -> str:
        txt = (raw or "").strip().lower()
        if not txt:
            return ""
        out: list[str] = []
        for ch in txt:
            if ch.isalnum() or ch in {"-", "_"}:
                out.append(ch)
            elif ch.isspace():
                out.append("-")
        clean = "".join(out).strip("-")
        while "--" in clean:
            clean = clean.replace("--", "-")
        return clean

    def parse_form(self, form: Any) -> dict[str, Any]:
        name = (getattr(form, "get", lambda k, d=None: d)("theme_name") or "default").strip() or "default"
        values: dict[str, str] = {}
        for key in DEFAULTS:
            raw = getattr(form, "get", lambda k, d=None: d)(key)
            if raw:
                values[key] = raw
        return {"name": name, "values": values}

    def save_theme(self, payload: Any = None, *, name: str | None = None, values: dict[str, str] | None = None) -> Path:
        if isinstance(payload, dict):
            name = (payload.get("name") or name or "default").strip() or "default"
            values = payload.get("values") or values or {}
        else:
            name = (name or "default").strip() or "default"
            values = values or {}

        preset_name = self._sanitize_name(name) or "default"
        system_names = set(self.list_presets().get("System") or [])
        if preset_name in system_names:
            preset_name = f"{preset_name}-custom"

        saved_at = datetime.now(timezone.utc).isoformat()
        merged = self._merged(values)
        if merged.get("danger_color") is None and merged.get("artlomo_danger"):
            danger_val = merged.get("artlomo_danger")
            if danger_val is not None:
                merged["danger_color"] = danger_val
        twin = self._as_twin(preset_name, folder="user", saved_at=saved_at, light_values=merged)

        json_path = self.user_dir / f"{preset_name}.json"
        write_json_atomic(json_path, twin)
        self._write_css(twin)
        write_json_atomic(self.active_path, twin)
        return json_path

    def restore_defaults(self) -> Path:
        return self.save_theme({"name": "default", "values": {}})

    def delete_preset(self, folder: str, name: str) -> dict[str, Any]:
        folder = (folder or "").strip().lower()
        preset_name = self._sanitize_name(name)
        if folder not in {"user", "root"}:
            raise ValueError("Only user or root presets can be deleted")
        if not preset_name or preset_name == "default":
            raise ValueError("Preset cannot be deleted")

        base_dir = self.user_dir if folder == "user" else self.themes_root
        json_path = base_dir / f"{preset_name}.json"
        if not json_path.exists():
            raise FileNotFoundError("Preset not found")

        # If deleting the active preset, revert to defaults.
        active = self.current_preset()
        active_name = str(active.get("name") or "").strip().lower()
        active_folder = str(active.get("folder") or "").strip().lower()

        json_path.unlink(missing_ok=True)
        css_path = self.presets_css_dir / f"{preset_name}.css"
        css_path.unlink(missing_ok=True)

        if active_name == preset_name and active_folder == folder:
            self.restore_defaults()

        return self.current_preset()

    def _merged(self, values: dict[str, str]) -> dict[str, str]:
        merged = DEFAULTS.copy()
        for key, default_value in DEFAULTS.items():
            if values.get(key):
                merged[key] = values[key]
            else:
                merged[key] = default_value
        return merged

    def _derive_dark(self, light_values: dict[str, str]) -> dict[str, str]:
        merged = self._merged(light_values)
        merged.update(
            {
                "background_color": "#0b0b0b",
                "card_background": "#0f0f0f",
                "text_color": "#f2f2f2",
                "text_secondary": "#b3b3b3",
                "border_color": "#2b2b2b",
            }
        )
        if merged.get("danger_color") is None and merged.get("artlomo_danger"):
            danger_val = merged.get("artlomo_danger")
            if danger_val is not None:
                merged["danger_color"] = danger_val
        return merged

    def _as_twin(self, name: str, *, folder: str, saved_at: Any, light_values: dict[str, str]) -> dict[str, Any]:
        light_vals = self._merged(light_values)
        dark_vals = self._derive_dark(light_vals)
        return {
            "name": name,
            "folder": folder,
            "saved_at": saved_at,
            "light": light_vals,
            "dark": dark_vals,
        }

    def _migrate_flat_presets_to_twin(self) -> None:
        def _iter_paths() -> list[tuple[str, Path]]:
            out: list[tuple[str, Path]] = []
            for p in self.themes_root.glob("*.json"):
                out.append(("root", p))
            for p in self.system_dir.glob("*.json"):
                out.append(("system", p))
            for p in self.user_dir.glob("*.json"):
                out.append(("user", p))
            return out

        for folder, path in _iter_paths():
            try:
                raw = self._load_json(path)
            except Exception:
                continue
            if not isinstance(raw, dict):
                continue
            if isinstance(raw.get("light"), dict) or isinstance(raw.get("dark"), dict):
                continue

            preset_name = str(raw.get("name") or path.stem).strip() or path.stem
            saved_at = raw.get("saved_at")
            merged = self._merged(raw)
            if merged.get("danger_color") is None and merged.get("artlomo_danger"):
                danger_val = merged.get("artlomo_danger")
                if danger_val is not None:
                    merged["danger_color"] = danger_val
            twin = self._as_twin(preset_name, folder=folder, saved_at=saved_at, light_values=merged)
            try:
                write_json_atomic(path, twin)
            except Exception:
                continue

    def _write_css(self, payload: dict[str, str]) -> None:

        def _resolved(theme_key: str) -> dict[str, str]:
            light_raw = payload.get("light") if isinstance(payload.get("light"), dict) else None
            dark_raw = payload.get("dark") if isinstance(payload.get("dark"), dict) else None
            if light_raw is None and dark_raw is None:
                return self._merged(payload)
            base_values = {k: v for k, v in payload.items() if k in DEFAULTS}
            overrides = payload.get(theme_key) if isinstance(payload.get(theme_key), dict) else {}
            if isinstance(overrides, dict):
                return self._merged({**base_values, **overrides})
            return self._merged(base_values)

        def _block(theme: str, p: dict[str, str]) -> list[str]:
            accent = p.get("accent_color") or DEFAULTS["accent_color"]
            background = p.get("background_color") or DEFAULTS["background_color"]
            card_background = p.get("card_background") or DEFAULTS["card_background"]
            text = p.get("text_color") or DEFAULTS["text_color"]
            text_secondary = p.get("text_secondary") or DEFAULTS["text_secondary"]
            font_family = p.get("font_family") or DEFAULTS["font_family"]
            font_heading = p.get("font_heading") or DEFAULTS["font_heading"]
            base_font_size = p.get("base_font_size") or DEFAULTS["base_font_size"]
            card_radius = p.get("card_radius") or DEFAULTS["card_radius"]
            border_color = p.get("border_color") or DEFAULTS["border_color"]
            border_width = p.get("border_width") or DEFAULTS["border_width"]
            grid_gap = p.get("grid_gap") or DEFAULTS["grid_gap"]
            letter_spacing_heading = p.get("letter_spacing_heading") or DEFAULTS["letter_spacing_heading"]
            button_padding = p.get("button_padding") or DEFAULTS["button_padding"]
            artlomo_btn_text = p.get("artlomo_btn_text") or DEFAULTS["artlomo_btn_text"]
            artlomo_btn_bg = p.get("artlomo_btn_bg") or DEFAULTS["artlomo_btn_bg"]
            artlomo_btn_shadow = p.get("artlomo_btn_shadow") or DEFAULTS["artlomo_btn_shadow"]
            artlomo_btn_hover_bg = p.get("artlomo_btn_hover_bg") or accent
            artlomo_btn_hover_text = p.get("artlomo_btn_hover_text") or DEFAULTS["artlomo_btn_hover_text"]
            artlomo_save_bg = p.get("artlomo_save_bg") or accent
            artlomo_save_text = p.get("artlomo_save_text") or DEFAULTS["artlomo_save_text"]
            danger = p.get("danger_color") or p.get("artlomo_danger") or DEFAULTS.get("danger_color") or DEFAULTS["artlomo_danger"]
            artlomo_lock_border_light = p.get("artlomo_lock_border_light") or DEFAULTS["artlomo_lock_border_light"]
            artlomo_lock_border_dark = p.get("artlomo_lock_border_dark") or DEFAULTS["artlomo_lock_border_dark"]

            return [
                f'html[data-theme="{theme}"] {{',
                f"  --color-bg-primary: {background};",
                f"  --color-background: {background};",
                f"  --color-card-bg: {card_background};",
                f"  --color-text: {text};",
                f"  --color-text-primary: {text};",
                f"  --color-border-primary: {border_color};",
                f"  --color-border-subtle: {border_color};",
                f"  --color-action-danger: {danger};",
                f"  --bg-body: var(--color-background);",
                f"  --bg-secondary: var(--card-bg);",
                f"  --text-primary: var(--color-text);",
                f"  --card-bg: var(--color-card-bg);",
                f"  --card-text: var(--color-text);",
                f"  --button-bg: var(--color-border-primary);",
                f"  --button-text: var(--color-bg-primary);",
                f"  --header-bg: {background};",
                f"  --overlay-surface: var(--color-bg-primary);",
                f"  --button-danger-bg: var(--color-action-danger);",
                f"  --checkbox-accent: var(--color-action-danger);",
                f"  --artlomo-accent: {accent};",
                f"  --accent-color: {accent};",
                f"  --font-family-main: {font_family};",
                f"  --font-primary: {font_family};",
                f"  --font-heading: {font_heading};",
                f"  --base-font-size: {base_font_size};",
                f"  --card-radius: {card_radius};",
                f"  --border-color: {border_color};",
                f"  --border-width: {border_width};",
                f"  --grid-gap: {grid_gap};",
                f"  --letter-spacing-heading: {letter_spacing_heading};",
                f"  --text-secondary: {text_secondary};",
                f"  --button-padding: {button_padding};",
                f"  --artlomo-btn-text: {artlomo_btn_text};",
                f"  --artlomo-btn-bg: {artlomo_btn_bg};",
                f"  --artlomo-btn-shadow: {artlomo_btn_shadow};",
                f"  --artlomo-btn-hover-bg: {artlomo_btn_hover_bg};",
                f"  --artlomo-btn-hover-text: {artlomo_btn_hover_text};",
                f"  --artlomo-save-bg: {artlomo_save_bg};",
                f"  --artlomo-save-text: {artlomo_save_text};",
                f"  --artlomo-danger: {danger};",
                f"  --artlomo-lock-border-light: {artlomo_lock_border_light};",
                f"  --artlomo-lock-border-dark: {artlomo_lock_border_dark};",
                "}",
            ]

        def _root_block(p: dict[str, str]) -> list[str]:
            accent = p.get("accent_color") or DEFAULTS["accent_color"]
            background = p.get("background_color") or DEFAULTS["background_color"]
            card_background = p.get("card_background") or DEFAULTS["card_background"]
            text = p.get("text_color") or DEFAULTS["text_color"]
            text_secondary = p.get("text_secondary") or DEFAULTS["text_secondary"]
            font_family = p.get("font_family") or DEFAULTS["font_family"]
            font_heading = p.get("font_heading") or DEFAULTS["font_heading"]
            base_font_size = p.get("base_font_size") or DEFAULTS["base_font_size"]
            card_radius = p.get("card_radius") or DEFAULTS["card_radius"]
            border_color = p.get("border_color") or DEFAULTS["border_color"]
            border_width = p.get("border_width") or DEFAULTS["border_width"]
            grid_gap = p.get("grid_gap") or DEFAULTS["grid_gap"]
            letter_spacing_heading = p.get("letter_spacing_heading") or DEFAULTS["letter_spacing_heading"]
            button_padding = p.get("button_padding") or DEFAULTS["button_padding"]
            artlomo_btn_text = p.get("artlomo_btn_text") or DEFAULTS["artlomo_btn_text"]
            artlomo_btn_bg = p.get("artlomo_btn_bg") or DEFAULTS["artlomo_btn_bg"]
            artlomo_btn_shadow = p.get("artlomo_btn_shadow") or DEFAULTS["artlomo_btn_shadow"]
            artlomo_btn_hover_bg = p.get("artlomo_btn_hover_bg") or accent
            artlomo_btn_hover_text = p.get("artlomo_btn_hover_text") or DEFAULTS["artlomo_btn_hover_text"]
            artlomo_save_bg = p.get("artlomo_save_bg") or accent
            artlomo_save_text = p.get("artlomo_save_text") or DEFAULTS["artlomo_save_text"]
            danger = p.get("danger_color") or p.get("artlomo_danger") or DEFAULTS.get("danger_color") or DEFAULTS["artlomo_danger"]
            artlomo_lock_border_light = p.get("artlomo_lock_border_light") or DEFAULTS["artlomo_lock_border_light"]
            artlomo_lock_border_dark = p.get("artlomo_lock_border_dark") or DEFAULTS["artlomo_lock_border_dark"]

            return [
                ":root {",
                f"  --color-bg-primary: {background};",
                f"  --color-background: {background};",
                f"  --background-color: {background};",
                f"  --color-card-bg: {card_background};",
                f"  --color-text: {text};",
                f"  --color-text-primary: {text};",
                f"  --color-border-primary: {border_color};",
                f"  --color-border-subtle: {border_color};",
                f"  --color-action-danger: {danger};",
                f"  --bg-body: var(--color-background);",
                f"  --bg-secondary: var(--card-bg);",
                f"  --text-primary: var(--color-text);",
                f"  --card-bg: var(--color-card-bg);",
                f"  --card-text: var(--color-text);",
                f"  --button-bg: var(--color-border-primary);",
                f"  --button-text: var(--color-bg-primary);",
                f"  --header-bg: {background};",
                f"  --overlay-surface: var(--color-bg-primary);",
                f"  --button-danger-bg: var(--color-action-danger);",
                f"  --checkbox-accent: var(--color-action-danger);",
                f"  --artlomo-accent: {accent};",
                f"  --accent-color: {accent};",
                f"  --font-family-main: {font_family};",
                f"  --font-primary: {font_family};",
                f"  --font-heading: {font_heading};",
                f"  --base-font-size: {base_font_size};",
                f"  --card-radius: {card_radius};",
                f"  --border-color: {border_color};",
                f"  --border-width: {border_width};",
                f"  --grid-gap: {grid_gap};",
                f"  --letter-spacing-heading: {letter_spacing_heading};",
                f"  --text-secondary: {text_secondary};",
                f"  --button-padding: {button_padding};",
                f"  --artlomo-btn-text: {artlomo_btn_text};",
                f"  --artlomo-btn-bg: {artlomo_btn_bg};",
                f"  --artlomo-btn-shadow: {artlomo_btn_shadow};",
                f"  --artlomo-btn-hover-bg: {artlomo_btn_hover_bg};",
                f"  --artlomo-btn-hover-text: {artlomo_btn_hover_text};",
                f"  --artlomo-save-bg: {artlomo_save_bg};",
                f"  --artlomo-save-text: {artlomo_save_text};",
                f"  --artlomo-danger: {danger};",
                f"  --artlomo-lock-border-light: {artlomo_lock_border_light};",
                f"  --artlomo-lock-border-dark: {artlomo_lock_border_dark};",
                "}",
            ]

        light_p = _resolved("light")
        dark_p = _resolved("dark")

        lines = _root_block(light_p) + [""] + _block("light", light_p) + [""] + _block("dark", dark_p)

        css_vars = "\n".join(lines) + "\n"
        # Modular preset engine: preset CSS is authoritative; do not write a global theme stylesheet.

        preset_name = self._sanitize_name(str(payload.get("name") or "")) or "default"
        preset_path = self.presets_css_dir / f"{preset_name}.css"

        leica_typography = "\n".join(
            [
                "@font-face {",
                "  font-family: 'Outfit';",
                "  src: url('/static/fonts/Outfit-VariableFont_wght.ttf') format('truetype');",
                "  font-weight: 100 900;",
                "  font-style: normal;",
                "  font-display: swap;",
                "}",
                "",
                "html, body, button, input {",
                "  font-family: 'Outfit', sans-serif !important;",
                "}",
                "",
                "body {",
                "  letter-spacing: 0.01em;",
                "  line-height: 1.5;",
                "}",
                "",
                "h1, h2, h3, h4, h5, h6 {",
                "  letter-spacing: -0.02em;",
                "}",
                "",
                ".stark-topnav a,",
                ".site-header a,",
                ".artlomo-btn,",
                ".btn,",
                "button {",
                "  text-transform: uppercase;",
                "  letter-spacing: 0.08em;",
                "  font-weight: 600;",
                "}",
                "",
                "input, button {",
                "  border-radius: 0px !important;",
                "}",
                "",
            ]
        )

        extra_rules = "\n".join(
            [
                "",
                ".artlomo-admin-surface h1,",
                ".artlomo-admin-surface h2,",
                ".artlomo-admin-surface h3,",
                ".artlomo-admin-surface h4,",
                ".artlomo-admin-surface h5,",
                ".artlomo-admin-surface h6 {",
                "  text-align: left;",
                "  margin: 0 0 40px;",
                "}",
                "",
                ".row {",
                "  margin-left: 0 !important;",
                "  margin-right: 0 !important;",
                "}",
                "",
                ".col,",
                "[class^='col-'],",
                "[class*=' col-'] {",
                "  padding-left: 0 !important;",
                "  padding-right: 0 !important;",
                "  margin-left: 0 !important;",
                "  margin-right: 0 !important;",
                "}",
                "",
                ".artlomo-btn {",
                "  background: transparent;",
                "  border: 1px solid var(--color-text, var(--text-primary)) !important;",
                "  color: var(--color-text, var(--text-primary));",
                "  border-radius: 0px;",
                "  height: 42px;",
                "  padding: var(--button-padding, 12px 24px);",
                "  font-family: var(--font-family-main);",
                "  font-weight: 600;",
                "  text-transform: uppercase;",
                "  letter-spacing: 0.08em;",
                "  display: flex;",
                "  align-items: center;",
                "  justify-content: center;",
                "  gap: 10px;",
                "  text-decoration: none;",
                "  transition: none;",
                "}",
                "",
                ".artlomo-btn:hover,",
                ".artlomo-btn:focus-visible {",
                "  background: var(--color-text, var(--text-primary));",
                "  color: var(--color-bg-primary);",
                "  outline: none;",
                "}",
                "",
                ".artlomo-btn--danger {",
                "  border-color: var(--color-action-danger);",
                "}",
                "",
                ".artlomo-btn--danger:hover,",
                ".artlomo-btn--danger:focus-visible {",
                "  background: var(--color-action-danger);",
                "  border-color: var(--color-action-danger);",
                "  color: var(--color-bg-primary);",
                "}",
                "",
                ".artlomo-workstation-grid {",
                "  display: grid;",
                "  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));",
                "  gap: 40px;",
                "}",
            ]
        )
        custom_css = payload.get("custom_css") if isinstance(payload, dict) and isinstance(payload.get("custom_css"), str) else ""
        custom_css = custom_css.strip() if isinstance(custom_css, str) else ""
        if custom_css:
            custom_css = "\n" + custom_css + "\n"
        preset_css = leica_typography + css_vars + extra_rules + custom_css + "\n"
        preset_path.write_text(preset_css, encoding="utf-8")

    def current_theme(self) -> dict[str, Any]:
        if self.active_path.exists():
            raw = self._load_json(self.active_path)
            if isinstance(raw, dict) and (isinstance(raw.get("light"), dict) or isinstance(raw.get("dark"), dict)):
                light_vals = raw.get("light") if isinstance(raw.get("light"), dict) else {}
                merged = {**DEFAULTS, **self._merged(light_vals or {})}  # type: ignore[arg-type]
                name_val = raw.get("name") or merged.get("name")
                if name_val is not None:
                    merged["name"] = name_val
                folder_val = raw.get("folder") or merged.get("folder")
                if folder_val is not None:
                    merged["folder"] = folder_val
                saved_at_val = raw.get("saved_at")
                if saved_at_val is not None:
                    merged["saved_at"] = saved_at_val
                return merged
            return {**DEFAULTS, **raw}
        return DEFAULTS

    def current_preset(self) -> dict[str, Any]:
        if self.active_path.exists():
            raw = self._load_json(self.active_path)
            if isinstance(raw, dict) and (isinstance(raw.get("light"), dict) or isinstance(raw.get("dark"), dict)):
                return raw
            if isinstance(raw, dict):
                return self._as_twin(
                    str(raw.get("name") or "default").strip() or "default",
                    folder=str(raw.get("folder") or "user"),
                    saved_at=raw.get("saved_at"),
                    light_values=raw,
                )
        return self._as_twin("default", folder="root", saved_at=None, light_values=DEFAULTS)

    def _load_json(self, path: Path) -> dict[str, Any]:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return DEFAULTS
