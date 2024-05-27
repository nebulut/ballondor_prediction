import soccerdata as sd
import pandas as pd
from functions import (
    get_ucl_standings,
    get_league_standigs,
    get_wc_standigs,
    add_prefix_based_on_column,
    fill_missing_columns,
)

# pandas uyarısı için
pd.set_option("future.no_silent_downcasting", True)

#! sezon girişi
season = "23-24"

# Çeşitli istatistik kategorilerini içeren bir liste
categories = [
    "shooting",
    "passing",
    "passing_types",
    "goal_shot_creation",
    "defense",
    "possession",
    "playing_time",
    "misc",
]

#
# ŞAMPİYONLAR LİGİ (UCL) İSTATİSTİKLERİNİ OKUMA
#
ucl = sd.FBref(leagues=["UCL"], seasons=[season])

# Önce standart verileri alıyoruz
df_ucl = ucl.read_player_season_stats("standard")

# Başlıkları düzenleme, birleştirme
df_ucl.columns = ["_".join(filter(None, col)).strip() for col in df_ucl.columns.values]

# index düzenleme
df_ucl = df_ucl.reset_index()


# Diğer her kategori için istatistikleri okuyup birleştirme
df_list = []
for category in categories:
    df_category = ucl.read_player_season_stats(category)
    # Sütun adlarını kategori ismi olmadan güncelleme
    df_category.columns = [
        "_".join(filter(None, col)).strip() for col in df_category.columns.values
    ]
    df_category.reset_index(inplace=True)  # Her kategori için index'i resetleme
    df_list.append(df_category)

# Tüm DataFrames'i ilk DataFrame üzerine birleştirme
for df in df_list:
    df_ucl = pd.merge(df_ucl, df, on=["player"], how="left", suffixes=("", "_drop"))
# Birleştirmeden sonra '_drop' ile biten sütunları kaldır
df_ucl = df_ucl.loc[:, ~df_ucl.columns.str.endswith("_drop")]
# Tekrarlanan satırlar oluyordu bu nedenle onları atıyoruz
df_ucl = df_ucl.drop_duplicates(subset=["player"], keep="first")

# oynama süresine göre oyuncuları sıralama
df_ucl = df_ucl.sort_values(by="Playing Time_Min", ascending=False)

# En çok oynayan 200 oyuncudan oluşan data
df_ucl = df_ucl.head(200)

"""Amacım veri sayısını azaltmak için ucldeki en çok oynayan 200 oyuncuyu 
alıp işleri kolaylaştırmak. Burada gelen oyuncuları ileriki aşamalarda
diğer tür verileri toplarken ayıklıyorum"""
# UCL top 200 listesindeki oyuncu isimlerini bir listeye çevir
ucl_player_names = df_ucl["player"].unique()

# ucl için sıralamaları alma
ucl_standings = get_ucl_standings(ucl)

# Burada ucl istatistiklerine ucl sıralamalarını da ekliyorum
df_ucl = pd.merge(
    df_ucl,
    ucl_standings,
    left_on="team",
    right_on="Squad",
    how="left",
)

# 'Squad' sütununu sildim çünkü 'team' ile aynı
df_ucl.drop(columns=["Squad"], inplace=True)

#
# LİG İSTATİSTİKLERİNİ OKUMA
#
lg = sd.FBref(leagues="Big 5 European Leagues Combined", seasons=[season])

# önce standdart veriler
df_lg = lg.read_player_season_stats("standard")

# Başlıkları düzenleme, birleştirme
df_lg.columns = ["_".join(filter(None, col)).strip() for col in df_lg.columns.values]

# index düzenleme
df_lg = df_lg.reset_index()

# Diğer her kategori için istatistikleri okuyup birleştirme
df_list = []
for category in categories:
    df_category = lg.read_player_season_stats(category)
    # Sütun adlarını kategori ismi olmadan güncelleme
    df_category.columns = [
        "_".join(filter(None, col)).strip() for col in df_category.columns.values
    ]
    df_category.reset_index(inplace=True)  # Her kategori için index'i resetleme
    df_list.append(df_category)

