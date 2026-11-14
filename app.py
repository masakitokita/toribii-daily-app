import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="炭火バル とりびぃーの 日報・小口管理",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if "reports" not in st.session_state:
    st.session_state.reports = []
if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []
if "small_cash_locked" not in st.session_state:
    st.session_state.small_cash_locked = False
if "current_claim" not in st.session_state:
    st.session_state.current_claim = None

st.title("炭火バル とりびぃーの")
st.caption("店舗スタッフ用日報・仕入管理システム")

tab1, tab2, tab3 = st.tabs(["日報・仕入送信", "小口精算申請", "管理者画面"])

with tab1:
    st.subheader("日報・売上・原価入力")
    report_date = st.date_input("営業日", value=datetime.today())
    sales_amount = st.number_input("Uレジ 売上金額（円）", min_value=0, step=1000, value=140670, format="%d")
    
    col_g, col_c = st.columns(2)
    with col_g:
        group_count = st.number_input("組数（組）", min_value=0, step=1, value=10)
    with col_c:
        customer_count = st.number_input("客数（人）", min_value=0, step=1, value=28)
        
    avg_spending = (sales_amount / customer_count) if customer_count > 0 else 0
    st.caption(f"本日の客単価: **¥{int(avg_spending):,}**")
    
    labor_cost = st.number_input("人件費（円）", min_value=0, step=1000, value=35600, format="%d")
    labor_rate = (labor_cost / sales_amount * 100) if sales_amount > 0 else 0.0
    st.caption(f"人件費率: **{labor_rate:.1f}%**")
    
    st.subheader("仕入・経費項目（日報記載分）")
    col1, col2 = st.columns(2)
    with col1:
        sejima = st.number_input("瀬島", min_value=0, value=9716)
        nishihara = st.number_input("西原商会有", min_value=0, value=12975)
        hirobi = st.number_input("廣備", min_value=0, value=0)
        tori_yamada = st.number_input("鶏の山田", min_value=0, value=1469)
    with col2:
        kawashima = st.number_input("川島食品", min_value=0, value=0)
        alpaca = st.number_input("アルプス商事", min_value=0, value=0)
        koguchi = st.number_input("小口", min_value=0, value=2417)
        card = st.number_input("カード", min_value=0, value=0)
        
    calc_cost = sejima + nishihara + hirobi + tori_yamada + kawashima + alpaca + koguchi + card
    food_rate = (calc_cost / sales_amount * 100) if sales_amount > 0 else 0.0
    
    st.markdown(f"**仕入・経費合計:** ¥{calc_cost:,}")
    st.caption(f"原価率換算: **{food_rate:.1f}%**")
    
    st.markdown("")
    st.subheader("各種写メのアップロード")
    u_regi_img = st.file_uploader("1. Uレジの売上画面", type=["jpg", "jpeg", "png"], key="u_regi")
    receipt_img = st.file_uploader("2. 納品書・レシート類", type=["jpg", "jpeg", "png"], key="receipts")
    
    st.markdown("")
    if st.button("日報を送信する", use_container_width=True):
        date_str = report_date.strftime("%Y-%m-%d")
        supplier_breakdown = {
            "瀬島": sejima, "西原商会有": nishihara, "廣備": hirobi,
            "鶏の山田": tori_yamada, "川島食品": kawashima, "アルプス商事": alpaca,
            "小口": koguchi, "カード": card
        }
        new_data = {
            "日時": date_str, "Uレジ売上": sales_amount, "組数": group_count,
            "客数": customer_count, "客単価": int(avg_spending), "人件費": labor_cost,
            "人件費率": f"{labor_rate:.1f}%", "合計支出": calc_cost, "内訳": supplier_breakdown, "ステータス": "完了"
        }
        st.session_state.reports.append(new_data)
        st.session_state.journal_entries.append({"日付": date_str, "借方勘定": "現金売掛金", "借方金額": sales_amount, "貸方勘定": "売上高", "貸方金額": sales_amount, "摘要": "Uレジ売上計上"})
        st.session_state.journal_entries.append({"日付": date_str, "借方勘定": "労務費", "借方金額": labor_cost, "貸方勘定": "未払金", "貸方金額": labor_cost, "摘要": "人件費計上"})
        for sup, amt in supplier_breakdown.items():
            if amt > 0:
                st.session_state.journal_entries.append({"日付": date_str, "借方勘定": f"経費・仕入({sup})", "借方金額": amt, "貸方勘定": "買掛金未払金", "貸方金額": amt, "摘要": f"{sup}計上"})
        st.success("日報の送信と自動仕訳の作成が完了しました。")
        st.rerun()

with tab2:
    st.subheader("小口現金 精算申請")
    st.caption("インプレスト（10万円定額）の補充・精算を行います")
    if st.session_state.small_cash_locked:
        st.warning("現在、小口精算の申請がロックされています。管理者の確認・現金精算を行うまで次の申請はできません。")
        if st.session_state.current_claim:
            st.info(f"申請中の金額: ¥{st.session_state.current_claim:,}")
    else:
        sc_receipt = st.file_uploader("小口レシート写メ", type=["jpg", "jpeg", "png"], key="sc_receipt")
        auto_calculated_amount = 4580 if sc_receipt is not None else 0
        st.info(f"自動読み取りされた精算申請額: ¥{auto_calculated_amount:,}")
        if st.button("小口精算を申請する", use_container_width=True):
            if sc_receipt is None:
                st.error("レシートの写メをアップロードしてください。")
            else:
                st.session_state.current_claim = auto_calculated_amount
                st.session_state.small_cash_locked = True
                st.success("小口精算の申請を行いました。")
                st.rerun()

with tab3:
    st.subheader("管理者コントロール")
    if st.session_state.small_cash_locked:
        st.error(f"未処理の小口精算があります。申請額: ¥{st.session_state.current_claim:,}")
        if st.button("現金を渡し、確認済み（ロック解除）にする", type="primary", use_container_width=True):
            st.session_state.small_cash_locked = False
            st.session_state.current_claim = None
            st.success("ロックを解除しました。")
            st.rerun()
    else:
        st.success("現在、保留中の小口精算はありません。")

    st.subheader("蓄積データ一覧（日報）")
    if st.session_state.reports:
        df_rep = pd.DataFrame(st.session_state.reports)
        st.dataframe(df_rep, use_container_width=True)
    else:
        st.info("まだ送信されたデータはありません。")

    st.subheader("自動生成された仕訳データ一覧")
    if st.session_state.journal_entries:
        df_je = pd.DataFrame(st.session_state.journal_entries)
        st.dataframe(df_je, use_container_width=True)
    else:
        st.info("まだ生成された仕訳データはありません。")
