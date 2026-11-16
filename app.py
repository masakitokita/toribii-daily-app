import datetime
import os
import pandas as pd
import streamlit as st

# --- ページ設定 ---
st.set_page_config(
    page_title="炭火バル とりびぃーの 日報・管理システム",
    page_icon="🏮",
    layout="wide",
)

# --- CSVデータ保存ファイル名 ---
DATA_FILE = "toribii_daily_data.csv"


# --- 過去データを含む初期データの読み込み・作成 ---
def load_data():
  if os.path.exists(DATA_FILE):
    try:
      df = pd.read_csv(DATA_FILE)
      df["日時"] = pd.to_datetime(df["日時"])
      return df
    except Exception:
      pass

  # 過去の売上データ（8月、9月、10月、11月）の完全版サンプルデータ
  initial_data = []

  # 8月データ生成（24営業日分）
  for day in range(1, 32):
    try:
      dt = datetime.date(2026, 8, day)
      # 日曜（weekday == 6）は基本休業(0円)、他は営業日としてサンプル売上を設定
      if dt.weekday() == 6:
        sales, groups, customers, labor = 0, 0, 0, 0
      else:
        sales = 95000 + (day * 1300) % 60000
        groups = 6 + (day % 6)
        customers = 15 + (day % 15)
        labor = 35600
      initial_data.append({
          "日時": pd.Timestamp(dt),
          "Uレジ売上": sales,
          "組数": groups,
          "客数": customers,
          "人件費": labor,
          "瀬島": 8000 if sales > 0 else 0,
          "川島食品": 3000 if sales > 0 else 0,
      })
    except ValueError:
      break

  # 9月データ生成
  for day in range(1, 31):
    try:
      dt = datetime.date(2026, 9, day)
      if dt.weekday() == 6:
        sales, groups, customers, labor = 0, 0, 0, 0
      else:
        sales = 98000 + (day * 1500) % 58000
        groups = 6 + (day % 6)
        customers = 16 + (day % 14)
        labor = 35600
      initial_data.append({
          "日時": pd.Timestamp(dt),
          "Uレジ売上": sales,
          "組数": groups,
          "客数": customers,
          "人件費": labor,
          "瀬島": 8500 if sales > 0 else 0,
          "川島食品": 3200 if sales > 0 else 0,
      })
    except ValueError:
      break

  # 10月データ生成
  for day in range(1, 32):
    try:
      dt = datetime.date(2026, 10, day)
      if dt.weekday() == 6:
        sales, groups, customers, labor = 0, 0, 0, 0
      else:
        sales = 100000 + (day * 1400) % 60000
        groups = 7 + (day % 5)
        customers = 18 + (day % 12)
        labor = 36000
      initial_data.append({
          "日時": pd.Timestamp(dt),
          "Uレジ売上": sales,
          "組数": groups,
          "客数": customers,
          "人件費": labor,
          "瀬島": 9000 if sales > 0 else 0,
          "川島食品": 3500 if sales > 0 else 0,
      })
    except ValueError:
      break

  # 11月データ（途中経過含む）
  nov_data = [
      ("2026-11-01", 0, 0, 0, 0, 0, 0),
      ("2026-11-02", 116930, 8, 22, 35600, 8500, 4200),
      ("2026-11-03", 67947, 5, 12, 32000, 4000, 3100),
      ("2026-11-04", 87153, 4, 11, 32000, 6200, 2800),
      ("2026-11-05", 95400, 7, 19, 35600, 7100, 3500),
      ("2026-11-06", 142000, 11, 30, 40000, 12000, 6000),
      ("2026-11-07", 155000, 12, 33, 42000, 15000, 7500),
      ("2026-11-08", 0, 0, 0, 0, 0, 0),
      ("2026-11-09", 0, 0, 0, 0, 0, 0),
      ("2026-11-10", 98000, 7, 18, 33000, 5000, 2500),
      ("2026-11-11", 89000, 6, 16, 33000, 4800, 2200),
      ("2026-11-12", 105000, 8, 21, 35600, 6500, 3000),
      ("2026-11-13", 152392, 12, 34, 42000, 14000, 6800),
      ("2026-11-14", 140670, 10, 28, 35600, 9716, 0),
  ]
  for dt_str, sales, grp, cust, lab, sej, kaw in nov_data:
    initial_data.append({
        "日時": pd.to_datetime(dt_str),
        "Uレジ売上": sales,
        "組数": grp,
        "客数": cust,
        "人件費": lab,
        "瀬島": sej,
        "川島食品": kaw,
    })

  df = pd.DataFrame(initial_data)
  df.to_csv(DATA_FILE, index=False)
  return df


# セッションステートで保持
if "df_data" not in st.session_state:
  st.session_state.df_data = load_data()

df_data = st.session_state.df_data

# --- 共通ヘッダー ---
st.title("炭火バル とりびぃーの")
st.markdown("店舗スタッフ用日報・仕入管理・経営ダッシュボードシステム")

# タブの構成
tab_input, tab_dashboard, tab_admin = st.tabs(
    ["日報・仕入送信", "📊 経営ダッシュボード【仮案1】", "管理者画面"]
)

# ==========================================
# 1. 日報
