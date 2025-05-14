from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="Surabhi",
    user="root",
    password="Goldy@2406",
    database="income_prediction"
)

# Fetch data
df = pd.read_sql("SELECT * FROM income_data", conn)

# Categorical columns
cols_to_encode = ['workclass', 'education', 'marital_status', 'occupation',
                 'relationship', 'race', 'sex', 'native_country']

le_dict = {}

for col in cols_to_encode:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    le_dict[col] = le

# Feature order must match exactly
X = df[['age', 'workclass', 'education', 'education_num', 'marital_status',
       'occupation', 'relationship', 'race', 'sex', 'capital_gain',
       'capital_loss', 'hours_per_week', 'native_country']]
y = df['income'].apply(lambda x: 1 if x == '>50K' else 0)

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, 'models/income_model.pkl')
joblib.dump(le_dict, 'models/label_encoders.pkl')

print("✅ Model trained and saved successfully!")