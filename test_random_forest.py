import pandas as pd
from joblib import load
from sklearn.preprocessing import MinMaxScaler

season = "23-24"  #! sezon


def load_and_predict(test_data_path, model_path, feature_columns_path):
    # Modeli yükle
    model = load(model_path)

    # Tahmin yapılacak veriyi yükle
    test_df = pd.read_csv(test_data_path)

    # Veri ön işleme
    # Önce 'Unnamed: 0' ve diğer gereksiz sütunları kaldırın
    if "Unnamed: 0" in test_df.columns:
        test_df.drop(columns="Unnamed: 0", inplace=True)

    # Kaydedilen özellik sütunlarını yükleyin
    feature_columns = pd.read_csv(feature_columns_path, header=None).squeeze().tolist()

    # 'player' ve 'WIN' sütunlarını sakla
    players = test_df["player"]
    win_labels = test_df["WIN"]

    # Özellikleri ayır ve doğru sırayla düzenleyin
    features = test_df.drop(["player", "WIN"], axis=1)
    features = features[feature_columns]

    # Özellikleri ölçeklendir (eğer model eğitiminde ölçeklendirme yapıldıysa)
    scaler = MinMaxScaler()
    features_scaled = pd.DataFrame(
        scaler.fit_transform(features), columns=features.columns
    )

    # Tahmin yap
    predictions = model.predict_proba(features_scaled)[
        :, 1
    ]  # Kazanma olasılıklarını al

    # Tahmin sonuçlarını yüzde olarak DataFrame'e ekle
    test_df["Win Probability"] = predictions * 100
    # Sonuçları 'Win Probability' göre azalan sıralama yap
    test_df.sort_values(by="Win Probability", ascending=False, inplace=True)

    # Tahminleri normalleştirme
    total_probability = test_df["Win Probability"].sum()
    test_df["Normalized Win Probability"] = (
        test_df["Win Probability"] / total_probability
    ) * 100

    # Normalleştirilmiş sonuçları 'Normalized Win Probability' göre azalan sıralama yap
    sorted_df = test_df.sort_values(by="Normalized Win Probability", ascending=False)

    # 'player' sütununu kontrol edip ekleyin
    if "player" not in sorted_df.columns:
        sorted_df.insert(0, "player", players)

    return sorted_df


# Test edilecek verinin ve modelin yollarını belirtin
test_data_path = f"to_predict/{season}.csv"  # Bu yolu değiştirin
model_path = "random_forest_model.joblib"  # Bu yolu değiştirin
feature_columns_path = "feature_columns.csv"  # Bu yolu değiştirin

# Tahminleri yap ve sonucu al
sorted_df = load_and_predict(test_data_path, model_path, feature_columns_path)

# Sonuçları yazdır veya kaydet
print(sorted_df[["player", "Win Probability", "Normalized Win Probability"]])

# Sonuçları kaydet
sorted_df.to_csv(
    f"results/random_forest/result_{season}.csv",
    columns=["player", "Normalized Win Probability"],
    index=False,
)
