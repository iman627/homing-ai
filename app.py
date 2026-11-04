import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
from duckduckgo_search import DDGS
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="HOMING AI",
    page_icon="🚀",
    layout="wide"
)

# اتصال به هوش مصنوعی
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    api_key = st.secrets["OPENAI_API_KEY"]

client = OpenAI(
    api_key=api_key,
    base_url="https://1xai.ir/v1"
)

# ده منبع جست‌وجو
WEBSITES = [
    "wikipedia.org",
    "britannica.com",
    "nasa.gov",
    "khanacademy.org",
    "coursera.org",
    "stackoverflow.com",
    "w3schools.com",
    "nationalgeographic.com",
    "who.int",
    "unesco.org"
]

# طراحی فضایی
st.markdown("""
/* خوانایی نوشته‌ها */
.stApp,
.stApp p,
.stApp label,
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stChatMessage"],
.stApp .stCaption {
    color: #ffffff !important;
}

/* نوشته‌های داخل کادرهای ورودی */
.stApp input,
.stApp textarea {
    color: #ffffff !important;
    background-color: #142447 !important;
}
<style>
.stApp {
    background:
    radial-gradient(circle at top, #172c64, #080b20 65%);
    color: white;
}
h1 {
    color: #55d9ff;
    text-align: center;
    font-size: 55px;
    text-shadow: 0 0 20px #00cfff;
}
.subtitle {
    text-align: center;
    color: #a5caff;
    font-size: 17px;
}
.stChatMessage {
    background: rgba(30, 55, 110, 0.35);
    border: 1px solid #315eaa;
    border-radius: 15px;
}
.stButton button {
    background: linear-gradient(90deg,#087cff,#8b35ff);
    color: white;
    border-radius: 12px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🚀 HOMING AI</h1>", unsafe_allow_html=True)

st.markdown(
    '<p class="subtitle">YOUR INTELLIGENT SPACE COMPANION</p>',
    unsafe_allow_html=True
)

st.caption("سیستم هوشمند هومینگ فعال است 🌌")

# تنظیمات کناری
with st.sidebar:
    st.title("⚙️ تنظیمات هومینگ")

    search_enabled = st.toggle(
        "فعال کردن جست‌وجوی ۱۰ سایت",
        value=True
    )

    teacher_mode = st.toggle(
        "حالت معلم هوشمند",
        value=True
    )

    if st.button("🗑️ گفت‌وگوی جدید"):
        st.session_state.messages = []
        st.rerun()

# حافظه مکالمه
if "messages" not in st.session_state:
    st.session_state.messages = []

# جست‌وجوی اینترنت
def search_web(question):
    results = []

    try:
        with DDGS() as ddgs:
            for site in WEBSITES:
                query = f"site:{site} {question}"

                found = ddgs.text(
                    query,
                    max_results=2
                )

                for item in found:
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("href", ""),
                        "body": item.get("body", "")
                    })

    except Exception as error:
        st.warning(f"خطای جست‌وجو: {error}")

    return results


# ساخت پاسخ هوشمند
def ask_homing(question):

    sources = []

    if search_enabled:
        sources = search_web(question)

    web_context = ""

    for source in sources:
        web_context += (
            f"\nعنوان: {source['title']}"
            f"\nلینک: {source['url']}"
            f"\nمتن: {source['body']}\n"
        )

    mode = (
        "تو یک معلم حرفه‌ای هستی و درس‌ها را "
        "مرحله‌به‌مرحله و ساده آموزش می‌دهی."
        if teacher_mode else
        "تو یک دستیار هوشمند و خلاق هستی."
    )

    instructions = f"""
    نام تو HOMING است.

    {mode}

    قوانین تو:
    1. با زبان کاربر صحبت کن.
    2. زبان‌های مختلف را تا حد توان پشتیبانی کن.
    3. پاسخ‌ها دقیق، مفید و قابل فهم باشند.
    4. در درس‌ها مثال بزن.
    5. اگر جواب را نمی‌دانی، صادق باش.
    6. اطلاعات اینترنتی را از منابع داده‌شده تفکیک کن.
    7. هیچ منبعی را بدون بررسی معتبر اعلام نکن.
    8. ظاهر پاسخ‌ها مرتب و خوانا باشد.

    اطلاعات جست‌وجوی وب:
    {web_context}
    """

    history = st.session_state.messages[-12:]

    response = client.responses.create(
       model="gpt-4o-mini",
        instructions=instructions,
        input=history + [
            {"role": "user", "content": question}
        ]
    )

    return response.output_text, sources


# نمایش تاریخچه
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ورودی کاربر
question = st.chat_input(
    "با هومینگ صحبت کن... 🌌"
)

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("هومینگ در حال فکر کردن است... 🚀"):

            try:
                answer, sources = ask_homing(question)

                st.markdown(answer)

                # نمایش منابع جست‌وجو
                if sources:
                    with st.expander("🔎 منابع جست‌وجو"):
                        for source in sources:
                            st.markdown(
                                f"- [{source['title']}]"
                                f"({source['url']})"
                            )

                # خواندن پاسخ با صدای مرورگر
                safe_answer = answer.replace(
                    "\\", "\\\\"
                ).replace("`", "\\`").replace(
                    "$", "\\$"
                )

                components.html(
                    f"""
                    <button onclick="speakAnswer()">
                    🔊 خواندن پاسخ هومینگ
                    </button>

                    <script>
                    function speakAnswer() {{
                        const text = `{safe_answer}`;
                        const speech = new SpeechSynthesisUtterance(text);
                        speech.lang = "fa-IR";
                        speech.rate = 0.95;
                        speechSynthesis.cancel();
                        speechSynthesis.speak(speech);
                    }}
                    </script>
                    """,
                    height=55
                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:
                st.error(f"خطا در سیستم: {error}")