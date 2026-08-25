# import streamlit as st
# import requests


# # -----------------------------
# # Configuration
# # -----------------------------
# API_URL = "http://127.0.0.1:8000/emails/process-eml"


# # -----------------------------
# # Page Configuration
# # -----------------------------
# st.set_page_config(
#     page_title="EML Parser",
#     page_icon="📧",
#     layout="wide",
# )


# # -----------------------------
# # Header
# # -----------------------------
# st.title("📧 EML Email Parser")
# st.write(
#     "Upload an EML file to extract email body, attachments, "
#     "and attachment text."
# )

# st.divider()


# # -----------------------------
# # File Upload
# # -----------------------------
# uploaded_file = st.file_uploader(
#     "Upload EML file",
#     type=["eml"],
# )


# # -----------------------------
# # Process File
# # -----------------------------
# if uploaded_file is not None:

#     st.success(f"File selected: {uploaded_file.name}")

#     if st.button("🚀 Process Email", type="primary"):

#         with st.spinner("Processing EML file..."):

#             try:
#                 files = {
#                     "file": (
#                         uploaded_file.name,
#                         uploaded_file.getvalue(),
#                         "message/rfc822",
#                     )
#                 }

#                 response = requests.post(
#                     API_URL,
#                     files=files,
#                     timeout=120,
#                 )

#                 # -----------------------------
#                 # Success
#                 # -----------------------------
#                 if response.status_code == 200:

#                     result = response.json()

#                     st.success("Email processed successfully!")

#                     st.divider()

#                     # -----------------------------
#                     # Tabs
#                     # -----------------------------
#                     tab4, tab1, tab2, tab3 = st.tabs(
#                         [
#                             "🚚 Logistics Data",
#                             "📧 Email Content",
#                             "📎 Attachments",
#                             "🔧 API Response",
#                         ]
#                     )

#                     # -----------------------------
#                     # Logistics Data
#                     # -----------------------------
#                     with tab4:

#                         st.subheader("🚚 Extracted Logistics Data")

#                         # Dummy logistics response for now
#                         logistics_data = {
#                             "pickup_location": {
#                                 "raw_address": "Koper Port, Slovenia",
#                                 "name_or_company": None,
#                                 "city": "Koper",
#                                 "country": "Slovenia"
#                             },
#                             "drop_location": {
#                                 "raw_address": "Svetosavska 394d, 11460 Beograd-Barajevo, Serbia",
#                                 "name_or_company": "Kolektor Etra d.o.o. Beograd",
#                                 "city": "Beograd-Barajevo",
#                                 "country": "Serbia"
#                             },
#                             "cargo": [
#                                 {
#                                     "name_or_description": "FCL cargo - 40OT (Open Top) container",
#                                     "quantity": None,
#                                     "weight_kg": 14763.00,
#                                     "volume_cbm": 70.00
#                                 }
#                             ],
#                             "transport_mode": "Sea freight - FCL, 40ft Open Top container (Export, via Koper Port)",
#                             "incoterm": None
#                         }

#                         st.json(logistics_data)

#                     # -----------------------------
#                     # Email Body
#                     # -----------------------------
#                     with tab1:

#                         st.subheader("Email Body")

#                         body_text = result.get(
#                             "body_text",
#                             ""
#                         )

#                         if body_text:
#                             st.text_area(
#                                 "Extracted Body",
#                                 body_text,
#                                 height=400,
#                             )
#                         else:
#                             st.info("No email body found.")

#                     # -----------------------------
#                     # Attachments
#                     # -----------------------------
#                     with tab2:

#                         st.subheader("Attachments")

#                         attachments = result.get(
#                             "attachments",
#                             []
#                         )

#                         if not attachments:
#                             st.info("No attachments found.")

#                         else:

#                             st.write(
#                                 f"Found {len(attachments)} attachment(s)"
#                             )

#                             for index, attachment in enumerate(
#                                 attachments,
#                                 start=1,
#                             ):

#                                 filename = attachment.get(
#                                     "filename",
#                                     f"Attachment {index}",
#                                 )

#                                 with st.expander(
#                                     f"📎 {filename}"
#                                 ):

#                                     st.write(
#                                         "**Filename:**",
#                                         filename,
#                                     )

#                                     content_type = attachment.get(
#                                         "content_type"
#                                     )

#                                     if content_type:
#                                         st.write(
#                                             "**Content Type:**",
#                                             content_type,
#                                         )

#                                     extracted_text = attachment.get(
#                                         "extracted_text",
#                                         ""
#                                     )

#                                     if extracted_text:

