cask "sidelight" do
  version "0.10.0"
  sha256 "865e106cb5cac9a6e4ba905ff41beddf0b8c72ec4d0d4274393cf956c8e69e46"

  url "https://github.com/50BytesOfJohn/sidelight/releases/download/v#{version}/Sidelight-#{version}.dmg"
  name "Sidelight"
  desc "Side panel of always-on widgets for developers and their AI agents"
  homepage "https://github.com/50BytesOfJohn/sidelight"

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
