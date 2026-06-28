## 14. Localization Layer

The `l10n/` directory is an OPTIONAL layer providing translated or locale-adapted content for non-base locales. The base locale is `"en-US"` unless overridden by a `base_locale` field in `manifest.json`.

### 14.1 Structure

```
l10n/
  {locale}/              BCP 47 locale tag (e.g., es-MX, fr-FR, ja-JP)
    machine/
      glossary.json      Translated terms (same schema as machine/glossary.json)
      system_prompt.md   Locale-adapted system prompt
    okf/
      terms/             Translated OKF concept files with dkp_locale frontmatter
    human/
      handbook.md        Translated handbook
```

Within each `l10n/{locale}/` subdirectory, only `machine/glossary.json` and `machine/system_prompt.md` are RECOMMENDED. All other assets are OPTIONAL and inherit from the base pack when absent.

### 14.2 Locale Frontmatter

OKF concept files in `l10n/{locale}/okf/` MUST include all required DKP frontmatter (§10.3) plus:

| Field | Type | Required | Description |
|---|---|---|---|
| `dkp_locale` | string | REQUIRED | BCP 47 locale tag matching the parent `l10n/{locale}/` directory |

### 14.3 Conformance

`manifest.json` MUST list all supported locales in the `locales` array. Processors loading a locale-specific bundle SHOULD prefer content from `l10n/{locale}/` over base-pack content for matching locale tags, falling back to base-pack content when locale-specific content is absent. When a locale file in `l10n/{locale}/` contains relative Markdown links to targets that are not translated, producers MUST rewrite those links so they resolve relatively to components outside the localization directory (e.g., `../../okf/terms/concept.md`) rather than relative to the locale directory. Processors SHOULD treat the locale overlay as virtually merged onto the base bundle root when resolving such links, so that any remaining relative paths that were not rewritten still resolve correctly.
