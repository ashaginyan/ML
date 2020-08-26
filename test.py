from src.models import Strict_model, Middle_model, Risk_model

strict_model = Strict_model()
middle_model = Middle_model()
risk_model = Risk_model()

y_strict, y_proba_strict = strict_model.test()

y_middle = middle_model.test()

y_risk, y_proba_risk = risk_model.test()

for i in range(len(y_strict)):
    if y_strict[i] == 1:
        print(f'Строка {i}: Строгая модель говорит, что вас ждет неудача. Вероятность неудачи: {round(y_proba_strict[i, 1]*100)}%')
    else:
        print(f'Строка {i}: Строгая модель говорит, что вас ждет успех. Вероятность успеха: {round(y_proba_strict[i, 0]*100)}%')

    if y_middle[i] == 1:
        print(f'Строка {i}: Средняя модель считает, что вас ждет неудача')
    else:
        print(f'Строка {i}: Средняя модель считает, что вас ждет успех')

    if y_risk[i] == 0:
        print(f'Строка {i}: Рисковая модель считает, что вас ждет неудача. Вероятность неудачи: {round(y_proba_risk[i, 0]*100)}%')
    else:
        print(f'Строка {i}: Рисковая модель считает, что вас ждет успех. Вероятность успеха: {round(y_proba_risk[i, 1]*100)}%')

    print('____________________________________________________________________________________________________________')
