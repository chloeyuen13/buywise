import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="BuyWise", layout="wide")

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 4px;
}
.sub-title {
    font-size: 18px;
    color: #666;
    margin-bottom: 6px;
}
.sub-desc {
    font-size: 15px;
    color: #777;
    margin-bottom: 24px;
}
.card {
    background: #ffffff;
    border: 1px solid #ececec;
    border-radius: 18px;
    padding: 18px 18px 14px 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.04);
    min-height: 260px;
}
.card-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 8px;
}
.card-price {
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 12px;
}
.tag {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    background: #f3f4f6;
    margin: 4px 6px 0 0;
    font-size: 13px;
}
.highlight-box {
    background: #f8fbf8;
    border: 1px solid #d8ead8;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 8px;
}
.section-note {
    color: #777;
    font-size: 14px;
    margin-top: -8px;
    margin-bottom: 12px;
}
.metric-box {
    background: #fafafa;
    border: 1px solid #ededed;
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
.small-label {
    font-size: 13px;
    color: #777;
}
.big-value {
    font-size: 24px;
    font-weight: 800;
}
.divider-space {
    margin-top: 8px;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">BuyWise</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Find the right product for you — faster</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-desc">Compare products, understand trade-offs, and see whether now is a good time to buy.</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("headphones.csv")

# -----------------------------
# Helper Functions
# -----------------------------
def normalize_high(series):
    return (series - series.min()) / (series.max() - series.min() + 1e-9)

def normalize_low(series):
    return 1 - (series - series.min()) / (series.max() - series.min() + 1e-9)

def get_price_history(row):
    return [row["price_t1"], row["price_t2"], row["price_t3"], row["price_t4"], row["price"]]

def get_price_position_tag(current_price, history_prices):
    hist_min = min(history_prices)
    hist_max = max(history_prices)
    ratio = (current_price - hist_min) / (hist_max - hist_min + 1e-9)

    if ratio <= 0.2:
        return "Near recent low", "A good time to buy"
    elif ratio <= 0.6:
        return "Mid-range", "Worth buying if you need it now"
    else:
        return "Near recent high", "You may want to wait for a better deal"

def get_product_tags(row, scored):
    tags = []

    if row["price"] == scored["price"].min():
        tags.append("Best value")
    if row["battery"] == scored["battery"].max():
        tags.append("Long battery life")
    if row["anc"] == scored["anc"].max():
        tags.append("Strong noise cancellation")
    if row["rating"] == scored["rating"].max():
        tags.append("Highly rated")
    if row["after_sale"] == scored["after_sale"].max():
        tags.append("Reliable support")
    if row["price"] == scored["price"].max():
        tags.append("Premium pricing")
    if row["weight"] == scored["weight"].max():
        tags.append("Heavier design")
    if row["negative_review"] >= 10:
        tags.append("Mixed reviews")

    return tags

def build_strengths(row, scored):
    strengths = []
    history_prices = get_price_history(row)
    price_position, _ = get_price_position_tag(row["price"], history_prices)

    if row["price"] == scored["price"].min():
        strengths.append("more budget-friendly")
    if row["battery"] == scored["battery"].max():
        strengths.append("excellent battery life")
    if row["anc"] == scored["anc"].max():
        strengths.append("strong noise cancellation")
    if row["rating"] == scored["rating"].max():
        strengths.append("strong user reviews")
    if row["after_sale"] == scored["after_sale"].max():
        strengths.append("reliable after-sale support")
    if price_position == "Near recent low":
        strengths.append("a relatively attractive buying window")

    return strengths

def build_cautions(row, scored):
    cautions = []
    history_prices = get_price_history(row)
    price_position, _ = get_price_position_tag(row["price"], history_prices)

    if row["price"] == scored["price"].max():
        cautions.append("the highest price among the selected products")
    if row["weight"] == scored["weight"].max():
        cautions.append("a heavier design")
    if row["negative_review"] >= 10:
        cautions.append("more negative feedback than peers")
    if price_position == "Near recent high":
        cautions.append("the current price is less attractive")

    return cautions

# -----------------------------
# Product Selection
# -----------------------------
products = st.multiselect(
    "Select products to compare",
    df["product"].tolist(),
    default=df["product"].tolist()[:3]
)

if products:
    selected = df[df["product"].isin(products)].copy()

    # ---------------------------------
    # 1. Preference Setup
    # ---------------------------------
    st.subheader("1. Tell us what matters most to you")
    st.markdown(
        '<div class="section-note">Adjust the factors below so we can personalize the recommendation.</div>',
        unsafe_allow_html=True
    )

    preset = st.selectbox(
        "Quick preference preset",
        ["Custom", "Budget-conscious", "Audio enthusiast", "Frequent traveler", "Balanced user"]
    )

    if preset == "Budget-conscious":
        default_weights = {"price": 5, "rating": 3, "battery": 2, "anc": 2, "after_sale": 3}
    elif preset == "Audio enthusiast":
        default_weights = {"price": 2, "rating": 4, "battery": 3, "anc": 5, "after_sale": 3}
    elif preset == "Frequent traveler":
        default_weights = {"price": 2, "rating": 4, "battery": 5, "anc": 5, "after_sale": 3}
    elif preset == "Balanced user":
        default_weights = {"price": 4, "rating": 4, "battery": 4, "anc": 4, "after_sale": 4}
    else:
        default_weights = {"price": 4, "rating": 4, "battery": 3, "anc": 4, "after_sale": 3}

    col1, col2 = st.columns(2)

    with col1:
        price_weight = st.slider("How important is price?", 1, 5, default_weights["price"])
        rating_weight = st.slider("How important are user reviews?", 1, 5, default_weights["rating"])
        battery_weight = st.slider("How important is battery life?", 1, 5, default_weights["battery"])

    with col2:
        anc_weight = st.slider("How important is noise cancellation?", 1, 5, default_weights["anc"])
        after_sale_weight = st.slider("How important is after-sale support?", 1, 5, default_weights["after_sale"])

    # ---------------------------------
    # Scoring
    # ---------------------------------
    scored = selected.copy()
    scored["price_score"] = normalize_low(scored["price"])
    scored["rating_score"] = normalize_high(scored["rating"])
    scored["battery_score"] = normalize_high(scored["battery"])
    scored["anc_score"] = normalize_high(scored["anc"])
    scored["after_sale_score"] = normalize_high(scored["after_sale"])

    total_weight = price_weight + rating_weight + battery_weight + anc_weight + after_sale_weight

    scored["overall_score"] = (
        scored["price_score"] * price_weight +
        scored["rating_score"] * rating_weight +
        scored["battery_score"] * battery_weight +
        scored["anc_score"] * anc_weight +
        scored["after_sale_score"] * after_sale_weight
    ) / total_weight

    scored["overall_score_100"] = (scored["overall_score"] * 100).round(1)
    scored["product_tags"] = scored.apply(lambda row: ", ".join(get_product_tags(row, scored)), axis=1)

    ranked = scored.sort_values("overall_score", ascending=False).reset_index(drop=True)
    best_row = ranked.iloc[0]
    best_product = best_row["product"]

    best_strengths = build_strengths(best_row, scored)
    best_cautions = build_cautions(best_row, scored)
    best_history = get_price_history(best_row)
    best_position, best_action = get_price_position_tag(best_row["price"], best_history)

    # ---------------------------------
    # 2. Recommended for you
    # ---------------------------------
    st.subheader("2. Recommended for you")

    st.markdown(f"""
<div class="highlight-box">
    <h3 style="margin-top:0;">{best_product}</h3>
    <p style="font-size:18px; font-weight:700; margin-bottom:10px;">Match score: {best_row['overall_score_100']}/100</p>
    <p><strong>This product offers the best overall balance based on your current priorities.</strong></p>
</div>
""", unsafe_allow_html=True)

    rec_col1, rec_col2, rec_col3 = st.columns(3)

    with rec_col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="small-label">Current price</div>
            <div class="big-value">${best_row['price']}</div>
        </div>
        """, unsafe_allow_html=True)

    with rec_col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="small-label">Price position</div>
            <div class="big-value" style="font-size:20px;">{best_position}</div>
        </div>
        """, unsafe_allow_html=True)

    with rec_col3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="small-label">Buying suggestion</div>
            <div class="big-value" style="font-size:20px;">{best_action}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("**Why it fits your needs**")
    if best_strengths:
        for item in best_strengths[:3]:
            st.write(f"- {item}")
    else:
        st.write("- Balanced performance across the most important factors")

    # ---------------------------------
    # 3. Is this a good time to buy?
    # ---------------------------------
    st.subheader("3. Is this a good time to buy?")
    st.markdown(
        '<div class="section-note">Check the recent price trend for the recommended product first. You can inspect other products below.</div>',
        unsafe_allow_html=True
    )

    buy_col1, buy_col2 = st.columns([1.6, 1])

    with buy_col1:
        fig_price_best = go.Figure()
        fig_price_best.add_trace(go.Scatter(
            x=["T1", "T2", "T3", "T4", "Now"],
            y=best_history,
            mode="lines+markers",
            name=best_product
        ))
        fig_price_best.update_layout(
            title=best_product,
            xaxis_title="Time",
            yaxis_title="Price",
            height=320,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_price_best, use_container_width=True)

    with buy_col2:
        st.write(f"**Price position:** {best_position}")
        st.write(f"**Buying suggestion:** {best_action}")

        st.write("**Things to keep in mind**")
        if best_cautions:
            for item in best_cautions:
                st.write(f"- {item}")
        else:
            st.write("- No major drawback in this comparison")

        st.write("**Key highlights**")
        for tag in get_product_tags(best_row, scored):
            st.markdown(f'<span class="tag">{tag}</span>', unsafe_allow_html=True)

    # ---------------------------------
    # 4. Compare at a glance
    # ---------------------------------
    st.subheader("4. Compare at a glance")
    st.markdown(
        '<div class="section-note">A compact overview of the compared products.</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(len(selected))

    for i, (_, row) in enumerate(selected.iterrows()):
        history_prices = get_price_history(row)
        price_position, buy_timing = get_price_position_tag(row["price"], history_prices)
        all_tags = get_product_tags(row, scored)

        with cols[i]:
            tag_html = ""
            for t in all_tags[:2]:
                tag_html += f'<span class="tag">{t}</span>'

            st.markdown(f"""
            <div class="card">
                <div class="card-title">{row['product']}</div>
                <div class="card-price">${row['price']}</div>
                <p><strong>Rating:</strong> {row['rating']}</p>
                <p><strong>Battery:</strong> {row['battery']}h</p>
                <p><strong>ANC:</strong> {row['anc']}/10</p>
                <p><strong>Price:</strong> {price_position}</p>
                <div>{tag_html}</div>
            </div>
            """, unsafe_allow_html=True)

    # ---------------------------------
    # 5. Feature comparison
    # ---------------------------------
    st.subheader("5. Feature comparison")
    st.markdown(
        '<div class="section-note">A quick visual comparison across the core product features.</div>',
        unsafe_allow_html=True
    )

    radar_scaled = selected.copy()
    radar_scaled["battery_scaled"] = radar_scaled["battery"] / radar_scaled["battery"].max() * 5

    fig_radar = go.Figure()

    for _, row in radar_scaled.iterrows():
        fig_radar.add_trace(go.Scatterpolar(
            r=[
                row["rating"],
                row["battery_scaled"],
                row["anc"],
                row["after_sale"]
            ],
            theta=["User rating", "Battery life", "Noise cancellation", "After-sale support"],
            fill="toself",
            name=row["product"]
        ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=True,
        height=500
    )

    st.plotly_chart(fig_radar, use_container_width=True)
    st.caption("Battery life is scaled for easier visual comparison.")

    # ---------------------------------
    # 6. Consider other options
    # ---------------------------------
    st.subheader("6. Consider other options")
    st.markdown(
        '<div class="section-note">Explore alternatives if you want a different balance of price, performance, or timing.</div>',
        unsafe_allow_html=True
    )

    other_index = 1 if len(ranked) > 1 else 0
    other_product = st.selectbox(
        "Choose another product to inspect",
        ranked["product"].tolist(),
        index=other_index
    )

    other_row = scored[scored["product"] == other_product].iloc[0]
    other_strengths = build_strengths(other_row, scored)
    other_cautions = build_cautions(other_row, scored)
    other_history = get_price_history(other_row)
    other_position, other_action = get_price_position_tag(other_row["price"], other_history)

    other_left, other_right = st.columns([1.4, 1])

    with other_left:
        st.markdown(f"""
<div class="highlight-box">
    <h3 style="margin-top:0;">{other_product}</h3>
    <p><strong>Match score:</strong> {other_row['overall_score_100']}/100</p>
    <p><strong>Price position:</strong> {other_position}</p>
    <p><strong>Buying suggestion:</strong> {other_action}</p>
</div>
""", unsafe_allow_html=True)

        fig_price_other = go.Figure()
        fig_price_other.add_trace(go.Scatter(
            x=["T1", "T2", "T3", "T4", "Now"],
            y=other_history,
            mode="lines+markers",
            name=other_product
        ))
        fig_price_other.update_layout(
            title=other_product,
            xaxis_title="Time",
            yaxis_title="Price",
            height=280,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_price_other, use_container_width=True)

    with other_right:
        st.write("**What it does well**")
        if other_strengths:
            for item in other_strengths:
                st.write(f"- {item}")
        else:
            st.write("- Balanced overall profile")

        st.write("**Things to keep in mind**")
        if other_cautions:
            for item in other_cautions:
                st.write(f"- {item}")
        else:
            st.write("- No major drawback in this comparison")

        st.write("**Key highlights**")
        for tag in get_product_tags(other_row, scored):
            st.markdown(f'<span class="tag">{tag}</span>', unsafe_allow_html=True)

    # ---------------------------------
    # 7. AI shopping insight
    # ---------------------------------
    st.subheader("7. AI shopping insight")
    st.markdown(
        '<div class="section-note">A concise summary of the key differences and trade-offs across the selected products.</div>',
        unsafe_allow_html=True
    )

    if st.button("Generate insight"):
        with st.spinner("Analyzing products..."):
            best_price = scored.loc[scored["price"].idxmin(), "product"]
            best_rating = scored.loc[scored["rating"].idxmax(), "product"]
            best_battery = scored.loc[scored["battery"].idxmax(), "product"]
            best_anc = scored.loc[scored["anc"].idxmax(), "product"]
            best_after_sale = scored.loc[scored["after_sale"].idxmax(), "product"]

            top_n = min(3, len(ranked))
            top_items = ranked.head(top_n)

            summary_lines = []
            for _, row in top_items.iterrows():
                strengths = build_strengths(row, scored)
                if not strengths:
                    strengths = ["balanced performance"]
                summary_lines.append(
                    f"- **{row['product']}** performs well in {', '.join(strengths[:3])}."
                )

            explanation_block = "\n".join(summary_lines)

            summary_text = f"""
### Shopping insight

Based on your current priorities, **{best_product}** is the strongest overall recommendation with a **match score of {best_row['overall_score_100']}/100**.

**Category leaders**
- Best value: **{best_price}**
- Best user reviews: **{best_rating}**
- Best battery life: **{best_battery}**
- Strongest noise cancellation: **{best_anc}**
- Best after-sale support: **{best_after_sale}**

**Top options**
{explanation_block}

**Bottom line**
If you want the product that best matches your needs right now, **{best_product}** is the strongest choice in this comparison set.
"""
            st.markdown(summary_text)

else:
    st.info("Please select at least one product.")
