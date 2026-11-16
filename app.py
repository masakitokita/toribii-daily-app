with tab1:
    st.subheader("📊 炭火バル とりびぃーの 経営ダッシュボード")
    
    # サイドバーまたは画面上部で「見たい項目」を選択
    selected_sections = st.sidebar.multiselect(
        "👁️ 表示する項目を選択してください",
        ["月間KPIサマリー", "曜日別パフォーマンス", "日別売上グラフ・詳細", "コスト・人件費バランス", "前年同月比"],
        default=["月間KPIサマリー", "曜日別パフォーマンス", "日別売上グラフ・詳細"]
    )
    
    # 選択されたセクションに応じて動的に表示を切り替え
    if "月間KPIサマリー" in selected_sections:
        st.markdown("### 🎯 月間目標達成状況（目標: ¥3,000,000 / 24営業日）")
        # メトリック＆プログレスバーの描画処理...
        
    if "曜日別パフォーマンス" in selected_sections:
        st.markdown("### 📅 曜日別目標対比")
        # 金土や平日ごとの実績グラフ...
        
    if "日別売上グラフ・詳細" in selected_sections:
        st.markdown("### 📈 日別売上推移")
        # 折れ線グラフとデータフレーム...
        
    if "コスト・人件費バランス" in selected_sections:
        st.markdown("### 💰 コストバランス")
        # 人件費率の計算など...
