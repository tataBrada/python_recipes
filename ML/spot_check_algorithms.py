import numpy as np
from pandas import read_csv
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score, KFold, train_test_split
from sklearn.datasets import make_classification


# Read the dataset from a CSV file
dataset = read_csv('datasets/sonar.csv', header=None)
print(f"Shape of Dataset: {dataset.shape}")

# Convert the dataset to numpy array
data = dataset.values
X = data[:, 0:60].astype(float)
y = data[:, 60]

# Split the dataset into training and validation sets
validation_size = 0.25
num_fold = 10
seed = 42
X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=validation_size, random_state=seed)

# Define the models
models = {
    'LR': LogisticRegression(),
    'LDA': LinearDiscriminantAnalysis(),
    'QDA': QuadraticDiscriminantAnalysis(),
    'KNN': KNeighborsClassifier(),
    'CART': DecisionTreeClassifier(),
    'NB': GaussianNB(),
    'SVM': SVC()
}

results = []
names = []

# Evaluate each model in turn using cross-validation
for name, model in models.items():
    kfold = KFold(n_splits=num_fold)
    cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
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
