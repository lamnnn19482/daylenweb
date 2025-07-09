import streamlit as st
import datetime
import os

NOTE = (
    "💡 Sao rất nhiều lệnh trade: Nên chia nhỏ lệnh, tránh dồn một cục để bị quét một lần!\n"
    "💡 SL thì giữ nguyên, không cần di chuyển nếu giá chưa chạy 1500 giá."
)
WORKFLOW = {
    "step_1": {
        "question": "Giá có trên VWAP không?",
        "options": ["Trên", "Dưới"]
    },
    "step_2": {
        "question": "Big trader vào lệnh phút thứ mấy? (Nhập số phút 0-59)",
        "options": "input_minute"
    },
    "step_3": {
        "question": "Mặt cười màu gì? (Xanh/Đỏ)",
        "options": ["Xanh", "Đỏ"]
    },
    "should_trade": {
        "question": "✅ Nên vào lệnh!\n\n" + NOTE,
        "options": ["Kết quả giao dịch: Thắng", "Kết quả giao dịch: Thua"]
    },
    "end_no_trade": {
        "question": "❌ VÀO LÀ MẤT TIỀN NHA MẦY\n" * 3 + NOTE,
        "options": ["Quay lại menu"]
    },
    # Nhánh dưới VWAP
    "step_2_below": {
        "question": "Big trader vào lệnh phút thứ mấy? (Nhập số phút 0-59)",
        "options": "input_minute_below"
    },
    "step_3_below": {
        "question": "Mặt cười màu gì? (Xanh/Đỏ)",
        "options": ["Đỏ", "Xanh"]
    },
    "should_short": {
        "question": "🔴 Nên vào lệnh SHORT!\n\n" + NOTE,
        "options": ["Kết quả giao dịch: Thắng", "Kết quả giao dịch: Thua"]
    },
    "wait_short": {
        "question": "❌ Vào là MẤT TIỀN\n" * 3 + NOTE,
        "options": ["Quay lại menu"]
    },
    "reason_win": {
        "question": "Bạn thắng vì lý do gì? (Nhập lý do)",
        "options": "input_reason_win"
    },
    "reason_lose": {
        "question": "Bạn thua vì lý do gì? (Nhập lý do)",
        "options": "input_reason_lose"
    },
    "reason_win_short": {
        "question": "Bạn thắng (SHORT) vì lý do gì? (Nhập lý do)",
        "options": "input_reason_win_short"
    },
    "reason_lose_short": {
        "question": "Bạn thua (SHORT) vì lý do gì? (Nhập lý do)",
        "options": "input_reason_lose_short"
    },
    "menu": {
        "question": "Chào mừng! Chọn một chức năng bên dưới:",
        "options": ["Vào", "Lịch sử giao dịch", "Kết quả thắng", "Kết quả thua"]
    },
    "history_menu": {
        "question": "Chọn loại lịch sử muốn xem:",
        "options": ["Lịch sử hôm nay", "Lịch sử tuần này", "Tất cả lịch sử", "Quay lại menu"]
    }
}

HISTORY_FILE = "history.txt"

def save_history(trade_type, result, reason):
    now = datetime.datetime.now().strftime("%d-%m-%Y")
    r_value = "2R"
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{now} | {trade_type} | {result} | {reason} | {r_value}\n")

def show_history(filter_func=None, title="Lịch sử"):
    results = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if filter_func is None or filter_func(line):
                    results.append(line.strip())
    st.subheader(title)
    if results:
        st.text("\n".join(results))
    else:
        st.info("Không có dữ liệu.")

def show_reasons(result_type, title):
    reasons = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) >= 4 and parts[2].strip() == result_type:
                    reason = parts[3].strip()
                    if reason:
                        reasons.append(reason)
    st.subheader(title)
    if reasons:
        unique_reasons = sorted(set(reasons), key=lambda x: x.lower())
        for r in unique_reasons:
            st.markdown(f"- {'🏆' if result_type=='Thắng' else '💥'} **{r}**")
    else:
        st.info(f"Chưa có lịch sử giao dịch {result_type.lower()} nào.")

def main():
    st.set_page_config(page_title="Trading Workflow Minimalist", layout="centered")
    st.markdown("""
        <style>
        .stButton>button {font-size: 18px !important; padding: 0.7em 2em; margin: 0.5em 0; border-radius: 10px;}
        .stTextInput>div>div>input {font-size: 18px !important; border-radius: 8px; padding: 0.7em;}
        .stMarkdown, .stSubheader {font-size: 20px !important;}
        </style>
    """, unsafe_allow_html=True)
    if "state" not in st.session_state:
        st.session_state.state = "menu"
        st.session_state.big_trader_minute = None
        st.session_state.last_branch = None
    state = st.session_state.state
    step_data = WORKFLOW[state]
    st.markdown(f"**{step_data['question']}**")
    options = step_data["options"]
    # Menu chính
    if state == "menu":
        if st.button("Vào"):
            st.session_state.state = "step_1"
            st.rerun()
        if st.button("Lịch sử giao dịch"):
            st.session_state.state = "history_menu"
            st.rerun()
        if st.button("Kết quả thắng"):
            show_reasons("Thắng", "Các lý do thắng nổi bật")
        if st.button("Kết quả thua"):
            show_reasons("Thua", "Các lý do thua nổi bật")
    # Lịch sử menu
    elif state == "history_menu":
        if st.button("Lịch sử hôm nay"):
            today = datetime.datetime.now().strftime("%d-%m-%Y")
            show_history(lambda line: line.startswith(today), "Lịch sử hôm nay")
        if st.button("Lịch sử tuần này"):
            today = datetime.datetime.now()
            start_week = today - datetime.timedelta(days=today.weekday())
            def in_week(line):
                try:
                    date_str = line.split("|")[0].strip()
                    date_obj = datetime.datetime.strptime(date_str, "%d-%m-%Y")
                    return start_week.date() <= date_obj.date() <= today.date()
                except:
                    return False
            show_history(in_week, "Lịch sử tuần này")
        if st.button("Tất cả lịch sử"):
            show_history(None, "Tất cả lịch sử")
        if st.button("Quay lại menu"):
            st.session_state.state = "menu"
            st.rerun()
    # Các bước workflow
    elif state in ["step_1", "step_3", "step_3_below", "should_trade", "should_short", "end_no_trade", "wait_short"]:
        for opt in options:
            if st.button(opt):
                # Xử lý chuyển bước
                if state == "step_1":
                    if opt == "Trên":
                        st.session_state.state = "step_2"
                    else:
                        st.session_state.state = "step_2_below"
                elif state == "step_3":
                    if opt == "Xanh":
                        st.session_state.state = "should_trade"
                    else:
                        st.session_state.state = "end_no_trade"
                elif state == "step_3_below":
                    if opt == "Đỏ":
                        st.session_state.state = "should_short"
                    else:
                        st.session_state.state = "wait_short"
                elif state == "should_trade":
                    if opt == "Kết quả giao dịch: Thắng":
                        st.session_state.state = "reason_win"
                    else:
                        st.session_state.state = "reason_lose"
                elif state == "should_short":
                    if opt == "Kết quả giao dịch: Thắng":
                        st.session_state.state = "reason_win_short"
                    else:
                        st.session_state.state = "reason_lose_short"
                elif state in ["end_no_trade", "wait_short"]:
                    st.session_state.state = "menu"
                st.rerun()
    elif state == "step_2":
        minute = st.text_input("Nhập số phút (0-59)", max_chars=2, key="minute_input")
        if minute.isdigit() and 0 <= int(minute) <= 59:
            st.session_state.big_trader_minute = int(minute)
            now_minute = datetime.datetime.now().minute
            da_troi = now_minute - int(minute) if now_minute >= int(minute) else (60 - int(minute)) + now_minute
            if da_troi >= 17:
                st.warning("⛔️ Hết giờ giao dịch, không được vào lệnh!")
                if st.button("Quay lại menu"):
                    st.session_state.state = "menu"
                    st.rerun()
            else:
                con_lai = 17 - da_troi
                st.success(f"✅ Hợp lệ! Còn {con_lai} phút để giao dịch.")
                if st.button("Tiếp tục"):
                    st.session_state.state = "step_3"
                    st.rerun()
    elif state == "step_2_below":
        minute = st.text_input("Nhập số phút (0-59)", max_chars=2, key="minute_input_below")
        if minute.isdigit() and 0 <= int(minute) <= 59:
            st.session_state.big_trader_minute = int(minute)
            now_minute = datetime.datetime.now().minute
            da_troi = now_minute - int(minute) if now_minute >= int(minute) else (60 - int(minute)) + now_minute
            if da_troi >= 17:
                st.warning("⛔️ Hết giờ giao dịch, không được vào lệnh!")
                if st.button("Quay lại menu"):
                    st.session_state.state = "menu"
                    st.rerun()
            else:
                con_lai = 17 - da_troi
                st.success(f"✅ Hợp lệ! Còn {con_lai} phút để giao dịch.")
                if st.button("Tiếp tục"):
                    st.session_state.state = "step_3_below"
                    st.rerun()
    elif state in ["reason_win", "reason_lose", "reason_win_short", "reason_lose_short"]:
        result = "Thắng" if "win" in state else "Thua"
        trade_type = "Long" if "short" not in state else "Short"
        reason = st.text_input("Nhập lý do:", key="reason_input")
        if reason:
            if st.button("Lưu lịch sử lệnh"):
                save_history(trade_type, result, reason)
                st.success("Đã lưu lịch sử lệnh!")
                st.session_state.state = "menu"
                st.rerun()

if __name__ == "__main__":
    main()



