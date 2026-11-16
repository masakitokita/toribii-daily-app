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


# --- 初期データの読み込み・作成 ---
def load_data():
  if os.path.exists(DATA_FILE):
    try:
      df = pd.read_csv(DATA_FILE)
      df["日時"] = pd.to_datetime(df["日時"])
      return df
    except Exception:
      pass

  # 初期サンプルデータ（11月途中経過含む）
  initial_data = [
      {
          "日時": "2026-08-01",
          "Uレジ売上": 101068,
          "組数": 6,
          "客数": 16,
          "人件費": 35600,
          "瀬島": 9500,
          "川島食品": 0,
      },
      {
          "日時": "2026-08-02",
          "Uレジ売上": 81587,
          "組数": 6,
          "客数": 17,
          "人件費": 35600,
          "瀬島": 0,
          "川島食品": 5400,
      },
      {
          "日時": "2026-11-01",
          "Uレジ売上": 0,
          "組数": 0,
          "客数": 0,
          "人件費": 0,
          "瀬島": 0,
          "川島食品": 0,
      },
      {
          "日時": "2026-11-02",
          "Uレジ売上": 116930,
          "組数": 8,
          "客数": 22,
          "人件費": 35600,
          "瀬島": 8500,
          "川島食品": 4200,
      },
      {
          "日時": "2026-11-03",
          "Uレジ売上": 67947,
          "組数": 5,
          "客数": 12,
          "人件費": 32000,
          "瀬島": 4000,
          "川島食品": 3100,
      },
      {
          "日時": "2026-11-04",
          "Uレジ売上": 87153,
          "組数": 4,
          "客数": 11,
          "人件費": 32000,
          "瀬島": 6200,
          "川島食品": 2800,
      },
      {
          "日時": "2026-11-05",
          "Uレジ売上": 95400,
          "組数": 7,
          "客数": 19,
          "人件費": 35600,
          "瀬島": 7100,
          "川島食品": 3500,
      },
      {
          "日時": "2026-11-06",
          "Uレジ売上": 142000,
          "組数": 11,
          "客数": 30,
          "人件費": 40000,
          "瀬島": 12000,
          "川島食品": 6000,
      },
      {
          "日時": "2026-11-07",
          "Uレジ売上": 155000,
          "組数": 12,
          "客数": 33,
          "人件費": 42000,
          "瀬島": 15000,
          "川島食品": 7500,
      },
      {
          "日時": "2026-11-08",
          "Uレジ売上": 0,
          "組数": 0,
          "客数": 0,
          "人件費": 0,
          "瀬島": 0,
          "川島食品": 0,
      },
      {
          "日時": "2026-11-09",
          "Uレジ売上": 0,
          "組数": 0,
          "客数": 0,
          "人件費": 0,
          "瀬島": 0,
          "川島食品": 0,
      },
      {
          "日時": "2026-11-10",
          "Uレジ売上": 98000,
          "組数": 7,
          "客数": 18,
          "人件費": 33000,
          "瀬島": 5000,
          "川島食品": 2500,
      },
      {
          "日時": "2026-11-11",
          "Uレジ売上": 89000,
          "組数": 6,
          "客数": 16,
          "人件費": 33000,
          "瀬島": 4800,
          "川島食品": 2200,
      },
      {
          "日時": "2026-11-12",
          "Uレジ売上": 105000,
          "組数": 8,
          "客数": 21,
          "人件費": 35600,
          "瀬島": 6500,
          "川島食品": 3000,
      },
      {
          "日時": "2026-11-13",
          "Uレジ売上": 152392,
          "組数": 12,
          "客数": 34,
          "人件費": 42000,
          "瀬島": 14000,
          "川島食品": 6800,
      },
      {
          "日時": "2026-11-14",
          "Uレジ売上": 140670,
          "組数": 10,
          "客数": 28,
          "人件費": 35600,
          "瀬島": 9716,
          "川島食品": 0,
      },
  ]
  df = pd.DataFrame(initial_data)
  df["日時"] = pd.to_datetime(df["日時"])
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
    ["日報・仕入送信", "📊 経営ダッシュボード（仮案1）", "管理者画面"]
)