#                                         st.subheader(
#                                             "Extracted Text"
#                                         )

#                                         st.text_area(
#                                             "Text",
#                                             extracted_text,
#                                             height=350,
#                                             key=f"attachment_{index}",
#                                         )

#                                     else:
#                                         st.info(
#                                             "No text extracted from this attachment."
#                                         )

#                     # -----------------------------
#                     # Complete API Response
#                     # -----------------------------
#                     with tab3:

#                         st.subheader("Complete API Response")

#                         st.json(result)

#                 # -----------------------------
#                 # API Error
#                 # -----------------------------
#                 else:

#                     st.error(
#                         f"API returned status "
#                         f"{response.status_code}"
#                     )

#                     try:
#                         st.json(response.json())

#                     except Exception:
#                         st.code(response.text)

#             except requests.exceptions.ConnectionError:

#                 st.error(
#                     "Could not connect to FastAPI. "
#                     "Make sure the FastAPI server is running."
#                 )

#             except requests.exceptions.Timeout:

#                 st.error(
#                     "API request timed out."
#                 )

#             except Exception as e:

#                 st.error(
#                     f"Something went wrong: {str(e)}"
#                 )

import streamlit as st
import requests


# -----------------------------
# Configuration
# -----------------------------
API_URL = "http://127.0.0.1:8000/emails/process-eml"
OCR_API_URL = "http://127.0.0.1:8000/emails/extract-text"


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="EML Parser",
    page_icon="📧",
    layout="wide",
)


# -----------------------------
# Header
# -----------------------------
st.title("📧 EML Email Parser")
st.write(
    "Upload an EML file to extract email body, attachments, "
    "and attachment text."
)

st.divider()


# ============================================================
# EML PROCESSING
# ============================================================

st.header("📧 EML Processing")

# -----------------------------
# File Upload
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload EML file",
    type=["eml"],
    key="eml_uploader",
)


# -----------------------------
# Process File
# -----------------------------
if uploaded_file is not None:

    st.success(f"File selected: {uploaded_file.name}")

    if st.button("🚀 Process Email", type="primary"):

        with st.spinner("Processing EML file..."):

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

                # -----------------------------
                # Success
                # -----------------------------
                if response.status_code == 200:

                    result = response.json()

                    st.success("Email processed successfully!")

                    st.divider()

                    # -----------------------------
                    # Tabs
                    # -----------------------------
                    tab4, tab1, tab2, tab3 = st.tabs(
                        [
                            "🚚 Logistics Data",
                            "📧 Email Content",
                            "📎 Attachments",
                            "🔧 API Response",
                        ]
                    )

                    # -----------------------------
                    # Logistics Data
                    # -----------------------------
                    with tab4:

                        st.subheader("🚚 Extracted Logistics Data")

                        # Dummy logistics response for now
                        logistics_data = {
                            "pickup_location": {
                                "raw_address": "Koper Port, Slovenia",
                                "name_or_company": None,
                                "city": "Koper",
                                "country": "Slovenia"
                            },
                            "drop_location": {
                                "raw_address": "Svetosavska 394d, 11460 Beograd-Barajevo, Serbia",
                                "name_or_company": "Kolektor Etra d.o.o. Beograd",
                                "city": "Beograd-Barajevo",
                                "country": "Serbia"
                            },
                            "cargo": [
                                {
                                    "name_or_description": "FCL cargo - 40OT (Open Top) container",
                                    "quantity": None,
                                    "weight_kg": 14763.00,
                                    "volume_cbm": 70.00
                                }
                            ],
                            "transport_mode": "Sea freight - FCL, 40ft Open Top container (Export, via Koper Port)",
                            "incoterm": None
                        }

                        st.json(logistics_data)

                    # -----------------------------
                    # Email Body
                    # -----------------------------
                    with tab1:

                        st.subheader("Email Body")

                        body_text = result.get(
                            "body_text",
                            ""
                        )

                        if body_text:
                            st.text_area(
                                "Extracted Body",
                                body_text,
                                height=400,
                            )
                        else:
                            st.info("No email body found.")

                    # -----------------------------
                    # Attachments
                    # -----------------------------
                    with tab2:

                        st.subheader("Attachments")

                        attachments = result.get(
                            "attachments",
                            []
                        )

                        if not attachments:
                            st.info("No attachments found.")

                        else:

                            st.write(
                                f"Found {len(attachments)} attachment(s)"
                            )

                            for index, attachment in enumerate(
                                attachments,
                                start=1,
                            ):

                                filename = attachment.get(
                                    "filename",
                                    f"Attachment {index}",
                                )

                                with st.expander(
                                    f"📎 {filename}"
                                ):

                                    st.write(
                                        "**Filename:**",
                                        filename,
                                    )

                                    content_type = attachment.get(
                                        "content_type"
                                    )

                                    if content_type:
                                        st.write(
                                            "**Content Type:**",
                                            content_type,
                                        )

                                    extracted_text = attachment.get(
                                        "extracted_text",
                                        ""
                                    )

                                    if extracted_text:

                                        st.subheader(
                                            "Extracted Text"
                                        )

                                        st.text_area(
                                            "Text",
                                            extracted_text,
                                            height=350,
                                            key=f"attachment_{index}",
                                        )

                                    else:
                                        st.info(
                                            "No text extracted from this attachment."
                                        )

                    # -----------------------------
                    # Complete API Response
                    # -----------------------------
                    with tab3:

                        st.subheader("Complete API Response")

                        st.json(result)

                # -----------------------------
                # API Error
                # -----------------------------
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
                    "Make sure the FastAPI server is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "API request timed out."
                )

            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )


