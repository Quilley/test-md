# Packaging and host maintenance

## Offline assembly

Use exactly one `<!-- ihd:styles -->` marker in the head and one `<!-- ihd:reader -->` marker before authored scripts. Run `python3 scripts/inline.py source.html result.html` from this package. It embeds shared CSS, reader, four bundled WOFF2 faces and OFL notices, preserves authored content and refuses overwrite.

For authorized custom faces, use `--font-css /absolute/fonts.css`. Define `IHD Serif`, `IHD Sans` and `IHD Mono` at their real weights/styles and include required notices. Local font URLs must stay beneath that CSS directory, use supported font formats and be at most 5MB per file. The legacy `--preview-fonts` flag remains an alias for the bundled fonts. Old custom family aliases remain fallbacks; trial fonts are not bundled.

The helper rejects rendering dependencies left outside the file. Inline images, styles and scripts first. Ordinary external citation/navigation links are allowed. This helper assembles HTML; it is not a renderer, publisher or domain engine. Model code and data stay authored in the source.

## Two independent hosts

The Codex installation is the maintenance source. Both hosts receive complete packages and resolve paths relative to their own skill directory. Normal usage never reads another host's directory or launches another host's CLI. Codex uses `$internal-html-design` with its explicit-invocation policy; Claude Code uses `/internal-html-design` with `disable-model-invocation: true`.

After editing the maintained package, run:

```sh
python3 scripts/sync_hosts.py --target claude --check
python3 scripts/sync_hosts.py --target claude
```

The sync command resolves its source from its own location. `--target codex` also works from a standalone Claude package. `--destination /absolute/skill-directory` supports portable and isolated installations. Check mode is read-only: exit 0 means parity, 1 means drift, and 2 means an invalid request or unreadable package. Shared resources and the entrypoint body are compared by content; host invocation metadata is normalized.

Write mode stages a full package, backs up an existing destination beneath `~/.local/share/internal-html-design/backups/<timestamp>/`, then replaces the destination. It rejects symlinked roots, source/target overlap and unexpected destination names. It does not edit host settings or install runtime dependencies. The included manifest records common file hashes and host identity; a package remains usable if the other installation is absent.

## Checks and examples

Run `python3 -m unittest discover -s tests -p 'test_*.py'` after helper changes. Regenerate every rendered example from `examples/source/` into new output paths, then replace only the generated examples. Run `node tests/check-previews.cjs` with an existing Playwright/browser installation and use `scripts/audit_layout.cjs` for arbitrary outputs. Set `NODE_PATH` and `PLAYWRIGHT_CHROMIUM_EXECUTABLE` where needed; missing runtime access is incomplete validation, not permission to install software automatically.

Validate Codex metadata with the available skill-creator validator. Validate Claude's explicit-invocation metadata and local references, and exercise its real CLI. Use `tests/forward-prompts.json` for fresh document, build and landing prompts, running them independently through each CLI, with outputs in temporary workspaces and no cross-host calls. Compare content preservation, packaging and rendered quality, not identical wording. Keep fixture data labeled as constructed.
