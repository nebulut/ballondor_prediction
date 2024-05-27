import pandas as pd


def get_league_standigs(league):
    # Sezon bilgilerini oku ve indexi sıfırla
    df = league.read_seasons().reset_index()

    # İlk URL'yi al (bu örnekte tüm URL'ler üzerinde dönüş yapabilirsiniz)
    url = df["url"].iloc[0]

    # Tam URL'yi oluştur
    full_url = f"https://fbref.com{url}"

    # tam tabloyu al
    table = pd.read_html(full_url, attrs={"id": "big5_table"})

    # Tablolar listesinden ilk DataFrame'i al (genellikle tek bir tablo döner)
    if table:
        league_table = table[0]
        # Sadece 'LgRk' ve 'Squad' sütunlarını al
        league_table = league_table[["LgRk", "Squad"]]
        league_table = league_table.copy()
        league_table.rename(columns={"LgRk": "Rk"}, inplace=True)
        return league_table
    else:
        print("No tables found.")
        return pd.DataFrame(columns=["Rk", "Squad"])


def get_ucl_standings(league):
    # Sezon bilgilerini oku ve indexi sıfırla
    df = league.read_seasons().reset_index()

    # İlk URL'yi al (bu örnekte tüm URL'ler üzerinde dönüş yapabilirsiniz)
    url = df["url"].iloc[0]

    # Tam URL'yi oluştur
    full_url = f"https://fbref.com{url}"

    # Sezon bilgilerini formatlayarak alalım
    if df["season"].apply(lambda x: int(x[:2]))[0] < 50:
        season_id = df["season"].apply(lambda x: f"20{x[:2]}-20{x[2:]}").iloc[0]
    elif df["season"].apply(lambda x: int(x[:2])).iloc[0] == 99:
        season_id = "1999-2000"
    else:
        season_id = df["season"].apply(lambda x: f"19{x[:2]}-19{x[2:]}").iloc[0]

    # Dinamik id oluşturma
    table_id = f"results{season_id}80_overall"

    # Tam tabloyu al
    table = pd.read_html(full_url, attrs={"id": table_id})

    # Tablolar listesinden ilk DataFrame'i al (genellikle tek bir tablo döner)
    if table:
        league_table = table[0]
        # Sadece 'LgRk' ve 'Squad' sütunlarını al ve boş satırları sil döndür
        league_table = league_table[["Rk", "Squad"]]
        # boş satırları sil
        league_table = league_table.dropna(subset=["Rk"])
        # takım isimlerini uygun şekilde diğer dataframelere göre düzenleme
        league_table["Squad"] = league_table["Squad"].str.replace(
            r"^\w+\s", "", regex=True
        )
        # Sıralama değerlerini sayısal değerlere dönüştür
        ranking_map = {
            "1": 1,  # Şampiyon
            "2": 2,  # İkinci
            "SF": 3,  # Yarı final
            "QF": 4,  # Çeyrek final
            "R16": 5,  # Son 16
            "GR": 6,  # Grup aşaması
            "W": 1,  # Şampiyon (Geçmiş yıl verilerinde 1 yerine w yazıyor)
            "F": 2,  # İkinci (2 yerine F)
        }
        league_table["Rk"] = league_table["Rk"].map(ranking_map)
        return league_table
    else:
        print("No tables found.")
        return pd.DataFrame(columns=["Rk", "Squad"])


