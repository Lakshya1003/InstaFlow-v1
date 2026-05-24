import streamlit as st

def render_info_page():
    # ── Retro HTML helpers ──
    WC = '<div class="retro-wc"><div class="retro-wc-btn">─</div><div class="retro-wc-btn">□</div><div class="retro-wc-btn">✕</div></div>'

    def rwin_open(title, icon=""):
        return f'<div class="retro-window"><div class="retro-titlebar"><span class="retro-titlebar-text">{icon} {title}</span>{WC}</div><div class="retro-body" style="padding: 24px;">'

    def rwin_close():
        return '</div></div>'

    # ── HEADER ──
    st.markdown(f"""
    <div class="header-bar">
        <div class="retro-titlebar">
            <span class="retro-titlebar-text">ℹ️ SYSTEM DOCUMENTATION TERMINAL</span>
            <div style="display:flex;align-items:center;gap:8px;">
                {WC}
            </div>
        </div>
        <div class="header-content" style="padding: 30px;">
            <span style="font-size:2.5rem; margin-right: 20px;">🎓</span>
            <div>
                <p class="header-title" style="font-size:2rem; margin-bottom: 5px;">WELCOME TO INSIGHT FLOW</p>
                <p class="header-subtitle" style="font-size:1.1rem; opacity: 0.9;">AI-Assisted Conversational Analytics Workstation</p>
            </div>
        </div>
    </div>
    <div style="margin-bottom: 20px;"></div>
    """, unsafe_allow_html=True)

    # ── BACK BUTTON ──
    cc1, cc2, cc3 = st.columns([1, 2, 1])
    with cc2:
        if st.button("🔙 RETURN TO WORKSTATION", use_container_width=True, type="primary"):
            st.session_state['show_info_page'] = False
            st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])

    with c1:
        # SECTION 2 — WHAT THIS SOFTWARE DOES
        st.markdown(rwin_open("WHAT THIS SOFTWARE DOES", "⚙️"), unsafe_allow_html=True)
        st.markdown("""
        **Insight Flow** is a lightweight analytical utility designed to reduce time spent in spreadsheets. It enables you to:
        * Generate visual analytics instantly.
        * Interact with structured data conversationally using AI.
        * Explore KPIs, trends, and growth metrics.
        * Export AI-assisted PDF executive reports.

        **Note:** This is a temporary session workflow. There is no permanent storage.
        
        <div style="padding: 10px; border-left: 4px solid var(--titlebar); background: var(--bg-inner); margin-top: 15px;">
            <b>IMPORTANT:</b> This software is designed for lightweight exploratory analytical visualization, not enterprise-scale forecasting.
        </div>
        """, unsafe_allow_html=True)
        st.markdown(rwin_close(), unsafe_allow_html=True)

        # SECTION 4 — AI USAGE POLICY
        st.markdown(rwin_open("AI SYSTEM LIMITATIONS", "🤖"), unsafe_allow_html=True)
        st.markdown("""
        The integrated Gemini AI operates under strict boundary conditions:
        * **Dataset-Constrained:** AI responses are isolated to the scope of your uploaded CSV.
        * **Rejection Protocol:** Unsupported questions (e.g., weather, sports, politics, general knowledge) will be rejected.
        * **No External Web Access:** The AI does not browse the unrestricted internet to answer queries.

        <div style="padding: 10px; border-left: 4px solid var(--accent-red); background: var(--bg-inner); margin-top: 15px;">
            <b>CRITICAL:</b> Gemini assists in interpretation but does NOT replace deterministic mathematical analytics calculations. Always verify critical business insights.
        </div>
        """, unsafe_allow_html=True)
        st.markdown(rwin_close(), unsafe_allow_html=True)

        # SECTION 6 — PRIVACY & SESSION POLICY
        st.markdown(rwin_open("STATELESS PRIVACY ARCHITECTURE", "🛡️"), unsafe_allow_html=True)
        st.markdown("""
        Insight Flow is built on a strict privacy-first foundation:
        * **No Permanent Storage:** Uploaded datasets remain entirely temporary and in-memory.
        * **Ephemeral Sessions:** All data, API keys, and AI conversations disappear immediately after a browser refresh or session end.
        * **Local API Keys:** Your Gemini API key is used strictly for the active session and is not stored in any database.
        
        This architecture ensures absolute business privacy and security for your sensitive data logs.
        """, unsafe_allow_html=True)
        st.markdown(rwin_close(), unsafe_allow_html=True)

        # SECTION 7 — SOFTWARE LIMITATIONS
        st.markdown(rwin_open("SOFTWARE LIMITATIONS", "⚠️"), unsafe_allow_html=True)
        st.markdown("""
        * Designed for lightweight, exploratory analytics.
        * **Not** enterprise-scale data infrastructure.
        * **Not** a real-time streaming platform.
        * **Not** a predictive forecasting engine.
        * **Not** a replacement for full-scale Enterprise BI systems (e.g., Tableau, PowerBI).
        """, unsafe_allow_html=True)
        st.markdown(rwin_close(), unsafe_allow_html=True)

    with c2:
        # SECTION 3 — CSV FORMATTING GUIDE
        st.markdown(rwin_open("CSV REQUIREMENTS & FORMATTING", "📄"), unsafe_allow_html=True)
        st.markdown("""
        For the system to automatically extract KPIs and build dashboards, your CSV must meet these structural requirements:

        **Required Columns:**
        1. At least one **Date** column.
        2. At least one **Numeric** column (e.g., Revenue, Quantity).

        **Recommended Columns:**
        * Categorical columns (e.g., Region, Product, Status) for breakdown views.

        **Supported Date Formats:**
        The system automatically attempts flexible parsing for:
        `YYYY-MM-DD` | `MM/DD/YYYY` | `DD-MM-YYYY`
        """)

        st.markdown("""
        **Example Valid Structure:**
        <div style="overflow-x:auto; margin-top:10px; margin-bottom:15px;">
            <table style="width:100%; border-collapse:collapse; font-family:monospace; font-size:0.9rem; background:var(--bg-white); border: 2px solid var(--border);">
                <thead>
                    <tr style="background:var(--bg-inner); border-bottom:2px solid var(--border);">
                        <th style="padding:8px; border-right:1px solid var(--border-light); text-align:left;">Date</th>
                        <th style="padding:8px; border-right:1px solid var(--border-light); text-align:left;">Region</th>
                        <th style="padding:8px; border-right:1px solid var(--border-light); text-align:left;">Product</th>
                        <th style="padding:8px; border-right:1px solid var(--border-light); text-align:right;">Revenue</th>
                        <th style="padding:8px; text-align:right;">Qty</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom:1px solid var(--border-light);">
                        <td style="padding:8px; border-right:1px solid var(--border-light);">2023-01-15</td>
                        <td style="padding:8px; border-right:1px solid var(--border-light);">North</td>
                        <td style="padding:8px; border-right:1px solid var(--border-light);">Software</td>
                        <td style="padding:8px; border-right:1px solid var(--border-light); text-align:right;">1500.50</td>
                        <td style="padding:8px; text-align:right;">10</td>
                    </tr>
                    <tr style="border-bottom:1px solid var(--border-light);">
                        <td style="padding:8px; border-right:1px solid var(--border-light);">2023-01-16</td>
                        <td style="padding:8px; border-right:1px solid var(--border-light);">South</td>
                        <td style="padding:8px; border-right:1px solid var(--border-light);">Hardware</td>
                        <td style="padding:8px; border-right:1px solid var(--border-light); text-align:right;">850.00</td>
                        <td style="padding:8px; text-align:right;">5</td>
                    </tr>
                    <tr>
                        <td style="padding:8px; border-right:1px solid var(--border-light);">2023-01-17</td>
                        <td style="padding:8px; border-right:1px solid var(--border-light);">North</td>
                        <td style="padding:8px; border-right:1px solid var(--border-light);">Hardware</td>
                        <td style="padding:8px; border-right:1px solid var(--border-light); text-align:right;">1200.00</td>
                        <td style="padding:8px; text-align:right;">8</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        **✅ Supported Data:** Sales datasets, E-commerce logs, Business KPIs, Website analytics, Time-series data.
        <br>**❌ Unsupported Data:** Unstructured text, PDFs, Images, Scanned documents, Corrupted CSV files.
        """, unsafe_allow_html=True)
        st.markdown(rwin_close(), unsafe_allow_html=True)

        # SECTION 5 — TERMS & CONDITIONS
        st.markdown(rwin_open("TERMS & CONDITIONS", "⚖️"), unsafe_allow_html=True)
        st.markdown("""
        By using Insight Flow, you agree to the following lightweight software terms:
        * **As-Is Provision:** This tool is provided "as-is" without any warranty or performance guarantees.
        * **Verification:** Analytical and AI-generated results should be independently verified before making critical business decisions.
        * **User Responsibility:** You are solely responsible for the legality and content of the datasets you upload.
        * **API Usage:** You are responsible for any external billing related to your personal Gemini API key.
        * **Compliance:** Users must comply with applicable data protection laws.
        """, unsafe_allow_html=True)
        st.markdown(rwin_close(), unsafe_allow_html=True)

    # ── CHECKLIST & START BUTTON ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(rwin_open("BEFORE YOU CONTINUE CHECKLIST", "✅"), unsafe_allow_html=True)
    
    st.markdown("""
    <div style="font-family: monospace; font-size: 1.1rem; line-height: 1.8;">
        ☑ My dataset contains a Date column.<br>
        ☑ My dataset contains numerical metrics.<br>
        ☑ I understand sessions are temporary and disappear upon refresh.<br>
        ☑ I understand Gemini API usage is my responsibility.<br>
        ☑ I understand unsupported non-dataset queries may be rejected.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cc1, cc2, cc3 = st.columns([1, 2, 1])
    with cc2:
        if st.button("🚀 I UNDERSTAND — CONTINUE TO INSIGHT FLOW", use_container_width=True, type="primary"):
            st.session_state['show_info_page'] = False
            st.rerun()

    st.markdown(rwin_close(), unsafe_allow_html=True)

    # ── Footer ──
    st.markdown(f"""<div class="retro-footer"><p>
    Insight Flow v1.0 — System Documentation & Onboarding Utility
    </p></div>""", unsafe_allow_html=True)
