# Analysis Presets - File Upload & Admin Export Features

## Overview

Two new features have been added to enhance the analysis workflow:

1. **File Upload for Presets** - Upload JSON files to populate all analysis preset fields at once
2. **Admin Export Bundle** - Export analysis data, metadata, and images for iteration and refinement

---

## Feature 1: File Upload for Analysis Presets

### Purpose

Allows rapid testing and refinement of AI analysis prompts by uploading JSON files containing preset configurations.

### Location

**Analysis Management Hub** - `/admin/analysis-management`

### How to Use

#### Step 1: Prepare Your JSON File

Create a JSON file with the following structure:

```json
{
  "system_prompt": "You are a Senior Art Curator...",
  "user_full_prompt": "ARTWORK\n- Title: {title}\n- Slug: {slug}\n...",
  "user_section_prompt": "ARTWORK\n- Title: {title}\n...",
  "listing_boilerplate": "This artwork...",
  "analysis_prompt": "Provide detailed analysis..."
}
```

## Required fields

- `system_prompt` - System-level instructions for the AI
- `user_full_prompt` - Complete artwork analysis prompt
- `user_section_prompt` - Section-specific analysis prompt
- `listing_boilerplate` - Boilerplate text for listings
- `analysis_prompt` - General analysis prompt template

#### Step 2: Upload the File

On the Analysis Management page, you'll see the "Import Preset from File" section:

- **Drag & drop** the JSON file into the upload area, OR
- **Click** the "click to select" link and choose the file

#### Step 3: Configure Provider & Name

A modal will appear asking you to:

- Select the **provider** (OpenAI or Gemini)
- Enter a **preset name** (e.g., "Test v1.0", "Pioneer Engine v2.0")

Click **"Import & Edit"** to proceed.

#### Step 4: Review & Save

The preset editor will open with all fields pre-populated from your JSON file:

- Review all fields
- Make any manual adjustments if needed
- Click **Save** to save the preset

#### Step 5: Test the Preset

Once saved, you can:

- Use it as the **default** for new analyses
- Test it on individual artworks
- Compare results with other presets

### Workflow for Iterative Refinement

```text
1. Export analysis bundle for an artwork
2. Share bundle with AI (Claude, ChatGPT, etc.)
3. AI refines the prompts based on results
4. Save refined prompts as JSON file
5. Upload JSON file to ArtLomo
6. Test refined preset on artwork
7. Repeat until results are perfect
```

### File Upload Features

- **Drag & drop support** - Drag JSON files directly onto the upload area
- **Click to browse** - Use traditional file browser
- **Validation** - Only accepts .json files
- **Error handling** - Clear error messages if JSON is invalid
- **Status messages** - Success/error feedback after upload

---

## Feature 2: Admin Export Bundle

Purpose

Create comprehensive bundles of analysis data for iteration and refinement of the analysis system.

### What Gets Bundled

Each export creates a `.tar.gz` file containing:

1. **analysis.json** - The AI-generated analysis metadata
  - Description, materials, colors, tags
  - Visual analysis, mood, palette
  - Analysis source and model used

2. **metadata.json** - Artwork metadata
  - SKU, slug, dimensions
  - Upload information, processing status
  - Any custom metadata

3. **info.json** - Export information
  - Export timestamp
  - Provider (OpenAI/Gemini)
  - Slug and SKU for reference

4. **analyse_image.jpg** - The ANALYSE version of the artwork
  - Optimized for AI analysis
  - High quality for review
  - Original metadata preserved

Location

**Artwork Analysis Page** - When viewing an artwork analysis

How to Use

#### Step 1: Navigate to Artwork Analysis

1. Go to an artwork that has been analyzed
2. Click the artwork to view its analysis page
3. Look for the **"Admin Export"** button next to the regular "Export" button

#### Step 2: Click Admin Export