def get_wc_standigs(league):
    # Sezon bilgilerini oku ve indexi sıfırla
    df = league.read_seasons().reset_index()

    # İlk URL'yi al (bu örnekte tüm URL'ler üzerinde dönüş yapabilirsiniz)
    url = df["url"].iloc[0]

    # Tam URL'yi oluştur
    full_url = f"https://fbref.com{url}"

    # güncel sezon urlsinde yıl bilgisi olmadığı için kontrol ediyoruz
    season_id = df["season"].str[:2].apply(lambda x: f"20{x}").iloc[0]

    # Dinamik id oluşturma
    table_id = f"results{season_id}10_overall"

    # Tam tabloyu al
    table = pd.read_html(full_url, attrs={"id": table_id})

    # Tablolar listesinden ilk DataFrame'i al (genellikle tek bir tablo döner)
    if table:
        league_table = table[0]
        # Sadece 'LgRk' ve 'Squad' sütunlarını al ve boş satırları sil döndür
        league_table = league_table[["Rk", "Squad"]]
        # boş satırları sil
        league_table = league_table.dropna(subset=["Rk"])
        # ülke isimlerini uygun şekilde diğer dataframelere göre düzenleme
        league_table["Squad"] = league_table["Squad"].str.replace(
            r"^\w+\s", "", regex=True
        )
        # Sıralama değerlerini sayısal değerlere dönüştür
        ranking_map = {
            "1": 1,  # 1. sırada
            "2": 2,  # 2. sırada
            "3": 3,  # 3. sırada
            "4": 4,  # 4. sırada
            "QF": 5,  # Çeyrek final
            "R16": 6,  # Son 16
            "GR": 7,  # Grup aşaması
        }
        league_table["Rk"] = league_table["Rk"].map(ranking_map)
        return league_table
    else:
        print("No tables found.")
        return pd.DataFrame(columns=["Rk", "Squad"])


# data framede her istatistik için ligini belirten eki ekleme
def add_prefix_based_on_column(df, prefix_column, exclude_columns):
    prefix = df[prefix_column].iloc[0]  # İlk satırdaki league değerini kullanıyoruz
    new_columns = {}
    for col in df.columns:
        if col not in exclude_columns:
            new_columns[col] = (
                f"{prefix}_{col}"  # League değeriyle yeni sütun adı oluştur
            )
        else:
            new_columns[col] = col  # Diğer sütun adlarını değiştirme
    df = df.rename(columns=new_columns)
    return df


