#!/usr/bin/env python3
"""
Manual Testing Guide: Director's Suite Persistence (Stage C)

This guide walks through manual testing of the unified persistence layer.
Each test should take ~2 minutes and fully exercises one persistence scenario.
"""

# ==============================================================================
# TEST SCENARIOS
# ==============================================================================

test_scenarios = [
    {
        "name": "T1: Single Setting Persistence",
        "description": "Test that a single setting change persists across reload",
        "steps": [
            "1. Open Director's Suite for any artwork",
            "2. Note current Duration (should be 15s or saved value)",
            "3. Click the '20s' duration button",
            "4. Verify button shows dark/selected style",
            "5. If auto-save, wait 1s; else look for Save button and click",
            "6. Press F5 to reload the page",
            "7. Check Duration - should still show 20s button as selected",
            "8. ✅ PASS: Duration persisted after reload",
        ],
        "expected_result": "Duration remains at 20s after page reload",
    },
    {
        "name": "T2: Multiple Setting Persistence",
        "description": "Test that multiple settings persist together",
        "steps": [
            "1. Open Director's Suite",
            "2. Change Duration to 20s",
            "3. Change Artwork Zoom to 1.2x (slider)",
            "4. Change Artwork Pan Direction to 'left'",
            "5. Change Output FPS to 60",
            "6. Change Output Size to 1920",
            "7. Verify all changes are visible in UI",
            "8. Save settings (auto or manual)",
            "9. Wait 2 seconds (let save complete)",
            "10. Reload page (F5)",
            "11. Verify all 5 settings are at their new values",
            "12. ✅ PASS: All settings persisted together",
        ],
        "expected_result": "All 5 settings restored to user-set values",
    },
    {
        "name": "T3: Mockup Selection Persistence",
        "description": "Test that selected mockups persist",
        "steps": [
            "1. Open Director's Suite",
            "2. In storyboard, select first 3 mockups (click checkboxes)",
            "3. Verify checkbox markers appear on selected mockups",
            "4. Check 'Mockups Selected' counter shows 3",
            "5. Save settings",
            "6. Reload page (F5)",
            "7. Check that same 3 mockups are still selected",
            "8. Check counter still shows 3",
            "9. ✅ PASS: Mockup selection persisted",
        ],
        "expected_result": "Same 3 mockups remain selected after reload",
    },
    {
        "name": "T4: Mockup Order Persistence",
        "description": "Test that drag-reordered mockup list persists",
        "steps": [
            "1. Open Director's Suite",
            "2. Select 3 mockups from storyboard",
            "3. In 'Chosen Mockups' panel, drag mockup-1 to position 3",
            "4. Verify order in panel changed visually",
            "5. Save settings",
            "6. Reload page (F5)",
            "7. In 'Chosen Mockups' panel, verify mockup-1 is still at position 3",
            "8. ✅ PASS: Mockup order persisted",
        ],
        "expected_result": "Mockup order in 'Chosen Mockups' remains as set",
    },
    {
        "name": "T5: Per-Mockup Pan Settings Persistence",
        "description": "Test that individual pan settings per mockup persist",
        "steps": [
            "1. Open Director's Suite",
            "2. Enable 'Mockup Pan'",
            "3. Select 2 mockups",
            "4. For mockup-1: Set pan direction to 'Left'",
            "5. For mockup-2: Set pan direction to 'Right'",
            "6. Verify settings display in 'Chosen Mockups' panel",
            "7. Save settings",
            "8. Reload page (F5)",
            "9. Expand each mockup's settings in panel",
            "10. Verify mockup-1 still shows 'Left' pan",
            "11. Verify mockup-2 still shows 'Right' pan",
            "12. ✅ PASS: Per-mockup settings persisted",
        ],
        "expected_result": "Each mockup's pan direction remains at user setting",
    },
    {
        "name": "T6: Pan Toggle with Direction Buttons",
        "description": "Test that pan toggle state and direction buttons persist",
        "steps": [
            "1. Open Director's Suite",
            "2. Toggle 'Artwork Pan' OFF",
            "3. Verify pan direction buttons become greyed/disabled",
            "4. Save settings",
            "5. Reload page (F5)",
            "6. Verify 'Artwork Pan' toggle is still OFF",
            "7. Verify direction buttons are still greyed",
            "8. Toggle 'Artwork Pan' ON",
            "9. Verify direction buttons are now enabled",
            "10. Select 'down' direction",
            "11. Save settings",
            "12. Reload page (F5)",
            "13. ✅ PASS: Pan toggle and direction both persisted",
        ],
        "expected_result": "Pan toggle state and last selected direction both restored",
    },
    {
        "name": "T7: Output Settings Suite",
        "description": "Test all output settings persist together",
        "steps": [
            "1. Open Director's Suite",
            "2. Set Output FPS to 60",
            "3. Set Output Size to 2560",
            "4. Set Encoder Preset to 'slow'",
            "5. Set Artwork Source to 'master' (if available)",
            "6. Check for output warning (should show if fps=60 and size>=1920)",
            "7. Save settings",
            "8. Reload page (F5)",
            "9. Verify all 4 output settings match what you set",
            "10. Check warning status matches",
            "11. ✅ PASS: All output settings persisted with warning state",
        ],
        "expected_result": "All output settings and warning state restored",
    },
    {
        "name": "T8: Fresh Start (No Persisted Data)",
        "description": "Test UI initialization when no settings are saved yet",
        "steps": [
            "1. Get a fresh artwork that has never been configured",
            "   (Or delete artwork_data.json for test artwork)",
            "2. Open Director's Suite",
            "3. Verify default values appear:",
            "   - Duration: 15s",
            "   - Artwork Zoom: 1.1x",
            "   - Artwork Pan: ON, direction: up",
            "   - Mockup Zoom: 1.1x",
            "   - FPS: 24",
            "   - Size: 1024",
            "   - Preset: fast",
            "   - Source: auto",
            "4. Verify no mockups selected initially",
            "5. ✅ PASS: Defaults work correctly",
        ],
        "expected_result": "UI shows sensible defaults when no saved state exists",
    },
    {
        "name": "T9: Settings Clear and Reset",
        "description": "Test clearing settings and starting fresh",
        "steps": [
            "1. Open Director's Suite with existing settings",
            "2. Manually note the current values",
            "3. Change everything to different values",
            "4. Save the changes",
            "5. Reload page - verify new values are there",
            "6. Change everything back to original values",
            "7. Save again",
            "8. Reload page - verify original values are restored",
            "9. ✅ PASS: Can cycle between settings cleanly",
        ],
        "expected_result": "Settings can be changed, saved, and restored multiple times",
    },
    {
        "name": "T10: Legacy Data Migration",
        "description": "Test backward compatibility with old top-level key format",
        "steps": [
            "1. Find artwork with old top-level keys in artwork_data.json",
            "   (created before Stage C)",
            "2. Open Director's Suite for that artwork",
            "3. Verify settings load correctly from old format",
            "4. Change one setting",
            "5. Save settings",
            "6. Check artwork_data.json - should now have 'video_suite' key",
            "7. Old top-level keys should still be there (not deleted)",
            "8. Reload page - settings should still restore",
            "9. ✅ PASS: Migration from old format works seamlessly",
        ],
        "expected_result": "Old data loads, saves under new video_suite key, no data loss",
    },
]