- If the artwork has **OpenAI analysis**: Exports OpenAI data
- If the artwork has **Gemini analysis**: Exports Gemini data
- Button is only visible to logged-in admin users

#### Step 3: Download Bundle

The browser will download a `.tar.gz` file with the naming format:

```text
{slug}_analysis_{provider}_{timestamp}.tar.gz
```

Example: `rjc-0165_analysis_openai_20260205_093940.tar.gz`

#### Step 4: Extract & Review

```bash
tar -xzf rjc-0165_analysis_openai_20260205_093940.tar.gz
```

This creates a directory with:

- `rjc-0165/analysis.json` - Analysis data
- `rjc-0165/metadata.json` - Artwork metadata
- `rjc-0165/info.json` - Export metadata
- `rjc-0165/analyse_*.jpg` - Image file

#### Step 5: Share for Refinement

Share the bundle with:

- Team members
- AI assistants (Claude, ChatGPT, etc.)
- External consultants

They can review the analysis and suggest prompt refinements.

### Typical Workflow for Perfect Analysis

```text
1. Analyze an artwork
2. Review the generated analysis
3. Export bundle using "Admin Export"
4. Share bundle with AI assistant/team
5. Receive feedback on analysis quality
6. Get refined prompts from assistant
7. Save refined prompts as JSON
8. Import JSON file to Analysis Management
9. Test refined preset on same artwork
10. Compare results - iterate if needed
11. Once perfect, set as default preset
```

### Access Control

- **Authentication Required**: Only logged-in admin users can export
- **Security Logging**: All admin exports are logged with user ID and timestamp
- **HTTPS Recommended**: Use HTTPS in production to protect sensitive data

### File Naming

Exports are named with timestamp for easy sorting:

- `{slug}_analysis_{provider}_{YYYYMMDD}_{HHMMSS}.tar.gz`
- Example: `rjc-0165_analysis_openai_20260205_093940.tar.gz`

---

## Integration Points

### Analysis Services

Both services (`OpenAI` and `Gemini`) now use presets from the Analysis Presets System:

```python
from application.analysis.services import AnalysisPresetService

# Get the active preset for a provider

preset = AnalysisPresetService.get_default_preset('openai')

# Use in analysis

if preset:
    system_msg = preset.system_prompt
    user_msg = preset.user_full_prompt
```

### Artwork Routes

- **Admin Export Route**: `/artwork/<slug>/admin-export/<provider>`
- **Returns**: `.tar.gz` file with analysis bundle
- **Auth**: Requires `session.get("is_admin")` to be true

### Logs

Admin exports are logged to security audit trail:

```text
action: admin_export
details: slug={slug} provider={provider}
user_id: {username}
timestamp: ISO 8601
```

---

## Technical Details

### File Upload Implementation

- **Frontend**: JavaScript with drag-drop support
- **Validation**: JSON schema validation
- **Modal**: Interactive provider/name selection
- **Query Parameters**: Imported data passed via `?imported_data=...&name=...`

### Admin Export Implementation

- **Service**: `AdminExportService` in `application/artwork/services/admin_export_service.py`
- **Format**: tar.gz (compressed tarball)
- **Contents**: Analysis JSON, metadata, image, export info
- **Streaming**: Files streamed directly, not stored on disk

### Database

- Presets stored in `AnalysisPreset` table
- Fields: id, name, provider, system_prompt, user_full_prompt, user_section_prompt, listing_boilerplate, analysis_prompt, is_default, created_at, updated_at
- Constraints: Unique (name, provider) pairs, one default per provider

---

## Examples

### Example: OpenAI Preset JSON

