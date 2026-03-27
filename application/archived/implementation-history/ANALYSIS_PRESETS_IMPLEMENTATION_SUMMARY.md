# Analysis Presets System - Implementation Summary

## Overview

A complete analysis presets system has been implemented to manage AI analysis prompts for OpenAI and Gemini providers. The system includes database persistence, REST API endpoints, admin UI, and integration with the analysis services.

## Components Implemented

### 1. Database Layer

#### Schema

File: [db.py](db.py)

- **AnalysisPreset** model with fields:
  - `id` (Integer, Primary Key)
  - `name` (String) - Unique preset name
  - `provider` (String) - 'openai' or 'gemini'
  - `system_prompt` (Text) - System-level instructions
  - `user_full_prompt` (Text) - Full artwork analysis prompt
  - `user_section_prompt` (Text) - Section-specific analysis prompt
  - `listing_boilerplate` (Text) - Boilerplate text for listings
  - `analysis_prompt` (Text) - General analysis prompt
  - `is_default` (Boolean) - Whether this is the default preset for the provider
  - `created_at` (DateTime)
  - `updated_at` (DateTime)

- Constraints:
  - Unique constraint on (name, provider) pairs
  - Only one default preset per provider

### 2. Service Layer

#### AnalysisPresetService

File: [application/analysis/services.py](application/analysis/services.py)

## Methods

- `list_presets(provider=None, is_default=None)` - List all presets with optional filtering
- `get_default_preset(provider)` - Get the default preset for a provider
- `get_preset_by_id(preset_id)` - Retrieve specific preset
- `get_preset_by_name(name, provider)` - Get preset by name
- `save_preset(...)` - Create or update preset (handles default switching)
- `delete_preset(preset_id)` - Delete a preset (cannot delete default)
- `create_from_legacy_config()` - Initialize from existing house_prompts.py
- `to_dict(preset)` - Convert ORM object to dictionary

## Features

- Lazy initialization of built-in presets
- Default preset management (ensures only one per provider)
- Transaction-safe operations
- Conflict resolution for duplicate name/provider pairs

### 3. REST API Endpoints

#### Analysis Management Admin Routes

File: [application/admin/analysis/routes.py](application/admin/analysis/routes.py)

## Endpoints

| Method | Path | Description |
| -------- | ------ | ------------- |
| GET | `/admin/analysis-management` | Hub page - list all presets |
| GET | `/admin/analysis-management/edit/<provider>/<preset_id>` | Preset editor page |
| POST | `/admin/analysis-management/save` | Save/update preset (JSON) |
| POST | `/admin/analysis-management/delete/<preset_id>` | Delete preset |

Features

- CSRF protection on all mutations
- Admin authentication required
- JSON request/response format
- Comprehensive error handling
- Flash messages for user feedback

### 4. User Interface

#### Admin Hub Template

File: [application/admin/analysis/templates/analysis_management_hub.html](application/admin/analysis/templates/analysis_management_hub.html)

Features

- Tabbed interface (OpenAI/Gemini)
- Preset list with quick actions
- Create new preset button
- Edit/Delete buttons for each preset
- Visual indicator for default presets
- Responsive design

#### Preset Editor Template

File: [application/admin/analysis/templates/analysis_preset_editor.html](application/admin/analysis/templates/analysis_preset_editor.html)

## Fields

- Preset Name (text input)
- System Prompt (textarea - 10 rows)
- Full Artwork Analysis Prompt (textarea - 15 rows)
- Section Analysis Prompt (textarea - 15 rows)
- Listing Boilerplate (textarea - 10 rows)
- Analysis Prompt (textarea - 15 rows)
- Set as Default (checkbox)

Features

- Form validation before submission
- Character count for each field
- Unsaved changes warning
- Auto-save indicator
- Cancel button with confirmation

### 5. Analysis Service Integration

#### OpenAI Analysis Service

File: [application/analysis/openai/service.py](application/analysis/openai/service.py)

## Updates

- Uses `AnalysisPresetService.get_default_preset('openai')` to get current prompts
- Falls back to legacy `house_prompts.py` if no preset exists
- Maintains backward compatibility

#### Gemini Analysis Service

File: [application/analysis/gemini/service.py](application/analysis/gemini/service.py)

Updates

- Uses `AnalysisPresetService.get_default_preset('gemini')` to get current prompts
- Falls back to legacy `house_prompts.py` if no preset exists
- Maintains backward compatibility

### 6. Migration & Initialization

#### Database Patch