# ==============================================================================
# CHECKING TOOLS
# ==============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                  Director's Suite Persistence Test Guide                    ║
║                                 (Stage C)                                   ║
╚════════════════════════════════════════════════════════════════════════════╝

This guide provides 10 manual test scenarios to validate the complete
persistence implementation for the Director's Suite.

Each test takes 2-5 minutes and validates one aspect of the persistence layer.

RECOMMENDED TEST ORDER:
- Start with T1 (simplest)
- Progress through T2-T7 (core functionality)
- T8 validates defaults
- T9 tests multiple cycles
- T10 validates backward compatibility

QUICK CHECKLIST:
- Does changing Duration persist? → T1
- Do multiple settings persist together? → T2  
- Do mockup selections persist? → T3
- Do mockup orders persist? → T4
- Do per-mockup settings persist? → T5
- Do toggles with dependent buttons work? → T6
- Do output settings persist? → T7
- Are defaults correct when nothing saved? → T8
- Can you change settings multiple times? → T9
- Does old data migrate smoothly? → T10

═══════════════════════════════════════════════════════════════════════════════
""")

for i, scenario in enumerate(test_scenarios, 1):
    print(f"\n┌─ TEST {i}/10: {scenario['name']}")
    print(f"├─ Description: {scenario['description']}")
    print(f"├─ Expected Result: {scenario['expected_result']}")
    print(f"└─ Steps:")
    for step in scenario['steps']:
        print(f"     {step}")

print(f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                       TESTING BEST PRACTICES                               ║
╚════════════════════════════════════════════════════════════════════════════╝

1. CLEAR BROWSER CACHE BETWEEN TESTS (optional but recommended)
   - Hard refresh (Ctrl+Shift+Delete or DevTools → Network → Disable Cache)
   - Or test in Incognito mode

2. ISOLATE EACH TEST
   - Each test should start with a fresh page load
   - Don't run multiple tests on the same page without reload

3. VERIFY SAVE COMPLETED
   - If auto-save: look for visual feedback (toast, status)
   - If manual save: click Save button and wait for response

4. CHECK BROWSER CONSOLE
   - Open DevTools (F12)
   - Check Console tab for any JavaScript errors
   - No errors expected during normal operation

5. VERIFY DATA PERSISTED
   - Open artwork_data.json in processed directory
   - Should contain "video_suite" key after first save
   - Should have "updated_at" timestamp

6. DATABASE STATE
   - After each save, note the timestamp in artwork_data.json
   - Should update on each save
   - Timestamps prove persistence is working

═══════════════════════════════════════════════════════════════════════════════

TESTING DATA FOR SPECIFIC CASES:

Test T1 - Duration Values:  10s, 15s, 20s (these are the only valid options)
Test T2 - Zoom Range:       1.0x to 1.35x (artwork), 1.0x to 1.2x (mockup)
Test T3 - Mockup Selection: Usually 1-7 mockups optimal
Test T4 - Mockup Order:     Any reordering of selected mockups
Test T5 - Pan Direction:    up, down, left, right
Test T6 - Pan Direction:    up, down, left, right  
Test T7 - FPS Values:       24, 30, 60
Test T7 - Size Values:      1024, 1536, 1920, 2560, 3840
Test T7 - Preset Values:    fast, medium, slow
Test T7 - Source Values:    auto, closeup_proxy, master (if available)

═══════════════════════════════════════════════════════════════════════════════

TROUBLESHOOTING:

Problem: Settings don't persist after reload
└─ Check: Is save endpoint working? (Network tab in DevTools)
└─ Check: Does artwork_data.json have "video_suite" key?
└─ Check: Is page actually reloading or using cache?

Problem: Only some settings persist
└─ Check: Which specific settings are missing?
└─ Possible: Not all controls implemented in initializeFromPersistedSuite()
└─ Action: Check video_cinematic.js line 653-730

Problem: UI frozen or buttons disabled incorrectly
└─ Check: Browser console for JavaScript errors
└─ Check: Pan toggle state - dependent buttons disable when toggle OFF
└─ Check: Auto-alternate toggle - affects pan direction button state

Problem: Old artwork data not loading
└─ Check: Is artwork_data.json missing?
└─ Check: Does it have top-level keys instead of "video_suite"?
└─ Action: This is T10 (legacy migration) - should still work

═══════════════════════════════════════════════════════════════════════════════

SUCCESS CRITERIA:

All 10 tests PASS if:
✅ Can change any single setting and have it persist
✅ Can change multiple settings simultaneously and all persist
✅ Mockup selection persists with exact same mockups selected
✅ Mockup order persists exactly as reordered
✅ Per-mockup pan settings persist individually
✅ Pan toggle state and direction both persist
✅ Output settings all persist together
✅ Defaults appear correctly on fresh start
✅ Can cycle through multiple change/save/reload cycles
✅ Old format data migrates and works with new format

═══════════════════════════════════════════════════════════════════════════════

Good luck with testing! 🎬
""")