# Tüm DataFrames'i ilk DataFrame üzerine birleştirme
for df in df_list:
    df_lg = pd.merge(
        df_lg,
        df,
        on=["player"],
        how="left",
        suffixes=("", "_drop"),
    )
# Birleştirmeden sonra '_drop' ile biten sütunları kaldır
df_lg = df_lg.loc[:, ~df_lg.columns.str.endswith("_drop")]
# Tekrarlanan satırlar oluyordu bu nedenle onları atıyoruz
df_lg = df_lg.drop_duplicates(subset=["player"], keep="first")

# En iyi 5 ligdeki oyuncu istatistiklerini, sadece UCL top 200 listesinde yer alan oyuncularla sınırla
df_lg = df_lg[df_lg["player"].isin(ucl_player_names)]

# Takımları ve takımların ligdeki sıralamasını döndürür
league_standings = get_league_standigs(lg)

# Burada lig istatistiklerine lig sıralamalarını da ekliyorum
df_lg = pd.merge(
    df_lg,
    league_standings,
    left_on="team",
    right_on="Squad",
    how="left",
)

# 'Squad' sütununu sildim çünkü 'team' ile aynı
df_lg.drop(columns=["Squad"], inplace=True)
# League bilgilerini standart tek yapıyorum
df_lg["league"] = "LG"

#
# DÜNYA KUPASI (WC) İSTATİSTİKLERİNİ OKUMA
#

# Sezonun Dünya Kupası sezonu olup olmadığını kontrol etme
wc_season = season
start_year = int(season.split("-")[0])
is_wc_season = (season != "21-22") and (start_year % 4 == 1) or (season == "22-23")

# Eğer Dünya Kupası sezonuysa, bir sonraki sezonun dünya kupası istatistiklerini ayarla
if is_wc_season and season != "22-23" and start_year > 5:
    wc_season = f"{start_year + 1}-{str(start_year + 2)[-2:]}"
elif start_year <= 5:
    wc_season = f"200{start_year + 1}"
else:
    wc_season = season

if is_wc_season:
    wc = sd.FBref(leagues=["WC"], seasons=[wc_season])  #!!!!!
    df_wc = wc.read_player_season_stats("standard")

    # Başlıkları düzenleme, birleştirme
    df_wc.columns = [
        "_".join(filter(None, col)).strip() for col in df_wc.columns.values
    ]

    # index düzenleme
    df_wc = df_wc.reset_index()

    # Diğer her kategori için istatistikleri okuyup birleştirme
    df_list = []
    for category in categories:
        df_category = wc.read_player_season_stats(category)
        # Sütun adlarını kategori ismi olmadan güncelleme
        df_category.columns = [
            "_".join(filter(None, col)).strip() for col in df_category.columns.values
        ]
        df_category.reset_index(inplace=True)  # Her kategori için index'i resetleme
        df_list.append(df_category)

    # Tüm DataFrames'i ilk DataFrame üzerine birleştirme
    for df in df_list:
        df_wc = pd.merge(
            df_wc,
            df,
            on=["player"],
            how="left",
            suffixes=("", "_drop"),
        )
    # Birleştirmeden sonra '_drop' ile biten sütunları kaldır
    df_wc = df_wc.loc[:, ~df_wc.columns.str.endswith("_drop")]
    # Tekrarlanan satırlar oluyordu bu nedenle onları atıyoruz
    df_wc = df_wc.drop_duplicates(subset=["player"], keep="first")

    # sıralamaları alma
    wc_standings = get_wc_standigs(wc)

    # bunda da ligdeki gibi sadece ucl ilk 200 oyuncuya bakıyoruz
    df_wc = df_wc[df_wc["player"].isin(ucl_player_names)]

    # Burada dünya kupası istatistiklerine takım başarılarını da ekliyorum
    df_wc = pd.merge(
        df_wc,
        wc_standings,
        left_on="nation",
        right_on="Squad",
        how="left",
    )

    # 'Squad' sütununu silmek isteyebilirsiniz çünkü 'Team' ile aynı bilgiyi taşır.
    df_wc.drop(columns=["Squad"], inplace=True)