# ==========================================
# 1. 日報・仕入送信タブ
# ==========================================
with tab_input:
  st.subheader("日報・売上・原価入力")

  with st.form("daily_report_form"):
    col1, col2 = st.columns(2)
    with col1:
      input_date = st.date_input(
          "営業日", value=datetime.date(2026, 11, 14)
      )
    with col2:
      sales = st.number_input(
          "Uレジ売上金額（円）", min_value=0, value=140670, step=1000
      )

    col3, col4 = st.columns(2)
    with col3:
      groups = st.number_input("組数（組）", min_value=0, value=10, step=1)
    with col4:
      customers = st.number_input("客数（人）", min_value=0, value=28, step=1)

    spend_per_customer = int(sales / customers) if customers > 0 else 0
    st.markdown(f"**本日の客単価: ¥{spend_per_customer:,}**")

    labor_cost = st.number_input(
        "人件費（円）", min_value=0, value=35600, step=1000
    )
    labor_rate = (labor_cost / sales * 100) if sales > 0 else 0.0
    st.markdown(f"人件費率: **{labor_rate:.1f}%**")

    st.markdown("---")
    st.markdown("### 仕入・経費項目（日報記載分）")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
      cost_sejima = st.number_input("瀬島", min_value=0, value=9716, step=100)
    with col_s2:
      cost_kawashima = st.number_input(
          "川島食品", min_value=0, value=0, step=100
      )

    submitted = st.form_submit_button("日報を送信・保存する")
    if submitted:
      date_str = input_date.strftime("%Y-%m-%d")
      date_dt = pd.to_datetime(date_str)

      mask = df_data["日時"].dt.strftime("%Y-%m-%d") == date_str
      if mask.any():
        df_data.loc[
            mask,
            [
                "Uレジ売上",
                "組数",
                "客数",
                "人件費",
                "瀬島",
                "川島食品",
            ],
        ] = [sales, groups, customers, labor_cost, cost_sejima, cost_kawashima]
      else:
        new_row = pd.DataFrame({
            "日時": [date_dt],
            "Uレジ売上": [sales],
            "組数": [groups],
            "客数": [customers],
            "人件費": [labor_cost],
            "瀬島": [cost_sejima],
            "川島食品": [cost_kawashima],
        })
        df_data = pd.concat([df_data, new_row], ignore_index=True)

      df_data.to_csv(DATA_FILE, index=False)
      st.session_state.df_data = df_data
      st.success(f"✨ {date_str} の日報データを正常に保存しました！")

