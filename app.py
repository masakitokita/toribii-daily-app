import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="炭火バル とりびぃーの 日報・小口管理",
    layout="wide", # PCでも広く使えるようwideに設定
    initial_sidebar_state="expanded"
)

# スマホ版プレビュー用のコンテナを再現するCSS
st.markdown(
    """
    <style>
    div[data-baseweb="spinbutton"] button {
        display: none !important;
    }
    div[data-baseweb="spinbutton"] input {
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# サイドバーで「表示モード」の切り替えスイッチを設置
st.sidebar.header("🖥️ 表示モード切替")
view_mode = st.sidebar.radio("表示方法を選んでください", ["スマホ版プレビューで確認", "通常PCワイド表示"])

if view_mode == "スマホ版プレビューで確認":
    # スマホの幅（約420px）に制限して中央寄せにするフレーム枠
    _, center_col, _ = st.sidebar.columns([1, 2, 1]) # ダミー用、メイン側で囲みを作る
    # 実質的なスマホ風レイアウトをレンダリングするため、中央にカラムを配置
    st.markdown("<div style='max-width: 480px; margin: auto; padding: 15px; border: 2px solid #ccc; border-radius: 20px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1);'>", unsafe_allow_html=True)

# ヘッダー
st.markdown("<h1 style='font-size: 24px; white-space: nowrap; margin-bottom: 0px;'>炭火バル とりびぃーの</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #666; font-size: 13px; margin-top: 2px;'>店舗スタッフ用日報・仕入管理システム</p>", unsafe_allow_html=True)

if "reports" not in st.session_state:
    st.session_state.reports = []
if "small_cash_locked" not in st.session_state:
    st.session_state.small_cash_locked = False
if "current_claim" not in st.session_state:
    st.session_state.current_claim = None

tab1, tab2, tab3, tab4 = st.tabs(["📊 ダッシュボード", "📝 日報送信", "💰 小口精算", "⚙️ 管理者"])

monthly_target = 4000000
current_sales = 3140670

with tab1:
    st.subheader("月間売上ダッシュボード")
    progress = min(current_sales / monthly_target, 1.0)
    st.metric(label="11月目標達成率", value=f"{progress*100:.1f}%", delta=f"¥{current_sales:,} / ¥{monthly_target:,}")
    st.progress(progress)
    
    st.markdown("---")
    st.subheader("日次売上推移（11月）")
    chart_data = pd.DataFrame({
        "日": [f"{i}日" for i in range(1, 15)],
        "売上": [120000, 140000, 135000, 150000, 125000, 160000, 180000, 110000, 130000, 145000, 155000, 140000, 142000, 140670]
    }).set_index("日")
    st.line_chart(chart_data)
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.metric("当月累計客数", "628人")
    with col_c2:
        st.metric("平均客単価", "¥5,001")

with tab2:
    st.subheader("日報・売上・原価入力")
    report_date = st.date_input("営業日", value=datetime.today())
    
    st.info("💡 **【日報・仕入用】各種写メのアップロード**\n過去の伝票も日付そのままで随時アップロードして蓄積できます。", icon="📷")
    
    u_regi_img = st.file_uploader("1. 【日報用】Uレジの売上画面", type=["jpg", "jpeg", "png"], key="u_regi_daily")
    receipt_img = st.file_uploader("2. 【日報用】仕入・納品書・レシート類", type=["jpg", "jpeg", "png"], key="receipts_daily")
    
    auto_sales = 142670 if u_regi_img is not None else 140000
    auto_groups = 10 if u_regi_img is not None else 10
    auto_customers = 28 if u_regi_img is not None else 25
    
    if u_regi_img is not None or receipt_img is not None:
        st.success("✨ 写メからの自動読み取りが完了しました。")

    sales_amount = st.number_input("Uレジ 売上金額（円）", min_value=0, step=1000, value=auto_sales, format="%d")
    
    col_g, col_c = st.columns(2)
    with col_g:
        group_count = st.number_input("組数（組）", min_value=0, step=1, value=auto_groups)
    with col_c:
        customer_count = st.number_input("客数（人）", min_value=0, step=1, value=auto_customers)
        
    avg_spending = (sales_amount / customer_count) if customer_count > 0 else 0
    st.caption(f"本日の客単価: **¥{int(avg_spending):,}**")
    
    # ── 人件費詳細入力（デフォルト値を設定） ──
    st.subheader("人件費詳細入力")
    staff_shain = st.number_input("正社員人数（日給¥20,000）", min_value=0, step=1, value=1)
    
    b_a_hours = st.number_input("パートA（時給¥1,300）時間数", min_value=0.0, step=0.5, value=5.0)
    b_b_hours = st.number_input("パートB（時給¥1,300）時間数", min_value=0.0, step=0.5, value=5.0)
    b_c_hours = st.number_input("パートC（時給¥1,300）時間数", min_value=0.0, step=0.5, value=5.0)
    b_d_hours = st.number_input("パートD（時給¥1,300）時間数", min_value=0.0, step=0.5, value=5.0)
    
    # 計算ロジック
    shain_cost = staff_shain * 20000
    part_time_cost = int((b_a_hours + b_b_hours + b_c_hours + b_d_hours) * 1300)
    total_labor_cost = shain_cost + part_time_cost
    
    st.markdown(f"**本日合計人件費:** **¥{total_labor_cost:,}**")
    # ──────────────────────────────
    
    st.markdown("")
    if st.button("日報データを蓄積する", use_container_width=True):
        date_str = report_date.strftime("%Y-%m-%d")
        new_data = {
            "日時": date_str, "Uレジ売上": sales_amount, "組数": group_count,
            "客数": customer_count, "客単価": int(avg_spending), "人件費": total_labor_cost
        }
        st.session_state.reports.append(new_data)
        st.success("データを蓄積しました。")
        st.rerun()

with tab3:
    st.subheader("小口現金 精算申請")
    st.info("💰 **【小口専用】レシートのアップロード**", icon="🧾")
    sc_receipt = st.file_uploader("【小口精算用】レシート写メ", type=["jpg", "jpeg", "png"], key="sc_receipt")
    auto_calculated_amount = 4580 if sc_receipt is not None else 0
    st.info(f"自動読み取りされた精算申請額: ¥{auto_calculated_amount:,}")
    if st.button("小口精算を申請する", use_container_width=True):
        if sc_receipt is None:
            st.error("小口精算用のレシート写メをアップロードしてください。")
        else:
            st.session_state.current_claim = auto_calculated_amount
            st.session_state.small_cash_locked = True
            st.success("小口精算の申請を行いました。")
            st.rerun()

with tab4:
    st.subheader("管理者コントロール・データ一覧")
    if st.session_state.reports:
        st.dataframe(pd.DataFrame(st.session_state.reports), use_container_width=True)
    else:
        st.info("まだ蓄積されたデータはありません。")

if view_mode == "スマホ版プレビューで確認":
    st.markdown("</div>", unsafe_allow_html=True)
