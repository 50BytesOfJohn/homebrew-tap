# Sidelight Homebrew tap

Install [Sidelight](https://github.com/50BytesOfJohn/sidelight), a native side panel of
always-on widgets for developers and their AI agents:

```sh
brew install --cask 50bytesofjohn/tap/sidelight
```

Requires an Apple Silicon Mac with macOS 26 or later. Launch Sidelight from Applications
and grant Accessibility access when prompted. Individual widgets explain their optional permissions and tools.

Sidelight updates itself through Sparkle. To explicitly upgrade through Homebrew:

```sh
brew update
brew upgrade --cask --greedy 50bytesofjohn/tap/sidelight
```

Ordinary uninstall preserves settings. `brew uninstall --cask --zap sidelight` also removes settings and caches.

## Maintenance

Sidelight's release workflow pushes the cask after successfully publishing a stable release,
using a write-enabled SSH deploy key scoped to this repository. The private key is stored as
`HOMEBREW_TAP_DEPLOY_KEY` in Sidelight's tag-restricted `release` environment.

The hourly **Update Sidelight** workflow is a fallback, using this repository's own `GITHUB_TOKEN`.
It can also be run manually to catch up or retry without rebuilding the app:

```sh
gh workflow run update.yml --repo 50BytesOfJohn/homebrew-tap
```

The updater verifies the published release, the downloaded DMG's SHA-256 and size, and the
published checksum file before updating. It refuses drafts, prereleases, downgrades and changed
checksums for an existing version. Neither workflow replaces upstream release assets.

Run `python3 -m unittest discover -s tests` and `brew style --cask Casks/sidelight.rb` before
changing the updater or cask. The Check workflow also audits the cask online.
