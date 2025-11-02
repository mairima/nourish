from whitenoise.storage import CompressedManifestStaticFilesStorage
from whitenoise.storage import MissingFileError


class IgnoreAdminManifestStorage(CompressedManifestStaticFilesStorage):
    """Fix Heroku MissingFileError for admin/fonts.css during collectstatic."""

    def post_process(self, paths, dry_run=False, **options):
        all_processed = []
        try:
            for name, processed in super().post_process(paths, dry_run, **options):
                all_processed.append((name, processed))
            return all_processed
        except (MissingFileError, FileNotFoundError) as exc:
            msg = str(exc)
            if "admin/css/fonts.css" in msg:
                print("⚠️  Ignoring missing admin/fonts.css reference on Heroku.")
                return all_processed
            raise
