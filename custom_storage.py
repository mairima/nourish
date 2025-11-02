from whitenoise.storage import CompressedManifestStaticFilesStorage


class IgnoreAdminManifestStorage(CompressedManifestStaticFilesStorage):
    """Custom storage that ignores missing admin font references."""

    def post_process(self, paths, dry_run=False, **options):
        try:
            return super().post_process(paths, dry_run, **options)
        except Exception as exc:
            msg = str(exc)
            if "admin/css/fonts.css" in msg:
                # Skip the admin font file issue safely
                print("⚠️  Ignoring missing admin/fonts.css reference.")
                return []
            raise
