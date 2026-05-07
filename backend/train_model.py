import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# load dataset
df = pd.read_csv("livestock_symptoms_dataset.csv")

# split
X = df.drop("disease", axis=1)
y = df["disease"]

# train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# accuracy
print("Accuracy:", model.score(X_test, y_test))

# save model
joblib.dump(model, "symptom_model.pkl")