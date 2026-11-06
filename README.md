# Rive Unreal Win64 builds

This repository builds Win64 Unreal plugin source packages from
[`rive-app/rive-unreal`](https://github.com/rive-app/rive-unreal). It does not
modify or fork the upstream plugin.

## Releases

The [stable workflow](.github/workflows/release-win64.yml) checks upstream
published, non-prerelease Releases every hour at minute 17. Each new version
is built from its upstream tag commit and published here as `stable-<tag>`.
The 2 newest stable packages are retained. Monitoring starts with upstream
`0.4.26`; older versions are not built automatically. `built-release-*` CI
tags record completed upstream releases so pruning a package does not rebuild
it on the next check.

The [tag workflow](.github/workflows/tags-win64.yml) checks all upstream Git
tags every hour at minute 37, including weekly tags and tags without a GitHub
Release. New tags are built and published as `tag-<tag>` prereleases without
changing the latest stable release. Only the newest weekly package, ordered by
the date in its upstream tag, is retained. Completion tags record built weekly
versions so pruning does not rebuild them on the next check. Other tag packages
are retained independently of the stable and daily channels. Existing tags in
[the baseline](.github/upstream-tags-baseline.json), captured on 2026-10-26, are excluded
from automatic builds; manually supply `upstream_tag` to build any existing tag.
The one-version weekly retention also applies to manually requested historical
weeklies, so an older weekly package is removed after it is rebuilt.
Tag names must use letters, digits, dots, underscores, or hyphens and start
with a letter or digit, matching the package version format.

The [manual main workflow](.github/workflows/daily-win64.yml) runs only through
Actions `workflow_dispatch`; it has no scheduled or push trigger. It builds
upstream `main` only when it differs from the most recently published daily
package. Packages retain the `daily-<date>-<commit>` prerelease names; only the
newest package is retained.

All channels use GitHub-hosted Windows to build the Rive runtime and Ubuntu
to assemble `RiveUnreal-Win64.zip`. The zip contains plugin source, headers,
shaders, and Win64 native libraries. Unreal Engine compiles the plugin modules
when installed in a project. Download the zip from this repository's Releases
page; GitHub's automatic "Source code" archives contain this CI repository.

Changes to the stable or tag workflow, the shared build workflow, or the packaging
script pushed to `main` also trigger the corresponding automatic upstream checks.
Upstream tags are detected by polling; no upstream webhook or extra token is
required.

Each channel can also be run manually from Actions. A complete existing
release is left unchanged. Release notes record the exact upstream plugin and
runtime commits and CI commit used for each build. Release tags point to this
repository's `main` at publication, so the release notes identify the exact
CI code used when a build was started.

Scheduled GitHub Actions can be delayed and may be disabled after 60 days of
repository inactivity. Re-enable the workflows in Actions if that happens.