else:
    # Dünya Kupası olmayan sezonlar için boş bir DataFrame oluşturma
    wc_columns = df_ucl.columns.tolist()  # Tüm sütunları ucl dataframinden alıyorum
    df_wc = pd.DataFrame(columns=wc_columns)
    df_wc["player"] = ucl_player_names  # UCL oyuncularının isimlerini ekleme
    df_wc["league"] = "WC"
    df_wc = df_wc.fillna(0).infer_objects()  # Tüm değerleri 0 ile doldurduk

#
# VERİLERİ DÜZENLEME TÜM SEZONLARI BİRLEŞTİRME
#
# Gereksiz sütunları kaldırma
columns_to_drop = ["team", "nation", "age", "born", "season", "pos"]
df_ucl.drop(
    columns=[col for col in columns_to_drop if col in df_ucl.columns], inplace=True
)
df_lg.drop(
    columns=[col for col in columns_to_drop if col in df_lg.columns], inplace=True
)
columns_to_drop.append("Club")
df_wc.drop(
    columns=[col for col in columns_to_drop if col in df_wc.columns], inplace=True
)

# 17-18'den önceki sezonlarda bazı istatistikler olmadığı için onları manuel ekleyip 0'lıyoruz
if int(season.split("-")[0]) < 17:
    df_ucl = fill_missing_columns(df_ucl)
    df_lg = fill_missing_columns(df_lg)
    df_wc = fill_missing_columns(df_wc)

# Veriler birleştiğinde karışmaması için her istatistiğe ligini belirten prefix eklendi
df_ucl = add_prefix_based_on_column(df_ucl, "league", ["league", "player"])
df_lg = add_prefix_based_on_column(df_lg, "league", ["league", "player"])
df_wc = add_prefix_based_on_column(df_wc, "league", ["league", "player"])

# lig bilgisi kaldırıldı
df_ucl.drop(columns=["league"], inplace=True)
df_lg.drop(columns=["league"], inplace=True)
df_wc.drop(columns=["league"], inplace=True)

# DataFrame'leri birleştirelim
df_merged = pd.merge(df_lg, df_ucl, on="player", how="outer")
df_merged = pd.merge(df_merged, df_wc, on="player", how="outer")
# df_merged = df_merged.dropna() ilk başta olmayan değerleri silmiştim
# ancak daha sonradan bir diğer listede olmayan değerleri 0 yapmak daha mantıklı geldi
df_merged = df_merged.fillna(0)

# WC_Rk sütununda 0 olan değerleri 8 yap. Bunun nedeni wc oynanan
# yıllarda oynamayan oyuncuların sıralamasını diğer oyunculardan düşük yapmak
df_merged["WC_Rk"] = df_merged["WC_Rk"].replace(0, 8)

# burada da top5 ligte olmayan oyuncuların sırasını düşürme
df_merged["LG_Rk"] = df_merged["LG_Rk"].replace(0, 20)

# 'WIN' sütunu ekledim balondor kazananı belirlemek için
df_merged["WIN"] = 0

# Kazananları içeren dosyadan kazananı belirleme ve 1 olarak ayarlama
winners = pd.read_csv("winners.csv")

# 17-18 ve sonrasındaki sezonlarda bazı olmayan istatistikler eski
# sezonlarda yer almakta bunları kaldırıyoruz 17-18 öncesi için
if start_year < 17:
    columns_to_drop = [
        "WC_Rec",
        "LG_Rec",
        "LG_A-xAG",
        "WC_A-xAG",
        "UCL_Rec",
        "UCL_A-xAG",
    ]
    df_merged = df_merged.drop(columns=columns_to_drop)

try:
    winner = winners.loc[winners["season"] == season, "winner"].values[0]
    df_merged.loc[df_merged["player"] == winner, "WIN"] = 1
except IndexError:
    pass

df_merged.to_csv(f"seasons/{season}.csv", index=False)

print(f"{season} season statistics has been received successfully.")
