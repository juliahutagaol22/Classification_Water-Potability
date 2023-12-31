# -*- coding: utf-8 -*-
"""Juliawati Hutagaol_119140016_TUGAS AKHIR WATER Quality.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1W00-pXZPV99CC8pJQYdtYiQZtgiHmzT7

Urutan proses untuk pengerjaan:

1. Pengumpulan Data
2. Data Cleaning, Data Transformation
3. Balancing Dataset
4. Penerapan Algoritma Random Forest
5. Evaluasi Model
"""

#Import Library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.model_selection import GridSearchCV

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv("/content/drive/MyDrive/Dataset/waterQuality.csv")

df

# Mengganti nilai 0 menjadi NaN kecuali pada nilai target
df.iloc[:, :-1] = df.iloc[:, :-1].replace(["#NUM!",0], np.nan)

df

df.info()

df.describe()

"""# 2.A DATA CLEANING"""

display("Total data yang terduplikasi: %s" %df.duplicated().sum())

"""Handling Missing Value"""

df.isnull().sum()

missed_data = df.isnull().sum()
missed_data.sum()

total_data = np.product(df.shape)
percentage = missed_data.sum()/total_data
percentage*100

#handling missing value dengan KNN Imputer pada dataset
from sklearn.impute import KNNImputer
impute_knn=KNNImputer()
df=impute_knn.fit_transform(df)

# Mengubah array NumPy menjadi DataFrame Pandas
df= pd.DataFrame(df)
df.isnull().sum()

df.columns = ["aluminium","ammonia","arsenic","barium","cadmium","chloramine","chromium","copper","flouride","bacteria","viruses","lead","nitrates","nitrites","mercury","perchlorate","radium","selenium","silver","uranium","is_safe"]
# Mengubah kolom Target menjadi tipe data integer
df['is_safe'] = df['is_safe'].astype(int)

df.isnull().sum()

df

"""# 2.B NORMALISASI MINMAX"""

from sklearn.preprocessing import MinMaxScaler

# Normalisasi data
scaling =  ["aluminium","ammonia","arsenic","barium","cadmium","chloramine","chromium","copper","flouride","bacteria","viruses","lead","nitrates","nitrites","mercury","perchlorate","radium","selenium","silver","uranium"]

# Pisahkan kolom target
target = df['is_safe']
features = df.drop('is_safe', axis=1)

# Membuat objek MinMaxScaler
scaler = MinMaxScaler()

# Melakukan scaling pada fitur-fitur yang dipilih
features_scaled = scaler.fit_transform(features[scaling])

# Menggabungkan kembali fitur-fitur yang sudah di-scaling dengan kolom target
df_scaled = pd.DataFrame(features_scaled, columns=scaling)
df_scaled['is_safe'] = target

# Menampilkan DataFrame setelah scaling
df_scaled

"""Spliting Dataset"""

X = df_scaled.drop('is_safe', axis=1)
y = df_scaled['is_safe']

#Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(X_train.shape,
X_test.shape,"\n",
y_train.shape,
y_test.shape)

X_train

y_train

X_test

y_test

"""# Performansi Model tanpa melakukan Balancing Dataset"""

rf1 = RandomForestClassifier(n_estimators=20, max_features='sqrt', random_state=42)
rf1.fit(X_train, y_train)

y_pred = rf1.predict(X_test)

print(classification_report(y_test,y_pred))

cm = confusion_matrix(y_test, y_pred, labels=[1,0])
print(cm)
# Membuat plot confusion matrix
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True,fmt='d', cbar=False)

# Menambahkan label pada sumbu x dan y
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')

# Menampilkan plot
plt.show()

"""# 3.A Balancing dataset dengan Random Oversampling"""

df_scaled['is_safe'].value_counts()

sns.countplot(x="is_safe", data=df_scaled)

print(y_train.value_counts())

from imblearn.over_sampling import RandomOverSampler
# Inisialisasi RandomOverSampler
ros = RandomOverSampler(random_state=42)
# Melakukan random oversampling
X_resampled, y_resampled = ros.fit_resample(X_train, y_train)
# Menggabungkan fitur dan target yang telah diresampling menjadi DataFrame baru
df_resampled = pd.concat([pd.DataFrame(X_resampled, columns=X.columns), pd.Series(y_resampled, name='Target')], axis=1)

# cek jumlah data pada masing-masing kelas setelah oversampling
print(y_resampled.value_counts())

df_oversampled = pd.concat([X_resampled, y_resampled.rename('is_safe')], axis=1)
# Menampilkan jumlah kelas setelah oversampling
class_counts = df_oversampled['is_safe'].value_counts()
print(class_counts)

# Menampilkan snsplot
sns.countplot(x='is_safe', data=df_oversampled)

"""Hyperparamameter Tuning menggunakan GridSearchCV"""

param_grid = {
    'n_estimators': [20,100,200,300],
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth' : [None,3,4,5],
    'criterion' :['gini', 'entropy']
}

rfc2=RandomForestClassifier(random_state=42)
CV_rfc2 = GridSearchCV(estimator=rfc2, param_grid=param_grid)
CV_rfc2.fit(X_resampled, y_resampled)

CV_rfc2.best_params_

rf2 = RandomForestClassifier(n_estimators=20, criterion='entropy', max_depth=None, max_features='auto' ,random_state=42)

rf2.fit(X_resampled, y_resampled)

y_pred_ros= rf2.predict(X_test)

print(classification_report(y_test,y_pred_ros))

cm_ros = confusion_matrix(y_test, y_pred_ros, labels=[1,0])
print(cm_ros)
# Membuat plot confusion matrix
plt.figure(figsize=(6, 4))
sns.heatmap(cm_ros, annot=True,fmt='d', cbar=False)

# Menambahkan label pada sumbu x dan y
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')

# Menampilkan plot
plt.show()

"""# 3.B Balancing Dataset dengan SMOTE"""

from imblearn.over_sampling import SMOTE
# Inisialisasi SMOTE
smote = SMOTE(k_neighbors=1,random_state=42)

# Oversampling pada X_train dan y_train
X_oversampled, y_oversampled = smote.fit_resample(X_train, y_train)

df_Balanced = pd.concat([X_oversampled, y_oversampled.rename('is_safe')], axis=1)
# Menampilkan jumlah kelas setelah oversampling
class_counts = df_Balanced['is_safe'].value_counts()
print(class_counts)

# Menampilkan snsplot
sns.countplot(x='is_safe', data=df_Balanced)

"""Hyperparameter Tuning menggunakan GridSearchCV"""

param_grid = {
    'n_estimators': [20,100,200,300],
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth' : [None,3,4,5],
    'criterion' :['gini', 'entropy']
}

rfc3=RandomForestClassifier(random_state=42)
CV_rfc3 = GridSearchCV(estimator=rfc3, param_grid=param_grid)
CV_rfc3.fit(X_oversampled, y_oversampled)

CV_rfc3.best_params_

rf3 = RandomForestClassifier(n_estimators=300, criterion='entropy', max_depth=None, max_features='auto', random_state=42)

rf3.fit(X_oversampled, y_oversampled)

y_pred_smote = rf3.predict(X_test)

print(classification_report(y_test,y_pred_smote))

cm_smote = confusion_matrix(y_test, y_pred_smote, labels=[1,0])
print(cm_smote)
# Membuat plot confusion matrix
plt.figure(figsize=(6, 4))
sns.heatmap(cm_smote, annot=True,fmt='d', cbar=False)

# Menambahkan label pada sumbu x dan y
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')

# Menampilkan plot
plt.show()