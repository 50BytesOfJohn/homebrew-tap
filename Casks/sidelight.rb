cask "sidelight" do
  version "0.12.1"
  sha256 "49f49f5bed67750b8261c59f9cacd15788c2578b348397102d7f37af1b76b28f"

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
