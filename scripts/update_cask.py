#!/usr/bin/env python3
"""Update the cask only from a published stable upstream release with verified assets."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import urllib.request

UPSTREAM = "50BytesOfJohn/sidelight"
CASK = Path(__file__).resolve().parents[1] / "Casks/sidelight.rb"


def release_details(release):
    tag = release["tag_name"]
    if not re.fullmatch(r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", tag):
        raise ValueError("Expected a numeric stable release tag")
    if release["draft"] or release["prerelease"]:
        raise ValueError("Only published stable releases can update the tap")
    version = tag[1:]
    assets = {asset["name"]: asset for asset in release["assets"]}
    asset = assets[f"Sidelight-{version}.dmg"]
    url = f"https://github.com/{UPSTREAM}/releases/download/{tag}/Sidelight-{version}.dmg"
    if asset["browser_download_url"] != url or asset["state"] != "uploaded":
        raise ValueError("Unexpected or incomplete DMG asset")
    digest = asset["digest"]
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
        raise ValueError("Missing GitHub SHA-256 digest")
    checksum = assets[f"Sidelight-{version}.dmg.sha256"]
    if checksum["browser_download_url"] != url + ".sha256" or checksum["state"] != "uploaded":
        raise ValueError("Unexpected or incomplete checksum asset")
    return version, url, digest.removeprefix("sha256:"), asset["size"]


def render_cask(version, digest):
    return f'''cask "sidelight" do
  version "{version}"
  sha256 "{digest}"

  url "https://github.com/{UPSTREAM}/releases/download/v#{{version}}/Sidelight-#{{version}}.dmg"
  name "Sidelight"
  desc "Side panel of always-on widgets for developers and their AI agents"
  homepage "https://github.com/{UPSTREAM}"

  livecheck do
    url :url
    strategy :github_latest
  end

  auto_updates true
  depends_on arch: :arm64
  depends_on macos: :tahoe

  app "Sidelight.app"

  uninstall quit: "app.getsidelight.Sidelight"

  zap trash: [
    "~/Library/Application Support/Sidelight",
    "~/Library/Caches/app.getsidelight.Sidelight",
    "~/Library/Preferences/app.getsidelight.Sidelight.plist",
    "~/Library/Saved Application State/app.getsidelight.Sidelight.savedState",
  ]
end
'''


def ensure_forward_update(current, version, digest):
    old = re.search(r'^  version "([0-9.]+)"$', current, re.MULTILINE)
    if not old:
        raise ValueError("Cannot determine the existing cask version")
    previous = old[1]
    if tuple(map(int, version.split("."))) < tuple(map(int, previous.split("."))):
        raise ValueError(f"Refusing to downgrade {previous} to {version}")
    if version == previous and f'  sha256 "{digest}"' not in current:
        raise ValueError("Published release assets changed; refusing to replace the checksum")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", default="", help="Published tag; otherwise use the latest stable release")
    args = parser.parse_args()
    if args.tag and not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", args.tag):
        parser.error("tag must be a numeric v-prefixed version")
    endpoint = f"repos/{UPSTREAM}/releases/" + (f"tags/{args.tag}" if args.tag else "latest")
    release = json.loads(subprocess.check_output(["gh", "api", endpoint]))
    version, url, digest, size = release_details(release)
    if CASK.exists():
        ensure_forward_update(CASK.read_text(), version, digest)
    actual = hashlib.sha256()
    downloaded = 0
    with urllib.request.urlopen(url, timeout=120) as response:
        while chunk := response.read(1024 * 1024):
            actual.update(chunk)
            downloaded += len(chunk)
    if actual.hexdigest() != digest or downloaded != size:
        raise ValueError("Downloaded DMG does not match the published digest and size")
    with urllib.request.urlopen(url + ".sha256", timeout=30) as response:
        checksum = response.read().decode().strip()
    if checksum != f"{digest}  Sidelight-{version}.dmg":
        raise ValueError("Published checksum file does not match the DMG")
    CASK.write_text(render_cask(version, digest))
    print(f"Verified Sidelight {version}: {digest}")


if __name__ == "__main__":
    main()
