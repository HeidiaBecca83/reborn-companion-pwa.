
import io, math
from PIL import Image, ImageOps
import streamlit as st

st.set_page_config(page_title="Reborn Companion (PWA)", page_icon="🍼", layout="centered")

ACCENT_PINK = "#F7A8B8"
ACCENT_MINT = "#B6E3C6"

st.markdown('''
<div style="border-radius:16px;padding:12px;background:linear-gradient(90deg, #F7A8B822, #B6E3C622);border:1px solid #F7A8B844;">
  <h2 style="margin:0;color:#3A3A3A;font-family: ui-rounded, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue';">
    🍼 Reborn Companion — Mobile
  </h2>
  <p style="margin:6px 0 0;opacity:.85">Install from your browser: Share ▶︎ Add to Home Screen</p>
</div>
''', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🫁 Breathing GIF", "📝 Listing Builder"])

def animate_breathing(base_img, seconds_per_cycle=4.0, intensity=0.6, frames_per_cycle=24, bob_px=3):
    base = ImageOps.contain(base_img.convert("RGB"), (640, 640))
    frames = []
    for i in range(frames_per_cycle):
        t = i / frames_per_cycle
        s = (math.sin(2*math.pi*t - math.pi/2) + 1)/2  # 0..1
        a = max(0.003, (intensity/100.0)*0.02)
        scale = 1.0 - a + (2*a)*s
        bob = int(round(bob_px * math.sin(2*math.pi*t)))
        w, h = base.size
        nw, nh = int(w*scale), int(h*scale)
        fr = base.resize((nw, nh), Image.BICUBIC)
        canvas = Image.new("RGB", (w, h), (255,255,255))
        canvas.paste(fr, ((w-nw)//2, (h-nh)//2 + bob))
        frames.append(canvas)
    return frames

with tab1:
    st.caption("Upload a photo and create a soft, looped breathing animation.")
    img_file = st.file_uploader("Photo (JPG/PNG)", type=["jpg","jpeg","png"])
    c1, c2 = st.columns(2)
    with c1:
        speed = st.slider("Breath duration (seconds)", 2.0, 8.0, 4.0, 0.5)
    with c2:
        intensity = st.slider("Breath intensity", 0.0, 2.0, 0.6, 0.05)
    if img_file:
        base = Image.open(img_file).convert("RGB")
        frames = animate_breathing(base, seconds_per_cycle=speed, intensity=intensity)
        out = io.BytesIO()
        frames[0].save(out, format="GIF", save_all=True, append_images=frames[1:]+frames[-2:0:-1], loop=0, duration=int(1000*speed/24))
        st.image(out.getvalue(), caption="Preview")
        st.download_button("Download GIF", data=out.getvalue(), file_name="reborn_breathing.gif", mime="image/gif")

with tab2:
    st.caption("Generate a marketplace title + description quickly (client‑side).")
    with st.form("listing"):
        c1, c2 = st.columns(2)
        with c1:
            sculpt_name = st.text_input("Sculpt name", placeholder="Levi")
            sculpt_artist = st.text_input("Sculpt artist", placeholder="Bonnie Brown")
            material = st.selectbox("Material", ["Vinyl","Silicone"])
            size_in = st.slider("Size (inches)", 12, 26, 19)
        with c2:
            hair = st.selectbox("Hair", ["Bald","Painted","Mono-rooted","Micro-rooted premium"])
            eyes = st.text_input("Eyes", placeholder="Sleeping")
            coa = st.selectbox("COA included?", ["No","Yes"])
            edition_size = st.text_input("Edition size", placeholder="700")
        accessories = st.text_input("Included accessories", placeholder="Pacifier, blanket")

        submitted = st.form_submit_button("Build Listing")
        if submitted:
            parts = [sculpt_name, f"by {sculpt_artist}", material, f"{size_in}\\""]
            if hair and hair.lower() not in ["none","bald"]:
                parts.append(hair)
            if coa == "Yes": parts.append("COA")
            if edition_size: parts.append(f"LE {edition_size}")
            parts.append("Reborn Doll")
            title = " ".join([p for p in parts if p])[:120]

            bullets = [
                f"• Sculpt: **{sculpt_name}**  |  Artist: **{sculpt_artist}**",
                f"• Material: **{material}**  |  Size: **{size_in} in**  |  Hair: **{hair}**  |  Eyes: **{eyes}**",
            ]
            if edition_size: bullets.append(f"• Edition: **Limited {edition_size}**")
            if coa == "Yes": bullets.append("• COA: **Included**")

            para = f"Meet **{sculpt_name or 'this sweet baby'}**—a beautifully crafted reborn with realistic painting and gentle weighting."
            care = "Ships safely swaddled. Magnets (if any) may affect pacemakers. Not a toy for young children."
            desc = "\\n".join([para,"","### Details",*bullets,"","### Care & Shipping",care])

            tags = "#Reborn #RebornDoll #RebornCommunity #OOAK"
            st.markdown("#### Title"); st.code(title)
            st.markdown("#### Description"); st.write(desc)
            st.markdown("#### Hashtags"); st.code(tags)
