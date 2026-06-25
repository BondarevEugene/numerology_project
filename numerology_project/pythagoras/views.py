# В начало файла
from .analyser import PersonalityAdvancedAnalyser


def matrix_view(request):
    # ... существующий код получения даты и расчета матрицы ...
    # Допустим, переменная с матрицей называется result_matrix

    # Инициализируем наш новый анализатор
    analyser = PersonalityAdvancedAnalyser(result_matrix)
    advanced_data = analyser.get_analysis_report()

    context = {
        'result_matrix': result_matrix,  # ваша стандартная матрица
        'advanced': advanced_data,  # новые данные
        'chart_labels': advanced_data['chart_data']['labels'],
        'chart_values': advanced_data['chart_data']['values'],
    }
    return render(request, 'matrix.html', context)