class ReportAccessService:

    @staticmethod
    def is_preview_mode():
        return True

    @staticmethod
    def get_preview_jobs(jobs):
        return jobs[:3]

    @staticmethod
    def get_preview_text(text):
        if not text:
            return ""
        return text[:1500]