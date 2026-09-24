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

The [daily workflow](.github/workflows/daily-win64.yml) checks upstream
`main` at 08:00 China time (00:00 UTC). It builds only when `main` differs
from the most recently published daily build. Daily builds are prereleases named
`daily-<date>-<commit>`; only the newest daily build is retained.

Both channels use GitHub-hosted Windows to build the Rive runtime and Ubuntu
to assemble `RiveUnreal-Win64.zip`. The zip contains plugin source, headers,
shaders, and Win64 native libraries. Unreal Engine compiles the plugin modules
when installed in a project. Download the zip from this repository's Releases
page; GitHub's automatic "Source code" archives contain this CI repository.

Both workflows can also be run manually from Actions. A complete existing
release is left unchanged. Release notes record the exact upstream plugin and
runtime commits used for each build.

Scheduled GitHub Actions can be delayed and may be disabled after 60 days of
repository inactivity. Re-enable the workflows in Actions if that happens.
