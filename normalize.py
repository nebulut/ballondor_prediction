import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler

# Dosyaların bulunduğu klasör yolu
input_folder_path = "seasons"
output_folder_path = "normalized_seasons"

# Klasördeki tüm CSV dosyalarını listele
csv_files = [f for f in os.listdir(input_folder_path) if f.endswith(".csv")]

# Eğer çıktı klasörü yoksa oluştur
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# Normalizasyon için scaler örneği
scaler = MinMaxScaler()

for file in csv_files:
    # CSV dosyasını oku
    df = pd.read_csv(os.path.join(input_folder_path, file))

    # 'player' ve 'WIN' sütunlarını çıkar
    features = df.drop(["player", "WIN"], axis=1)
    labels = df[["WIN"]]  # Etiketleri sakla

    # Özellikleri normalizasyon
    normalized_features = pd.DataFrame(
        scaler.fit_transform(features), columns=features.columns
    )

    # 'player' ve 'WIN' sütunlarını geri ekle
    normalized_df = pd.concat([df[["player"]], normalized_features, labels], axis=1)

    # Normalleştirilmiş DataFrame'i yeni dosyaya yaz
    normalized_df.to_csv(os.path.join(output_folder_path, file), index=False)

print("All seasons have been successfully normalized and saved.")