```json
{
  "system_prompt": "You are a museum curator specializing in contemporary abstract art. Provide professional, insightful analysis suitable for online galleries.",
  "user_full_prompt": "ARTWORK\n- Title: {title}\n- Slug: {slug}\n- Dimensions: {aspect}\n\nProvide a detailed analysis covering:\n1. Visual composition and technique\n2. Color palette and mood\n3. Materials and medium\n4. Subject matter and themes\n5. Overall impression and recommendations",
  "user_section_prompt": "Edit this section of the artwork analysis:\n\n{section_content}\n\nMaintain professional tone and format.",
  "listing_boilerplate": "This artwork is offered as a digital download in museum-quality resolution.",
  "analysis_prompt": "Analyze the artwork for quality and completeness."
}
```

### Example: Extracting Analysis Bundle

```bash

# Download from browser (saves to Downloads folder)

# File: rjc-0165_analysis_openai_20260205_093940.tar.gz

# Extract in a working directory

cd ~/artlomo-analysis
tar -xzf rjc-0165_analysis_openai_20260205_093940.tar.gz

# View contents

ls -la rjc-0165/

# Read analysis

cat rjc-0165/analysis.json | jq '.analysis'

# View metadata

cat rjc-0165/metadata.json | jq '.'

# Check export info

cat rjc-0165/info.json | jq '.'

# View the analyse image

open rjc-0165/analyse_*.jpg  # macOS
```

---

## Troubleshooting

### Upload Issues

## "Invalid JSON file"

- Ensure file is valid JSON (use jsonlint.com to validate)
- Check all required fields are present
- Verify no trailing commas in JSON

## "Please select a JSON file"

- Only .json file extensions are accepted
- Rename your file if needed

### Admin Export Issues

## "Export failed: Artwork not found"

- Artwork slug may not exist in processed directory
- Check that artwork has been processed

## "Export failed: Export permissions"

- You must be logged in as admin
- Check that session has `is_admin = True`

## Download doesn't start

- Check browser download settings
- Ensure JavaScript is enabled
- Try a different browser

### Preset Issues

## "Cannot unset default preset"

- Each provider must have exactly one default
- Set another preset as default before unsetting this one

## Preset not showing in analysis

- Check that preset is marked as default
- Verify provider matches (OpenAI vs Gemini)
- Restart services to clear cache

---

## Best Practices

### For AI Analysis Refinement

1. **Export bundled data** early and frequently
2. **Share with experts** - Art curators, AI specialists
3. **Document changes** - Note what worked and what didn't
4. **Version your presets** - Name them "v1.0", "v1.1", etc.
5. **Test incrementally** - Small changes, test immediately
6. **Keep backup presets** - Don't delete old versions until new ones proven

### For File Uploads

1. **Use descriptive filenames** - `openai_curator_v1.0.json`
2. **Validate before uploading** - Use jsonlint or IDE
3. **Document your JSON** - Add comments about changes
4. **Keep copies** - Store JSON files in version control
5. **Test on test data first** - Try new presets on sample artworks

### Security

1. **Admin-only access** - Only admin users can export
2. **Protect bundles** - Don't share with untrusted parties
3. **HTTPS everywhere** - Use HTTPS in production
4. **Audit logs** - Review admin export logs regularly
5. **Access control** - Limit who has admin privileges

---

## Related Files

- [application/admin/analysis/routes.py](application/admin/analysis/routes.py) - Preset routes
- [application/admin/analysis/templates/analysis_management_hub.html](application/admin/analysis/templates/analysis_management_hub.html) - File upload UI
- [application/artwork/services/admin_export_service.py](application/artwork/services/admin_export_service.py) - Export service
- [application/artwork/routes/artwork_routes.py](application/artwork/routes/artwork_routes.py) - Admin export route
- [application/artwork/ui/templates/artwork_analysis.html](application/artwork/ui/templates/artwork_analysis.html) - Admin export button

---

## Future Enhancements

- **Preset diffing** - Compare two presets side-by-side
- **Batch export** - Export multiple artworks at once
- **Preset templates** - Start from built-in templates
- **Analysis history** - Track changes to analysis over time
- **Automated testing** - Test presets on batches of artworks
- **Analytics** - See which presets work best
- **Collaboration** - Share presets with team members
