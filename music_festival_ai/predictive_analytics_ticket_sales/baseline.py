import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import LinearRegression, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR


# Load historical ticket sales data
dataset = pd.read_csv('ticket_sales_data.csv')
print(dataset.columns)

# Prepare the data
data = dataset.values
X = data[:, :9]
y = data[:, 9]

# Split the dataset into training and validation sets
validation_size = 0.2
num_folds = 10
seed = 42
X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=validation_size, random_state=seed)

# Define the models
models = {
    'LR': LinearRegression(),
    'LASSO': Lasso(),
    'EN': ElasticNet(),
    'KNN': KNeighborsRegressor(),
    'CART': DecisionTreeRegressor(),
    'SVR': SVR(),
}

results = []
names = []

# Evaluate each model in turn using cross-validation
for name, model in models.items():
    kfold = KFold(n_splits=num_folds, shuffle=True)
    cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='neg_mean_absolute_error')
    results.append(cv_results)
    names.append(name)
    msg = f"{name}: {cv_results.mean()}, {cv_results.std()}"
    print(msg)

# Visualize the performance of the algorithms
fig = plt.figure()
fig.suptitle("Algorithms Comparison")
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()

