import streamlit as st
import requests
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "https://confider-atom-resonate.ngrok-free.dev/emails/process-eml"
OCR_API_URL = "https://confider-atom-resonate.ngrok-free.dev/emails/extract-text"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Logistics Email Parser",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
    }

    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        color: #6b7280;
        font-size: 15px;
        margin-top: 5px;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 650;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    .route-box {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px;
        background: #ffffff;
        margin-bottom: 20px;
    }

    .location-label {
        font-size: 12px;
        color: #6b7280;
        font-weight: 600;
        text-transform: uppercase;
    }

    .location-name {
        font-size: 17px;
        font-weight: 650;
        margin-top: 5px;
    }

    .location-address {
        font-size: 14px;
        color: #6b7280;
        margin-top: 4px;
    }

    .arrow {
        text-align: center;
        font-size: 28px;
        color: #6b7280;
        padding-top: 25px;
    }

    .metric-card {
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 15px;
        background: #ffffff;
        text-align: center;
    }

    .metric-value {
        font-size: 23px;
        font-weight: 700;
    }

    .metric-label {
        font-size: 12px;
        color: #6b7280;
        margin-top: 3px;
    }

    .info-card {
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 15px;
        background: #ffffff;
        height: 100%;
    }

    .info-label {
        font-size: 12px;
        color: #6b7280;
        text-transform: uppercase;
    }

    .info-value {
        font-size: 17px;
        font-weight: 650;
        margin-top: 5px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_number(value, decimals=2):
    if value is None:
        return "-"

    try:
        return f"{float(value):,.{decimals}f}"
    except (ValueError, TypeError):
        return str(value)


def render_location(location, label):
    if not location:
        st.info(f"No {label.lower()} information found.")
        return

    company = location.get("name_or_company") or "Unknown company"
    address = location.get("raw_address") or "Address not available"
    city = location.get("city") or "-"
    country = location.get("country") or "-"

    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-label">{label}</div>
            <div class="info-value">{company}</div>
            <div class="location-address">{address}</div>
            <div class="location-address">
                {city}, {country}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_logistics_data(logistics_data):
    if not logistics_data:
        st.warning("No logistics data was extracted.")
        return

    pickup = logistics_data.get("pickup_location", {})
    drop = logistics_data.get("drop_location", {})
    cargo = logistics_data.get("cargo", [])

    transport_mode = logistics_data.get("transport_mode") or "-"
    incoterm = logistics_data.get("incoterm") or "-"

    # --------------------------------------------------------
    # Shipment Route
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Shipment Route</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([5, 1, 5])

    with col1:
        render_location(
            pickup,
            "Pickup",
        )

    with col2:
        st.markdown(
            '<div class="arrow">→</div>',
            unsafe_allow_html=True,
        )

    with col3:
        render_location(
            drop,
            "Drop",
        )

    st.write("")

    # --------------------------------------------------------
    # Shipment Information
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Shipment Information</div>',
        unsafe_allow_html=True,
    )

    info1, info2 = st.columns(2)

    with info1:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">Transport Mode</div>
                <div class="info-value">{transport_mode}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with info2:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">Incoterm</div>
                <div class="info-value">{incoterm}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

  


    # --------------------------------------------------------
    # Cargo Table
    # --------------------------------------------------------

    if cargo:

        cargo_rows = []

        for index, item in enumerate(cargo, start=1):

            cargo_rows.append(
                {
                    "#": index,
                    "Description": item.get(
                        "name_or_description",
                        "-"
                    ),
                    "Quantity": item.get(
                        "quantity"
                    ),
                    "Weight (kg)": item.get(
                        "weight_kg"
                    ),
                    "Volume (CBM)": item.get(
                        "volume_cbm"
                    ),
                }
            )

        cargo_df = pd.DataFrame(cargo_rows)

        st.dataframe(
            cargo_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "#": st.column_config.NumberColumn(
                    width="small"
                ),
                "Description": st.column_config.TextColumn(
                    width="large"
                ),
                "Quantity": st.column_config.NumberColumn(
                    format="%.0f"
                ),
                "Weight (kg)": st.column_config.NumberColumn(
                    format="%.2f"
                ),
                "Volume (CBM)": st.column_config.NumberColumn(
                    format="%.3f"
                ),
            },
        )

    else:
        st.info("No cargo information found.")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">Logistics Email Parser</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
        Upload an EML file to extract shipment, cargo,
        email and attachment information.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# EML PROCESSING
# ============================================================

st.markdown(
    '<div class="section-title">Email Processing</div>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Upload EML file",
    type=["eml"],
    key="eml_uploader",
)

