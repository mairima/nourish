from whitenoise.storage import CompressedManifestStaticFilesStorage, MissingFileError


class IgnoreAdminManifestStorage(CompressedManifestStaticFilesStorage):
    """Ignore missing admin/fonts.css during collectstatic on Heroku."""

    def post_process(self, paths, dry_run=False, **options):
        all_processed = []
        try:
            for name, hashed_name, processed in super().post_process(
                paths, dry_run, **options
            ):
                all_processed.append((name, hashed_name, processed))
            return all_processed
        except (MissingFileError, FileNotFoundError) as exc:
            msg = str(exc)
            if "admin/css/fonts.css" in msg:
                print("⚠️  Ignoring missing admin/fonts.css reference on Heroku.")
                return all_processed
            raise
