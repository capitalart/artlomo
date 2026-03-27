(function () {
  function parseCommaItems(raw) {
    const source = String(raw || "");
    const parts = source.split(",");
    const items = parts.map((part) => part.trim()).filter(Boolean);
    const hasEmptyEntries = parts.some((part) => part.trim().length === 0) && source.includes(",");
    return { items, hasEmptyEntries };
  }

  function wordCount(raw) {
    return String(raw || "")
      .trim()
      .split(/\s+/)
      .filter(Boolean).length;
  }

  function hasInvalidEtsyChars(token) {
    // Etsy-safe simplification for this UI: no hyphens, commas are separators only,
    // and no punctuation/symbol noise beyond letters/numbers/spaces.
    return /-|[^a-zA-Z0-9 ]/.test(String(token || ""));
  }

  function getFilenameWithoutExtension(filename) {
    // Remove the file extension (everything after the last dot)
    const dotIndex = String(filename || "").lastIndexOf(".");
    if (dotIndex === -1) {
      return String(filename || "");
    }
    return String(filename || "").substring(0, dotIndex);
  }

  function setCounterState(el, isError) {
    if (!el) return;
    el.style.color = isError ? "#dc3545" : "var(--text-secondary)";
  }

  function updateSaveWarning(hasViolation) {
    const saveBtn = document.querySelector("[data-analysis-save]");
    if (!saveBtn) return;

    if (hasViolation) {
      saveBtn.setAttribute(
        "title",
        "Etsy Compliance Warning: Check mandatory Etsy fields (title, description, tags, quantity, price)."
      );
      saveBtn.dataset.etsyWarning = "1";
      saveBtn.classList.add("btn-warning");
    } else {
      saveBtn.setAttribute("title", "Save all changes");
      delete saveBtn.dataset.etsyWarning;
      saveBtn.classList.remove("btn-warning");
    }
  }

  function runValidation() {
    const titleInput = document.getElementById("title");
    const descriptionInput = document.getElementById("description");
    const tagsInput = document.getElementById("tags");
    const materialsInput = document.getElementById("materials");
    const quantityInput = document.getElementById("quantity");
    const priceInput = document.getElementById("price");
    const seoFilenameInput = document.getElementById("seo_filename");

    const titleCounter = document.querySelector("[data-title-counter]");
    const descriptionCounter = document.querySelector("[data-description-counter]");
    const tagsCounter = document.querySelector("[data-tags-counter]");
    const materialsCounter = document.querySelector("[data-materials-counter]");
    const seoFilenameCounter = document.querySelector("[data-seo-filename-counter]");

    const titleValue = (titleInput && titleInput.value) || "";
    const descriptionValue = (descriptionInput && descriptionInput.value) || "";
    const parsedTags = parseCommaItems((tagsInput && tagsInput.value) || "");
    const tagItems = parsedTags.items;
    const parsedMaterials = parseCommaItems((materialsInput && materialsInput.value) || "");
    const materialItems = parsedMaterials.items;
    const quantityValue = (quantityInput && quantityInput.value) || "";
    const priceValue = (priceInput && priceInput.value) || "";
    const seoFilenameValue = (seoFilenameInput && seoFilenameInput.value) || "";

    const titleTooLong = titleValue.length > 140;
    const titleAllCaps = !!titleValue.trim() && titleValue === titleValue.toUpperCase();
    const titleWords = wordCount(titleValue);
    if (titleCounter) {
      titleCounter.textContent = `${titleValue.length} / 140 chars | ${titleWords} words`;
      setCounterState(titleCounter, titleTooLong || titleAllCaps);
    }

    // Description counter with character and word count
    const descriptionWords = wordCount(descriptionValue);
    if (descriptionCounter) {
      descriptionCounter.textContent = `${descriptionValue.length} / 4500+ chars | ${descriptionWords} words`;
      setCounterState(descriptionCounter, false);  // Description has no hard limit in this UI
    }

    const tooManyTags = tagItems.length > 13;
    const tagTooLong = tagItems.some((tag) => tag.length > 20);
    const tagHasInvalidChars = tagItems.some((tag) => hasInvalidEtsyChars(tag));
    const tagHasEmptyEntries = parsedTags.hasEmptyEntries;
    const uniqueTags = new Set(tagItems.map((tag) => tag.toLowerCase()));
    const duplicateTags = uniqueTags.size !== tagItems.length;
    if (tagsCounter) {
      tagsCounter.textContent = `${tagItems.length} / 13 tags | <=20 chars each`;
      setCounterState(
        tagsCounter,
        tooManyTags || tagTooLong || duplicateTags || tagHasInvalidChars || tagHasEmptyEntries
      );
    }

    const materialTooLong = materialItems.some((item) => item.length > 45);
    const materialHasInvalidChars = materialItems.some((item) => hasInvalidEtsyChars(item));
    const materialHasEmptyEntries = parsedMaterials.hasEmptyEntries;
    if (materialsCounter) {
      materialsCounter.textContent = `${materialItems.length} materials | <=45 chars each`;
      setCounterState(
        materialsCounter,
        materialTooLong || materialHasInvalidChars || materialHasEmptyEntries
      );
    }

    const seoFilenameWithoutExt = getFilenameWithoutExtension(seoFilenameValue);
    const seoFilenameTooLong = seoFilenameWithoutExt.length > 70;
    if (seoFilenameCounter) {
      seoFilenameCounter.textContent = `${seoFilenameWithoutExt.length} / 70 chars`;
      setCounterState(seoFilenameCounter, seoFilenameTooLong);
    }

    const hasMandatoryViolation =
      !titleValue.trim() ||
      titleTooLong ||
      titleAllCaps ||
      !descriptionValue.trim() ||
      !tagItems.length ||
      tooManyTags ||
      tagTooLong ||
      duplicateTags ||
      tagHasInvalidChars ||
      tagHasEmptyEntries ||
      materialTooLong ||
      materialHasInvalidChars ||
      materialHasEmptyEntries ||
      !quantityValue.toString().trim() ||
      !priceValue.toString().trim();

    updateSaveWarning(hasMandatoryViolation);
  }

  document.addEventListener("DOMContentLoaded", function () {
    ["title", "description", "tags", "materials", "quantity", "price", "seo_filename"].forEach((id) => {
      const field = document.getElementById(id);
      if (field) {
        field.addEventListener("input", runValidation);
        field.addEventListener("change", runValidation);
      }
    });

    runValidation();
  });
})();
