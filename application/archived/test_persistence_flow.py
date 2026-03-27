#!/usr/bin/env python3
"""
Quick test to verify the persistence flow for video_suite settings.

Flow:
1. Settings saved to artwork_data.json under video_suite key
2. Settings loaded on page and passed to template as data-video-suite-json
3. JS initializes UI controls from persisted settings
4. Settings re-saved to same video_suite key
5. Page reload restores all settings

This script validates the data structures involved.
"""
import json
from pathlib import Path

# Mock persisted data (what would be in artwork_data.json)
persisted_artwork_data = {
    "created_at": "2026-02-20T12:00:00Z",
    "updated_at": "2026-02-20T12:30:00Z",
    "metadata": {"sku": "ART-001"},
    "video_suite": {
        "video_duration": 15,
        "artwork_zoom_intensity": 1.12,
        "artwork_zoom_duration": 3.5,
        "artwork_pan_enabled": True,
        "artwork_pan_direction": "up",
        "mockup_zoom_intensity": 1.1,
        "mockup_zoom_duration": 2.0,
        "mockup_pan_enabled": True,
        "mockup_pan_direction": "down",
        "mockup_pan_auto_alternate": False,
        "video_fps": 30,
        "video_output_size": 1920,
        "video_encoder_preset": "medium",
        "video_artwork_source": "auto",
        "selected_mockups": ["mockup-01", "mockup-02", "mockup-03"],
        "video_mockup_order": ["mockup-02", "mockup-01", "mockup-03"],
        "video_mockup_shots": [
            {"id": "mockup-02", "pan_enabled": True, "pan_direction": "left"},
            {"id": "mockup-01", "pan_enabled": False, "pan_direction": "up"},
        ]
    }
}

def test_video_suite_structure():
    """Validate video_suite structure matches what JS expects"""
    suite = persisted_artwork_data.get("video_suite", {})
    
    # Check all required keys are present
    required_keys = {
        "video_duration", "artwork_zoom_intensity", "artwork_zoom_duration",
        "artwork_pan_enabled", "artwork_pan_direction",
        "mockup_zoom_intensity", "mockup_zoom_duration",
        "mockup_pan_enabled", "mockup_pan_direction", "mockup_pan_auto_alternate",
        "video_fps", "video_output_size", "video_encoder_preset", "video_artwork_source",
        "selected_mockups", "video_mockup_order", "video_mockup_shots"
    }
    
    missing = required_keys - set(suite.keys())
    if missing:
        print(f"❌ Missing keys in video_suite: {missing}")
        return False
    
    print(f"✅ All {len(required_keys)} required keys present in video_suite")
    
    # Validate types
    type_checks = {
        "video_duration": int,
        "artwork_zoom_intensity": (int, float),
        "artwork_zoom_duration": (int, float),
        "artwork_pan_enabled": bool,
        "artwork_pan_direction": str,
        "mockup_zoom_intensity": (int, float),
        "mockup_zoom_duration": (int, float),
        "mockup_pan_enabled": bool,
        "mockup_pan_direction": str,
        "mockup_pan_auto_alternate": bool,
        "video_fps": int,
        "video_output_size": int,
        "video_encoder_preset": str,
        "video_artwork_source": str,
        "selected_mockups": list,
        "video_mockup_order": list,
        "video_mockup_shots": list,
    }
    
    type_errors = []
    for key, expected_type in type_checks.items():
        actual = suite.get(key)
        if isinstance(expected_type, tuple):
            if not isinstance(actual, expected_type):
                type_errors.append(f"{key}: expected {expected_type}, got {type(actual).__name__}")
        else:
            if not isinstance(actual, expected_type):
                type_errors.append(f"{key}: expected {expected_type.__name__}, got {type(actual).__name__}")
    
    if type_errors:
        print(f"❌ Type validation errors:")
        for err in type_errors:
            print(f"   - {err}")
        return False
    
    print(f"✅ All type checks passed")
    
    # Validate array structures
    for mockup_id in suite.get("selected_mockups", []):
        if not isinstance(mockup_id, str):
            print(f"❌ selected_mockups contains non-string: {mockup_id}")
            return False
    
    for mockup_id in suite.get("video_mockup_order", []):
        if not isinstance(mockup_id, str):
            print(f"❌ video_mockup_order contains non-string: {mockup_id}")
            return False
    
    for shot in suite.get("video_mockup_shots", []):
        if not isinstance(shot, dict) or "id" not in shot:
            print(f"❌ video_mockup_shots contains invalid shot: {shot}")
            return False
        if not isinstance(shot.get("pan_enabled"), bool):
            print(f"❌ shot.pan_enabled not bool: {shot}")
            return False
    
    print(f"✅ Array structures validated")
    
    return True

def test_json_serialization():
    """Test that video_suite can be JSON serialized (for template data attribute)"""
    suite = persisted_artwork_data.get("video_suite", {})
    
    try:
        json_str = json.dumps(suite)
        print(f"✅ JSON serialization successful ({len(json_str)} chars)")
    except Exception as e:
        print(f"❌ JSON serialization failed: {e}")
        return False
    
    # Verify we can parse it back
    try:
        reparsed = json.loads(json_str)
        if reparsed != suite:
            print(f"❌ Round-trip JSON parse failed")
            return False
        print(f"✅ Round-trip JSON parse successful")
    except Exception as e:
        print(f"❌ JSON parse failed: {e}")
        return False
    
    return True

def test_deep_merge_logic():
    """Test the deep merge logic for video_suite updates"""
    
    # Current state
    current_artwork_data = {
        "created_at": "2026-02-20T12:00:00Z",
        "metadata": {"sku": "ART-001", "title": "Original"},
        "video_suite": {
            "video_duration": 15,
            "video_fps": 24,
        }
    }
    
    # Patch: Update settings but keep other keys
    patch = {
        "video_suite": {
            "video_duration": 20,
            "video_fps": 30,
            "mockup_pan_enabled": True,
        }
    }
    
    # Apply deep merge (simulating _write_artwork_data logic)
    merged = dict(current_artwork_data)
    if "video_suite" in patch and isinstance(patch["video_suite"], dict):
        existing_suite = merged.get("video_suite", {})
        if not isinstance(existing_suite, dict):
            existing_suite = {}
        merged_suite = dict(existing_suite)
        merged_suite.update(patch["video_suite"])
        merged["video_suite"] = merged_suite
    
    # Verify merge
    expected_suite = {
        "video_duration": 20,
        "video_fps": 30,
        "mockup_pan_enabled": True,
    }
    
    if merged["video_suite"] != expected_suite:
        print(f"❌ Deep merge failed")
        print(f"   Expected: {expected_suite}")
        print(f"   Got: {merged['video_suite']}")
        return False
    
    if merged.get("metadata", {}).get("title") != "Original":
        print(f"❌ Metadata was lost during merge")
        return False
    
    print(f"✅ Deep merge logic correct")
    return True

if __name__ == "__main__":
    print("Testing persistence flow for video_suite settings\n")
    
    tests = [
        ("Video Suite Structure", test_video_suite_structure),
        ("JSON Serialization", test_json_serialization),
        ("Deep Merge Logic", test_deep_merge_logic),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{name}:")
        print("-" * 40)
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Test crashed: {e}")
            results.append((name, False))
    
    print(f"\n{'='*40}")
    print(f"Summary:")
    print(f"{'='*40}")
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(r for _, r in results)
    if all_passed:
        print(f"\n🎉 All tests passed!")
    else:
        print(f"\n⚠️ Some tests failed")
    
    exit(0 if all_passed else 1)