# ==========================================
# 2. 経営ダッシュボード（仮案1）タブ
# ==========================================
with tab_dashboard:
  st.subheader("📊 経営ダッシュボード【仮案1】")
  st.info(
      "💡 見たいモジュールを選択し、定休日（売上0円）を除外した営業日ベースのきれいな推移で確認できます。"
  )

  selected_modules = st.multiselect(
      "表示モジュール選択",
      [
          "1. 月間KPIサマリー（目標達成率・客数・客単価）",
          "2. 営業日数24日ベースの曜日別目標・実績比較",
          "3. 営業日ベースの日別売上推移グラフ ＆ 詳細テーブル",
          "4. 人件費・仕入コストバランス",
      ],
      default=[
          "1. 月間KPIサマリー（目標達成率・客数・客単価）",
          "2. 営業日数24日ベースの曜日別目標・実績比較",
          "3. 営業日ベースの日別売上推移グラフ ＆ 詳細テーブル",
      ],
  )

  st.markdown("---")

  # 月の選択
  df_data["年月"] = df_data["日時"].dt.strftime("%Y年%m月")
  available_months = sorted(df_data["年月"].unique(), reverse=True)
  selected_month = st.selectbox(
      "対象月を選択", available_months, key="dash_month"
  )

  df_filtered = df_data[df_data["年月"] == selected_month].copy()
  active_df = df_filtered[df_filtered["Uレジ売上"] > 0].copy()

  total_sales = active_df["Uレジ売上"].sum()
  target_sales = 3000000
  achievement_rate = (
      (total_sales / target_sales * 100) if target_sales > 0 else 0
  )
  active_days_count = len(active_df)
  total_customers = active_df["客数"].sum()
  avg_spend = int(total_sales / total_customers) if total_customers > 0 else 0
  avg_daily = int(total_sales / active_days_count) if active_days_count > 0 else 0

  # 1. 月間KPIサマリー
  if "1. 月間KPIサマリー（目標達成率・客数・客単価）" in selected_modules:
    st.markdown(f"### 🎯 {selected_month} 経営KPIサマリー（目標: 300万円）")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "月間売上（税込）",
        f"¥{total_sales:,}",
        f"達成率 {achievement_rate:.1f}%",
    )
    col2.metric(
        "営業日数", f"{active_days_count} 日", "基準: 24日（月商300万目標）"
    )
    col3.metric("月間総客数", f"{total_customers:,} 人")
    col4.metric(
        "平均客単価",
        f"¥{avg_spend:,}",
        f"日販平均 ¥{avg_daily:,}",
    )
    st.progress(min(achievement_rate / 100.0, 1.0))
    st.markdown("---")

  # 2. 曜日別目標・実績比較
  if "2. 営業日数24日ベースの曜日別目標・実績比較" in selected_modules:
    st.markdown("### 📅 営業日数24日ベース 曜日別目標対比")

    active_df["曜日JP"] = (
        active_df["日時"]
        .dt.day_name()
        .map({
            "Monday": "月",
            "Tuesday": "火",
            "Wednesday": "水",
            "Thursday": "木",
            "Friday": "金",
            "Saturday": "土",
            "Sunday": "日",
        })
    )

    dow_summary = (
        active_df.groupby("曜日JP")
        .agg(営業回数=("Uレジ売上", "count"), 平均売上=("Uレジ売上", "mean"))
        .reindex(["月", "火", "水", "木", "金", "土", "日"])
        .fillna(0)
    )

    target_dow_dict = {
        "金": 160000,
        "土": 145000,
        "火": 140000,
        "木": 120000,
        "月": 115000,
        "水": 105000,
        "日": 85000,
    }
    dow_summary["目標日販"] = pd.Series(target_dow_dict)
    dow_summary["平均実績"] = dow_summary["平均売上"].astype(int)

    display_dow = pd.DataFrame({
        "営業回数": dow_summary["営業回数"].astype(int).astype(str) + "回",
        "目標日販": dow_summary["目標日販"].apply(lambda x: f"¥{x:,.0f}"),
        "平均実績": dow_summary["平均実績"].apply(lambda x: f"¥{x:,.0f}"),
    })

    st.dataframe(display_dow, use_container_width=True)
    st.markdown("---")

  # 3. 営業日ベースの日別売上推移グラフ ＆ 詳細テーブル
  if "3. 営業日ベースの日別売上推移グラフ ＆ 詳細テーブル" in selected_modules:
    st.markdown(
        f"### 📈 {selected_month} 日別売上推移（営業日ベース・休業日除外）"
    )
    if not active_df.empty:
      # 営業日（Uレジ売上 > 0）のみのデータフレームでグラフを作成
      chart_df = active_df.set_index(
          active_df["日時"].dt.strftime("%m/%d")
      )[["Uレジ売上"]]
      st.line_chart(chart_df)

    with st.expander("📋 日別詳細データ一覧を表示する"):
      display_df = df_filtered.copy()
      display_df["日付"] = display_df["日時"].dt.strftime("%Y-%m-%d")
      display_df["曜日"] = display_df["日時"].dt.day_name().map({
          "Monday": "月",
          "Tuesday": "火",
          "Wednesday": "水",
          "Thursday": "木",
          "Friday": "金",
          "Saturday": "土",
          "Sunday": "日",
      })
      display_df = display_df[
          [
              "日付",
              "曜日",
              "Uレジ売上",
              "組数",
              "客数",
              "人件費",
              "瀬島",
              "川島食品",
          ]
      ]
      st.dataframe(display_df, use_container_width=True)
    st.markdown("---")

  # 4. 人件費・仕入コストバランス
  if "4. 人件費・仕入コストバランス" in selected_modules:
    st.markdown(f"### 💰 {selected_month} コストバランスサマリー")
    total_labor = active_df["人件費"].sum()
    total_sejima = active_df["瀬島"].sum()
    total_kawashima = active_df["川島食品"].sum()

    col_c1, col_c2, col_c3 = st.columns(3)
    col_c1.metric(
        "人件費合計",
        f"¥{total_labor:,}",
        f"対売上 {total_labor / total_sales * 100:.1f}%"
        if total_sales > 0
        else "0%",
    )
    col_c2.metric("瀬島 仕入合計", f"¥{total_sejima:,}")
    col_c3.metric("川島食品 仕入合計", f"¥{total_kawashima:,}")

# ==========================================
# 3. 管理者画面タブ
# ==========================================
with tab_admin:
  st.subheader("⚙️ 管理者設定・データ管理")
  if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "rb") as f:
      st.download_button(
          label="📥 全データをCSVでダウンロード",
          data=f,
          file_name="toribii_all_daily_data.csv",
          mime="text/csv",
      )

  st.markdown("### 📋 登録済み全データ一覧")
  st.dataframe(df_data, use_container_width=True)