if uploaded_file is not None:

    st.success(f"Selected: {uploaded_file.name}")

    if st.button(
        "Process Email",
        type="primary",
        use_container_width=False,
    ):

        with st.spinner(
            "Processing email and extracting shipment data..."
        ):

            try:

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "message/rfc822",
                    )
                }

                response = requests.post(
                    API_URL,
                    files=files,
                    timeout=120,
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success(
                        "Email processed successfully."
                    )

                    # ------------------------------------------------
                    # Get actual API data
                    # ------------------------------------------------

                    logistics_data = result.get(
                        "extracted_logistics_data",
                        {}
                    )

                    body_text = result.get(
                        "body_text",
                        ""
                    )

                    attachments = result.get(
                        "attachments",
                        []
                    )

                    # ------------------------------------------------
                    # Main Tabs
                    # ------------------------------------------------

                    tab1, tab2, tab3, tab4 = st.tabs(
                        [
                            "Shipment",
                            "Email Content",
                            "Attachments",
                            "API Response",
                        ]
                    )

                    # =================================================
                    # SHIPMENT TAB
                    # =================================================

                    with tab1:

                        render_logistics_data(
                            logistics_data
                        )

                    # =================================================
                    # EMAIL TAB
                    # =================================================

                    with tab2:

                        st.markdown(
                            '<div class="section-title">'
                            'Email Body'
                            '</div>',
                            unsafe_allow_html=True,
                        )

                        if body_text:

                            st.text_area(
                                "Extracted email content",
                                body_text,
                                height=500,
                                label_visibility="collapsed",
                            )

                        else:

                            st.info(
                                "No email body found."
                            )

                    # =================================================
                    # ATTACHMENTS TAB
                    # =================================================

                    with tab3:

                        st.markdown(
                            '<div class="section-title">'
                            'Attachments'
                            '</div>',
                            unsafe_allow_html=True,
                        )

                        if not attachments:

                            st.info(
                                "No attachments found."
                            )

                        else:

                            st.write(
                                f"Found {len(attachments)} attachment(s)."
                            )

                            for index, attachment in enumerate(
                                attachments,
                                start=1,
                            ):

                                filename = attachment.get(
                                    "filename",
                                    f"Attachment {index}",
                                )

                                content_type = attachment.get(
                                    "content_type",
                                    "-"
                                )

                                extracted_text = attachment.get(
                                    "extracted_text",
                                    ""
                                )

                                with st.expander(
                                    f"📎 {filename}",
                                    expanded=index == 1,
                                ):

                                    info1, info2 = st.columns(2)

                                    with info1:
                                        st.write(
                                            f"**Filename:** {filename}"
                                        )

                                    with info2:
                                        st.write(
                                            f"**Content Type:** "
                                            f"{content_type}"
                                        )

                                    st.divider()

                                    if extracted_text:

                                        st.text_area(
                                            "Extracted Text",
                                            extracted_text,
                                            height=400,
                                            key=f"attachment_{index}",
                                        )

                                    else:

                                        st.info(
                                            "No text extracted from "
                                            "this attachment."
                                        )

                    # =================================================
                    # API RESPONSE TAB
                    # =================================================

                    with tab4:

                        st.markdown(
                            '<div class="section-title">'
                            'Complete API Response'
                            '</div>',
                            unsafe_allow_html=True,
                        )

                        st.json(result)

                else:

                    st.error(
                        f"API returned status "
                        f"{response.status_code}"
                    )

                    try:
                        st.json(response.json())
                    except Exception:
                        st.code(response.text)

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to FastAPI. "
                    "Make sure the API server is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "Request timed out. "
                    "The email may take longer to process."
                )

            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )


# ============================================================
# OCR SECTION
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">Document OCR</div>',
    unsafe_allow_html=True,
)

st.caption(
    "Upload an image or scanned PDF to extract text using PaddleOCR."
)

ocr_file = st.file_uploader(
    "Upload Image or PDF",
    type=[
        "pdf",
        "jpg",
        "jpeg",
        "png",
        "bmp",
        "tiff",
        "tif",
        "webp",
    ],
    key="ocr_uploader",
)

if ocr_file is not None:

    st.success(
        f"Selected: {ocr_file.name}"
    )

    if st.button(
        "Extract Text",
        type="primary",
        key="extract_text_button",
    ):

        with st.spinner(
            "Extracting text using PaddleOCR..."
        ):

            try:

                files = {
                    "file": (
                        ocr_file.name,
                        ocr_file.getvalue(),
                        ocr_file.type,
                    )
                }

                ocr_response = requests.post(
                    OCR_API_URL,
                    files=files,
                    timeout=300,
                )

                if ocr_response.status_code == 200:

                    ocr_result = ocr_response.json()

                    st.success(
                        "Text extracted successfully."
                    )

                    ocr_tab1, ocr_tab2 = st.tabs(
                        [
                            "Extracted Text",
                            "OCR API Response",
                        ]
                    )

                    # ---------------------------------------------
                    # Extracted text
                    # ---------------------------------------------

                    with ocr_tab1:

                        extracted_text = ocr_result.get(
                            "extracted_text",
                            ""
                        )

                        if extracted_text:

                            st.text_area(
                                "PaddleOCR Output",
                                extracted_text,
                                height=600,
                                label_visibility="collapsed",
                            )

                        else:

                            st.info(
                                "No text was extracted."
                            )

                    # ---------------------------------------------
                    # OCR response
                    # ---------------------------------------------

                    with ocr_tab2:

                        st.json(
                            ocr_result
                        )

                else:

                    st.error(
                        f"OCR API returned status "
                        f"{ocr_response.status_code}"
                    )

                    try:
                        st.json(
                            ocr_response.json()
                        )
                    except Exception:
                        st.code(
                            ocr_response.text
                        )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to FastAPI."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "OCR request timed out."
                )

            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )