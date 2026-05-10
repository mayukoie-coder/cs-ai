import streamlit as st
from app.claude_client import draft_reply

st.set_page_config(
    page_title="恋愛相談 返信ドラフト生成",
    page_icon="💌",
    layout="wide",
)

st.title("💌 恋愛相談 返信ドラフト生成ツール")
st.caption("クライアントの相談文を貼り付けて、AIが返信の下書きを生成します。")

st.divider()

col_input, col_output = st.columns(2)

with col_input:
    st.subheader("📨 クライアントからの相談文")
    consultation = st.text_area(
        label="相談内容",
        height=420,
        placeholder="例：最近、マッチングアプリで気になる方がいて、メッセージのやり取りは続いているのですが...",
        label_visibility="collapsed",
    )
    generate_btn = st.button(
        "✨ 返信ドラフトを生成",
        type="primary",
        disabled=not consultation.strip(),
        use_container_width=True,
    )

with col_output:
    st.subheader("📝 返信ドラフト")

    if "draft" not in st.session_state:
        st.session_state.draft = ""
    if "usage" not in st.session_state:
        st.session_state.usage = None

    if generate_btn and consultation.strip():
        with st.spinner("生成中..."):
            try:
                draft, usage = draft_reply(consultation)
                st.session_state.draft = draft
                st.session_state.usage = usage
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

    if st.session_state.draft:
        st.text_area(
            label="ドラフト",
            value=st.session_state.draft,
            height=420,
            label_visibility="collapsed",
        )
        st.caption("上のテキストを編集してからSlackに貼り付けてください。")

        if st.session_state.usage:
            usage = st.session_state.usage
            with st.expander("📊 トークン使用状況（コスト管理用）"):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("入力", usage["input_tokens"])
                c2.metric("出力", usage["output_tokens"])
                c3.metric("キャッシュ作成", usage["cache_creation_tokens"])
                c4.metric("キャッシュ読み取り", usage["cache_read_tokens"])
                if usage["cache_read_tokens"] > 0:
                    st.success("✅ ナレッジベースがキャッシュから読み込まれました（コスト節約）")
                else:
                    st.info("ℹ️ 初回リクエスト：ナレッジベースをキャッシュしました")
    else:
        st.markdown(
            """
            <div style='height:420px; display:flex; align-items:center;
                        justify-content:center; color:#aaa; border:1px dashed #ddd;
                        border-radius:8px; font-size:14px;'>
                ← 相談文を入力して「返信ドラフトを生成」を押してください
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()
st.caption("⚠️ 生成されたドラフトは必ず内容を確認・編集してから送信してください。")
