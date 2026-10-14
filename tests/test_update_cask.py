import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("update_cask", Path(__file__).parents[1] / "scripts/update_cask.py")
update = importlib.util.module_from_spec(spec)
spec.loader.exec_module(update)


class ReleaseValidationTests(unittest.TestCase):
    def release(self):
        url = "https://github.com/50BytesOfJohn/sidelight/releases/download/v0.6.1/Sidelight-0.6.1.dmg"
        return {
            "tag_name": "v0.6.1", "draft": False, "prerelease": False,
            "assets": [
                {"name": "Sidelight-0.6.1.dmg", "browser_download_url": url,
                 "state": "uploaded", "size": 100, "digest": "sha256:" + "a" * 64},
                {"name": "Sidelight-0.6.1.dmg.sha256", "browser_download_url": url + ".sha256",
                 "state": "uploaded"},
            ],
        }

    def test_published_release(self):
        version, _, digest, size = update.release_details(self.release())
        self.assertEqual((version, digest, size), ("0.6.1", "a" * 64, 100))

    def test_unpublished_and_prerelease_rejected(self):
        for field in ("draft", "prerelease"):
            release = self.release()
            release[field] = True
            with self.assertRaises(ValueError):
                update.release_details(release)

    def test_malformed_tag_and_untrusted_asset_rejected(self):
        release = self.release()
        release["tag_name"] = 'v0.6.1"'
        with self.assertRaises(ValueError):
            update.release_details(release)
        release = self.release()
        release["assets"][0]["browser_download_url"] = "https://example.com/untrusted.dmg"
        with self.assertRaises(ValueError):
            update.release_details(release)

    def test_missing_digest_rejected(self):
        release = self.release()
        release["assets"][0]["digest"] = ""
        with self.assertRaises(ValueError):
            update.release_details(release)

    def test_downgrade_and_changed_release_rejected(self):
        current = update.render_cask("0.6.1", "a" * 64)
        for version, digest in (("0.6.0", "a" * 64), ("0.6.1", "b" * 64)):
            with self.assertRaises(ValueError):
                update.ensure_forward_update(current, version, digest)
        update.ensure_forward_update(current, "0.6.1", "a" * 64)
        update.ensure_forward_update(current, "0.7.0", "b" * 64)


if __name__ == "__main__":
    unittest.main()