def fill_missing_columns(df):
    full_columns = [
        "league",
        "player",
        "Playing Time_MP",
        "Playing Time_Starts",
        "Playing Time_Min",
        "Playing Time_90s",
        "Performance_Gls",
        "Performance_Ast",
        "Performance_G+A",
        "Performance_G-PK",
        "Performance_PK",
        "Performance_PKatt",
        "Performance_CrdY",
        "Performance_CrdR",
        "Expected_xG",
        "Expected_npxG",
        "Expected_xAG",
        "Expected_npxG+xAG",
        "Progression_PrgC",
        "Progression_PrgP",
        "Progression_PrgR",
        "Per 90 Minutes_Gls",
        "Per 90 Minutes_Ast",
        "Per 90 Minutes_G+A",
        "Per 90 Minutes_G-PK",
        "Per 90 Minutes_G+A-PK",
        "Per 90 Minutes_xG",
        "Per 90 Minutes_xAG",
        "Per 90 Minutes_xG+xAG",
        "Per 90 Minutes_npxG",
        "Per 90 Minutes_npxG+xAG",
        "90s",
        "Standard_Gls",
        "Standard_Sh",
        "Standard_SoT",
        "Standard_SoT%",
        "Standard_Sh/90",
        "Standard_SoT/90",
        "Standard_G/Sh",
        "Standard_G/SoT",
        "Standard_Dist",
        "Standard_FK",
        "Standard_PK",
        "Standard_PKatt",
        "Expected_npxG/Sh",
        "Expected_G-xG",
        "Expected_np:G-xG",
        "Total_Cmp",
        "Total_Att",
        "Total_Cmp%",
        "Total_TotDist",
        "Total_PrgDist",
        "Short_Cmp",
        "Short_Att",
        "Short_Cmp%",
        "Medium_Cmp",
        "Medium_Att",
        "Medium_Cmp%",
        "Long_Cmp",
        "Long_Att",
        "Long_Cmp%",
        "Ast",
        "xAG",
        "Expected_xA",
        "Expected_A-xAG",
        "KP",
        "1/3",
        "PPA",
        "CrsPA",
        "PrgP",
        "Att",
        "Pass Types_Live",
        "Pass Types_Dead",
        "Pass Types_FK",
        "Pass Types_TB",
        "Pass Types_Sw",
        "Pass Types_Crs",
        "Pass Types_TI",
        "Pass Types_CK",
        "Corner Kicks_In",
        "Corner Kicks_Out",
        "Corner Kicks_Str",
        "Outcomes_Cmp",
        "Outcomes_Off",
        "Outcomes_Blocks",
        "SCA_SCA",
        "SCA_SCA90",
        "SCA Types_PassLive",
        "SCA Types_PassDead",
        "SCA Types_TO",
        "SCA Types_Sh",
        "SCA Types_Fld",
        "SCA Types_Def",
        "GCA_GCA",
        "GCA_GCA90",
        "GCA Types_PassLive",
        "GCA Types_PassDead",
        "GCA Types_TO",
        "GCA Types_Sh",
        "GCA Types_Fld",
        "GCA Types_Def",
        "Tackles_Tkl",
        "Tackles_TklW",
        "Tackles_Def 3rd",
        "Tackles_Mid 3rd",
        "Tackles_Att 3rd",
        "Challenges_Tkl",
        "Challenges_Att",
        "Challenges_Tkl%",
        "Challenges_Lost",
        "Blocks_Blocks",
        "Blocks_Sh",
        "Blocks_Pass",
        "Int",
        "Tkl+Int",
        "Clr",
        "Err",
        "Touches_Touches",
        "Touches_Def Pen",
        "Touches_Def 3rd",
        "Touches_Mid 3rd",
        "Touches_Att 3rd",
        "Touches_Att Pen",
        "Touches_Live",
        "Take-Ons_Att",
        "Take-Ons_Succ",
        "Take-Ons_Succ%",
        "Take-Ons_Tkld",
        "Take-Ons_Tkld%",
        "Carries_Carries",
        "Carries_TotDist",
        "Carries_PrgDist",
        "Carries_PrgC",
        "Carries_1/3",
        "Carries_CPA",
        "Carries_Mis",
        "Carries_Dis",
        "Receiving_Rec",
        "Receiving_PrgR",
        "Playing Time_Mn/MP",
        "Playing Time_Min%",
        "Starts_Starts",
        "Starts_Mn/Start",
        "Starts_Compl",
        "Subs_Subs",
        "Subs_Mn/Sub",
        "Subs_unSub",
        "Team Success_PPM",
        "Team Success_onG",
        "Team Success_onGA",
        "Team Success_+/-",
        "Team Success_+/-90",
        "Team Success_On-Off",
        "Team Success (xG)_onxG",
        "Team Success (xG)_onxGA",
        "Team Success (xG)_xG+/-",
        "Team Success (xG)_xG+/-90",
        "Team Success (xG)_On-Off",
        "Performance_2CrdY",
        "Performance_Fls",
        "Performance_Fld",
        "Performance_Off",
        "Performance_Crs",
        "Performance_Int",
        "Performance_TklW",
        "Performance_PKwon",
        "Performance_PKcon",
        "Performance_OG",
        "Performance_Recov",
        "Aerial Duels_Won",
        "Aerial Duels_Lost",
        "Aerial Duels_Won%",
        "Rk",
    ]
    # 'full_columns' tüm olması gereken sütunları içerir
    missing_cols = set(full_columns) - set(df.columns)
    # Eksik sütunlar için sıfır değerleri ile DataFrame oluştur
    # Her sütun için df'in uzunluğu kadar sıfır içeren bir liste oluştur
    missing_data = {col: [0] * len(df) for col in missing_cols}
    missing_df = pd.DataFrame(missing_data, index=df.index)
    # Mevcut DataFrame ile birleştir
    df = pd.concat([df, missing_df], axis=1)
    return df
