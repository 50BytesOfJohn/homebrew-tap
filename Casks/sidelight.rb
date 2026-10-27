cask "sidelight" do
  version "0.13.0"
  sha256 "0584381f7d9f3d5e4671b8e6dbfc8e61eadda0b2696580759150f2156bfd3ac4"

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
