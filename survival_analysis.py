import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
import pandas as pd
from lifelines import CoxPHFitter, KaplanMeierFitter
import seaborn as sns

#=====Load data=====
df = pd.read_csv(r'D:\Portofolio\telco-customer-survival-analysis\data\Telco-Customer-Churn.csv')

#Preprocessing
df['Churn'] = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'] = df['TotalCharges'].fillna(df['TotalCharges'].median())
df['tenure'] = df['tenure'].astype(int)

#Ambil fitur yang akan dipakai (hapus kolom ID dan non-numeric)
df_model = df.drop(columns=['customerID', 'gender', 'Partner', 'Dependents',
                            'PhoneService', 'MultipleLines', 'InternetService',
                            'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                            'TechSupport', 'StreamingTV', 'StreamingMovies', 'PaperlessBilling'])

#One-hot encoding untuk Contract dan PaymentMethod
df_model = pd.get_dummies(df_model, columns=['Contract', 'PaymentMethod'], drop_first=True)

#=====Fit model Cox Proportional Hazards=====
cph = CoxPHFitter()
cph.fit(df_model, duration_col='tenure', event_col='Churn')

#Tampilkan hasil
cph.print_summary()

#Grafik CoxPH
cph.plot()
plt.title("Cox Proportional Hazards Model Coefficients")
plt.switch_backend('TkAgg')
plt.show()

#=====Fit model Kaplan-Meier=====
kmf = KaplanMeierFitter()
kmf.fit(durations=df['tenure'], event_observed=df['Churn'])

#Grafik Kaplan-Meier
kmf.plot_survival_function()
plt.title("Kaplan-Meier Survival Curve")
plt.xlabel("Tenure (bulan)")
plt.ylabel("Probabilitas Bertahan (Survival Probability)")
plt.grid()
plt.switch_backend('TkAgg')
plt.show()

# Ambil kolom numerik saja
numeric_cols = df_model.select_dtypes(include='number')

# Hitung korelasi
corr_matrix = numeric_cols.corr()

# Plot heatmap
plt.figure(figsize=(14, 10))
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0,
    linewidths=0.5,
    annot_kws={"size": 7}
)
plt.title("Correlation Heatmap - Telco Customer Churn", fontsize=14, pad=15)
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.yticks(fontsize=8)
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.clf()
print("Saved: correlation_heatmap.png")