# ============================================================
# IMAGE / PDF OCR PROCESSING
# ============================================================

st.divider()

st.header("📄 Image / PDF OCR")

st.write(
    "Upload an image or scanned PDF to extract text using PaddleOCR."
)


# -----------------------------
# Image / PDF Upload
# -----------------------------
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


# -----------------------------
# Process OCR File
# -----------------------------
if ocr_file is not None:

    st.success(f"File selected: {ocr_file.name}")

    if st.button(
        "🔍 Extract Text",
        type="primary",
        key="extract_text_button",
    ):

        with st.spinner(
            "Extracting text using PaddleOCR..."
        ):

            try:

                # -----------------------------
                # Prepare file
                # -----------------------------
                files = {
                    "file": (
                        ocr_file.name,
                        ocr_file.getvalue(),
                        ocr_file.type,
                    )
                }

                # -----------------------------
                # Call OCR API
                # -----------------------------
                ocr_response = requests.post(
                    OCR_API_URL,
                    files=files,
                    timeout=300,
                )

                # -----------------------------
                # Success
                # -----------------------------
                if ocr_response.status_code == 200:

                    ocr_result = ocr_response.json()

                    st.success(
                        "Text extracted successfully!"
                    )

                    st.divider()

                    # -----------------------------
                    # OCR Tabs
                    # -----------------------------
                    dummy_tab, actual_tab, response_tab = st.tabs(
                        [
                            "🚚 Dummy Logistics Data",
                            "📝 Actual Extracted Text",
                            "🔧 OCR API Response",
                        ]
                    )

                    # ==================================================
                    # Dummy Logistics Data
                    # ==================================================
                    with dummy_tab:

                        st.subheader(
                            "🚚 Extracted Logistics Data"
                        )

                        # Dummy response for now
                        logistics_data = {
                            "pickup_location": {
                                "raw_address": "Koper Port, Slovenia",
                                "name_or_company": None,
                                "city": "Koper",
                                "country": "Slovenia"
                            },
                            "drop_location": {
                                "raw_address": "Svetosavska 394d, 11460 Beograd-Barajevo, Serbia",
                                "name_or_company": "Kolektor Etra d.o.o. Beograd",
                                "city": "Beograd-Barajevo",
                                "country": "Serbia"
                            },
                            "cargo": [
                                {
                                    "name_or_description": "FCL cargo - 40OT (Open Top) container",
                                    "quantity": None,
                                    "weight_kg": 14763.00,
                                    "volume_cbm": 70.00
                                }
                            ],
                            "transport_mode": "Sea freight - FCL, 40ft Open Top container (Export, via Koper Port)",
                            "incoterm": None
                        }

                        st.json(logistics_data)

                    # ==================================================
                    # Actual OCR Extracted Text
                    # ==================================================
                    with actual_tab:

                        st.subheader(
                            "📝 Actual Extracted Text"
                        )

                        extracted_text = ocr_result.get(
                            "extracted_text",
                            ""
                        )

                        if extracted_text:

                            st.text_area(
                                "PaddleOCR Output",
                                extracted_text,
                                height=600,
                            )

                        else:

                            st.info(
                                "No text was extracted from this file."
                            )

                    # ==================================================
                    # OCR API Response
                    # ==================================================
                    with response_tab:

                        st.subheader(
                            "🔧 OCR API Response"
                        )

                        st.json(ocr_result)

                # -----------------------------
                # OCR API Error
                # -----------------------------
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
                    "Could not connect to FastAPI. "
                    "Make sure the FastAPI server is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "OCR request timed out."
                )

            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )