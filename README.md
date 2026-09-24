# Rive Unreal Win64 releases

This repository builds a Win64 Unreal plugin source package from
[`rive-app/rive-unreal`](https://github.com/rive-app/rive-unreal). It does not
modify or fork the upstream plugin.

The [release workflow](.github/workflows/release-win64.yml) checks the latest
published, non-prerelease upstream release each hour. For a new release, it
captures upstream `main` and its `rive-runtime` gitlink, builds the Win64
runtime libraries on a GitHub-hosted Windows runner, and publishes
`RiveUnreal-Win64.zip` here. The zip contains the plugin source, headers,
shaders, and Win64 native libraries. Unreal Engine compiles the plugin modules
when the plugin is installed in a project.

To rerun or build a specific published upstream release, use **Actions >
Release Rive Unreal Win64 source plugin > Run workflow** and optionally enter its tag. An existing
complete `win64-<upstream tag>` release is left unchanged. The release notes
record the exact upstream plugin and runtime commits used for the build.
After a successful run, the workflow keeps the 5 newest published Win64
releases and their CI tags. Drafts and unrelated releases are left alone.

Download `RiveUnreal-Win64.zip` from this repository's Releases page. GitHub's
automatic "Source code" archives contain this CI repository, not the plugin.

Scheduled GitHub Actions can be delayed and may be disabled after 60 days of
repository inactivity. If that happens, re-enable the workflow in Actions and
run it manually to catch up with the latest stable upstream release.
