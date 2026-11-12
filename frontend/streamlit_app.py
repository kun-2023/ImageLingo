import os
import httpx
import streamlit as st

API_BASE_URL=os.getenv("IMAGE_LINGO_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="ImageLingo", layout="wide")
st.title("ImageLingo")

with st.form("translate_form"):
    upload=st.file_uploader(
        "Upload a photo",
        type=["jpg", "jpeg", "png", "webp"],
    )
    target_language=st.selectbox("Translate to", ["English", "French"])
    submitted=st.form_submit_button("Translate image")
if submitted:
    st.session_state.pop("translation_result", None)
    if upload is None:
        st.warning("Choosing a photo first.")
    else:
        original=upload.getvalue()
        try:
            with st.spinner("Translating Image..."):
                response=httpx.post(
                    f"{API_BASE_URL}/translate",
                    files={"image": (upload.name, original, upload.type)},
                    data={"target_language": target_language},
                    timeout=180.0
                )
                response.raise_for_status()
        except httpx.TimeoutException:
            st.error("Image Translation took more than 3 minutes. Try again with different photo.")
        except httpx.HTTPStatusError as exc:
            st.error(f"Translation failed (HTTP {exc.response.status_code}.)")
        except httpx.RequestError:
            st.error("Could not reach FastAPI. Check that Uvicorn is running.")
        else:
            st.session_state["translation_result"]=(
                original,
                response.content,
                target_language,
            )

if "translation_result" in st.session_state:
    original, translated, language=st.session_state["translation_result"]
    left, right=st.columns(2)

    left.image(original, caption="Original")
    right.image(translated, caption=f"Translated to {language}")
    right.download_button(
        "Download PNG",
        data=translated,
        file_name=f"translated_{language.lower()}.png",
        mime="image/png"
    )

