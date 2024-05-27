import pandas as pd
import os
from sklearn.linear_model import LogisticRegression
from joblib import dump

# Eğitim verilerini yüklemek için klasör yolu
input_folder_path = "normalized_seasons"

# Klasördeki tüm CSV dosyalarını listele
csv_files = [f for f in os.listdir(input_folder_path) if f.endswith(".csv")]

# Tüm verileri bir DataFrame'de birleştir
all_data = pd.DataFrame()
for file in csv_files:
    df = pd.read_csv(os.path.join(input_folder_path, file))
    all_data = pd.concat([all_data, df], ignore_index=True)

# Özellikler ve etiketler
features = all_data.drop(["player", "WIN"], axis=1)
labels = all_data["WIN"]

# Modeli oluştur ve eğit
model = LogisticRegression(max_iter=10000000)
model.fit(features, labels)

# Eğitim sırasında kullanılan iterasyon sayısını yazdır
print("Number of iterations:", model.n_iter_[0])

# Modeli dosyaya kaydet
dump(model, "logistic_regression_model.joblib")

# Eğitim sırasında kullanılan özelliklerin sırasını kaydedin çünkü test sırasında sıralar farklı olabilir
feature_columns = list(features.columns)
# Özellik sütunlarını bir dosyaya kaydedin
pd.Series(feature_columns).to_csv("feature_columns.csv", index=False, header=False)

print("The model has been successfully trained and registered.")
