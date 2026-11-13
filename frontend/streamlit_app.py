import os
import httpx
import streamlit as st

API_BASE_URL=os.getenv("IMAGE_LINGO_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="ImageLingo", layout="wide")
st.title("ImageLingo")

st.write("""
        ImageLingo is an app that translates any visible and readable texts in the 
        image uploaded from any language to the one of the targeted languages, which 
        could be English, French, or Mandarin. Additionally, the app can automatically 
        improve lightings, remove shadows and make blurred words more visible and 
        recognizable to the user. While doing so, the app will keep the image original.
        It will preserve the style, color, logo, names of the original image.It's an 
        app can help you understand posters, forms and travelling documents in different 
        languages instantaneously. The app only accepts JPEG, PNG, or WebP image type. The
        processing time is between 30s and 60s approximately. Click the download button at
        the very bottom to download the successfully translated image.
""")

with st.form("translate_form"):
    upload=st.file_uploader(
        "Upload a photo",
        type=["jpg", "jpeg", "png", "webp"],
    )
    target_language=st.selectbox("Translate to", ["English", "French", "Mandarin"])
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
            st.error("Image Translation took more than 3 minutes. Try again with a different photo.")
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

    left.caption("Original")
    left.image(original)

    right.caption(f"Translated to {language}")
    right.image(translated)
    right.download_button(
        "Download PNG",
        data=translated,
        file_name=f"translated_{language.lower()}.png",
        mime="image/png",
        type="primary"
    )

