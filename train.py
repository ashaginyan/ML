from src.models import Strict_model, Middle_model, Risk_model, get_score

strict_model = Strict_model()
middle_model = Middle_model()
risk_model = Risk_model()

print('Идет обучение строгой модели...')
strict_model.train()
score = get_score(strict_model.y_test, strict_model.y_pred_test)
print(f'Доля объектов, названных строгой моделью неудачей, и при этом действительно неудачных: {round(score[0]*100)}%\n'
      f'Доля объектов категории неудач из всех неудач, которую нашел алгоритм: {round(score[1]*100)}%\n'
      f'Среднее гармоническое между двумя вышеперечисленными метриками: {round(score[2]*100)}%\n'
      f'Общая доля правильных ответов: {round(score[3]*100)}%')
with open('scores.txt', 'w') as f:
    f.write(f'{round(score[0]*100)} {round(score[1]*100)} {round(score[2]*100)} {round(score[3]*100)}\n')

print('Идет обучение средней модели...')
middle_model.train()
score = get_score(middle_model.y_test, middle_model.y_pred_test)
print(f'Доля объектов, названных средней моделью неудачей, и при этом действительно неудачных: {round(score[0]*100)}%\n'
      f'Доля объектов категории неудач из всех неудач, которую нашел алгоритм: {round(score[1]*100)}%\n'
      f'Среднее гармоническое между двумя вышеперечисленными метриками: {round(score[2]*100)}%\n'
      f'Общая доля правильных ответов: {round(score[3]*100)}%')
with open('scores.txt', 'a') as f:
    f.write(f'{round(score[0]*100)} {round(score[1]*100)} {round(score[2]*100)} {round(score[3]*100)}\n')

print('Идет обучение нестрогой модели...')
risk_model.train()
score = get_score(risk_model.y_test, risk_model.y_pred_test)
print(f'Доля объектов, названных нестрогой моделью удачей, и при этом действительно удачных: {round(score[0]*100)}%\n'
      f'Доля объектов категории удач из всех удач, которую нашел алгоритм: {round(score[1]*100)}%\n'
      f'Среднее гармоническое между двумя вышеперечисленными метриками: {round(score[2]*100)}%\n'
      f'Общая доля правильных ответов: {round(score[3]*100)}%')
with open('scores.txt', 'a') as f:
    f.write(f'{round(score[0]*100)} {round(score[1]*100)} {round(score[2]*100)} {round(score[3]*100)}\n')
print('Обучение завершено')