File: [patch_db.py](patch_db.py)

## Migration Script

- Creates `analysis_preset` table if it doesn't exist
- Checks for table existence before creating
- Initializes built-in presets on first run
- Safe to run multiple times (idempotent)

## Usage

```bash
python patch_db.py
```

## Data Flow

### Preset Creation

```text
Admin UI → POST /admin/analysis-management/save
→ AnalysisPresetService.save_preset()
→ Database (AnalysisPreset)
```

### Preset Usage in Analysis

```text
OpenAI/Gemini Service
→ AnalysisPresetService.get_default_preset(provider)
→ Database (AnalysisPreset)
→ Analysis Logic
```

### Preset List

```text
GET /admin/analysis-management
→ AnalysisPresetService.list_presets()
→ Database → UI Display
```

## Key Features

### 1. Default Preset Management

- Only one default preset per provider
- Automatic switching when setting a new default
- Cannot delete the default preset
- Falls back to legacy config if no presets exist

### 2. Backward Compatibility

- Existing `house_prompts.py` remains untouched
- Services check for presets first, fall back to legacy config
- Gradual migration possible

### 3. Security

- CSRF protection on all mutations
- Admin authentication required
- Input validation and sanitization
- SQL injection prevention (ORM)

### 4. Error Handling

- Graceful fallback to legacy config
- Comprehensive error messages
- Transaction rollback on conflicts
- User feedback via flash messages

## Usage Examples

### Creating a Preset Programmatically

```python
from application.analysis.services import AnalysisPresetService

preset = AnalysisPresetService.save_preset(
    name="Custom OpenAI",
    provider="openai",
    system_prompt="You are an art analysis expert...",
    user_full_prompt="Analyze this artwork...",
    user_section_prompt="For this section...",
    listing_boilerplate="This artwork...",
    analysis_prompt="Provide detailed analysis...",
    is_default=True,
)
```

### Using a Preset in Analysis

```python
from application.analysis.services import AnalysisPresetService

preset = AnalysisPresetService.get_default_preset('openai')
if preset:
    system_msg = preset.system_prompt
    user_msg = preset.user_full_prompt
```

### Listing All Presets

```python
presets = AnalysisPresetService.list_presets(provider='openai')
for preset in presets:
    print(f"{preset.name} (default: {preset.is_default})")
```

## Files Created/Modified

### Created

- [application/analysis/services.py](application/analysis/services.py)
- [application/admin/analysis/**init**.py](application/admin/analysis/**init**.py)
- [application/admin/analysis/routes.py](application/admin/analysis/routes.py)
- [application/admin/analysis/templates/analysis_management_hub.html](application/admin/analysis/templates/analysis_management_hub.html)
- [application/admin/analysis/templates/analysis_preset_editor.html](application/admin/analysis/templates/analysis_preset_editor.html)

### Modified

- [db.py](db.py) - Added AnalysisPreset model
- [patch_db.py](patch_db.py) - Added migration logic
- [application/app.py](application/app.py) - Registered blueprint
- [application/analysis/openai/service.py](application/analysis/openai/service.py) - Integrated presets
- [application/analysis/gemini/service.py](application/analysis/gemini/service.py) - Integrated presets

## Testing

### Unit Tests

File: [tests/test_analysis_presets.py](tests/test_analysis_presets.py)

## Coverage

- Preset CRUD operations
- Default preset management
- Service integration
- Error handling
- Legacy fallback

### Running Tests

```bash
pytest tests/test_analysis_presets.py -v
```

## Deployment Checklist

- [ ] Run `patch_db.py` to initialize database schema
- [ ] Verify `AnalysisPreset` table exists: `sqlite3 var/db/artlomo.db ".tables"`
- [ ] Test UI at `/admin/analysis-management`
- [ ] Create test presets for OpenAI and Gemini
- [ ] Verify analysis services use new presets
- [ ] Monitor logs for any fallback messages
- [ ] Document for team (this file serves as documentation)

## Future Enhancements

1. **Versioning** - Track changes to presets over time
2. **Import/Export** - Export presets as JSON, import from file
3. **Forking** - Clone existing presets as templates
4. **History** - Audit trail of preset modifications
5. **Testing** - Test preset against sample artworks
6. **Sharing** - Share presets between team members
7. **Analytics** - Track which presets produce best results

## Support

For issues or questions:

1. Check logs in `/srv/artlomo/logs/`
2. Review error messages in admin UI
3. Verify database integrity with `patch_db.py`
4. Test service integration directly with Python shell
