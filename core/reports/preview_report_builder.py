class PreviewReportBuilder:

    @staticmethod
    def build(report):

        preview = report.copy()

        jobs = preview.get(
            "jobs",
            []
        )

        preview["jobs"] = jobs[:3]

        interpretation = preview.get(
            "interpretation",
            ""
        )

        if len(interpretation) > 1200:
            preview["interpretation"] = (
                interpretation[:1200]
                + "\n\n[ Полная версия доступна в Genesis PRO ]"
            )

        preview["is_preview"] = True

        return preview