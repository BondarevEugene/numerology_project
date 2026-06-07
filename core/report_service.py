from core.archetype_content_service import (
    ArchetypeContentService
)

from core.matrix_service import MatrixService
from core.personality_service import PersonalityService
from core.archetype_service import ArchetypeService
from core.matrix_interpretation_service import MatrixInterpretationService
from core.report_access_service import ReportAccessService
from core.report_data_builder import ReportDataBuilder
from core.reports.preview_report_builder import PreviewReportBuilder
from core.access.payment_access_service import PaymentAccessService
from core.reports.premium_report_builder import PremiumReportBuilder


class ReportService:

    @staticmethod
    def build(day: int, month: int, year: int):

        matrix, destiny_number = MatrixService.build(
            day,
            month,
            year
        )

        adv_results = PersonalityService.analyze(
            matrix
        )

        print("\n")
        print("ADVANCED ANALYTICS")
        print(adv_results)
        print("\n")

        archetype = ArchetypeService.get(
            destiny_number
        )

        profile_data = (
            ArchetypeContentService
            .get_full_profile(
                destiny_number
            )
        )
        print("\n====================")
        print("PROFILE DATA")
        for k, v in profile_data.items():
            print(f"{k}: {v}")
        print("====================\n")

        raw_jobs = archetype.get(
            "jobs",
            []
        )

        clean_jobs = [
            str(job).title()
            for job in raw_jobs
        ] if raw_jobs else ["Специалист"]

        jobs = clean_jobs

        if ReportAccessService.is_preview_mode():
            jobs = ReportAccessService.get_preview_jobs(
                clean_jobs
            )

        interpretation = archetype.get(
            "interpretation",
            ""
        )

        if ReportAccessService.is_preview_mode():
            interpretation = ReportAccessService.get_preview_text(
                interpretation
            )

        archetype["interpretation"] = interpretation

        cell_statuses = {
            "character_desc": MatrixInterpretationService.get_cell_status(
                matrix,
                "1"
            ),
            "energy_desc": MatrixInterpretationService.get_cell_status(
                matrix,
                "2"
            ),
            "interest_desc": MatrixInterpretationService.get_cell_status(
                matrix,
                "3"
            ),
            "health_desc": MatrixInterpretationService.get_cell_status(
                matrix,
                "4"
            ),
            "logic_desc": MatrixInterpretationService.get_cell_status(
                matrix,
                "5"
            ),
            "labor_desc": MatrixInterpretationService.get_cell_status(
                matrix,
                "6"
            ),
            "luck_desc": MatrixInterpretationService.get_cell_status(
                matrix,
                "7"
            ),
            "duty_desc": MatrixInterpretationService.get_cell_status(
                matrix,
                "8"
            ),
            "memory_desc": MatrixInterpretationService.get_cell_status(
                matrix,
                "9"
            ),

            'action_power': profile_data.get(
                'action_power',
                ''
            ),

            'shadow_side': profile_data.get(
                'shadow_side',
                ''
            ),

            'growth_point': profile_data.get(
                'growth_point',
                ''
            ),

            'realization': profile_data.get(
                'realization',
                ''
            ),

            'karmic_tasks': profile_data.get(
                'karmic_tasks',
                ''
            ),

            'financial_tip': profile_data.get(
                'financial_tip',
                ''
            ),

            'health_tips': profile_data.get(
                'health_tips',
                ''
            ),

            'partner_type': profile_data.get(
                'partner_type',
                ''
            ),

            'mind_power': profile_data.get(
                'mind_power',
                ''
            ),

            'life_result': profile_data.get(
                'life_result',
                ''
            )
        }

        report = ReportDataBuilder.build(
            matrix=matrix,
            destiny_number=destiny_number,
            archetype=archetype,
            adv_results=adv_results,
            jobs=jobs,
            cell_statuses=cell_statuses
        )

        report["day"] = day
        report["month"] = month
        report["year"] = year

        if PaymentAccessService.has_premium_access():

            report = PremiumReportBuilder.build(
                report
            )

        else:

            report = PreviewReportBuilder.build(
                report
            )

        return report
