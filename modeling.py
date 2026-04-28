import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV, StratifiedKFold


def show_confusion_matrix(y_true, y_pred, labels):
    cm = confusion_matrix(y_true, y_pred)

    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)

    # Configurar etiquetas de los ejes
    plt.xlabel('Predicted Class')
    plt.ylabel('Real Class')

    # Mostrar el gráfico
    plt.show()

def param_search(X, y, pipline, param_grid, scoring, k_fold, verbose=4):
    print("Starting evaluation ")

    grid_search = GridSearchCV(estimator=pipline, 
                               param_grid=param_grid, 
                               scoring=scoring, 
                               cv=StratifiedKFold(n_splits=k_fold), 
                               n_jobs=-1,
                               verbose=verbose)
    grid_search.fit(X, y)

    print(scoring, str(grid_search.best_score_))

    best_score = grid_search.best_score_
    best_pipe = grid_search.best_estimator_

    selector = best_pipe.named_steps["select"]
    best_features = X.columns[selector.get_support()]
    best_model_params = best_pipe.named_steps["model"].get_params()
    
    return best_features, best_model_params
