"""
MTRX-TriAxis | PDF Upload Page
Upload and process curriculum PDFs through the AI pipeline.
"""

import streamlit as st
import os

from backend.pdf_processor import save_pdf, process_pdf
from backend.rag_pipeline import create_vectorstore, add_to_vectorstore, vectorstore_exists


st.markdown("# 📄 Upload Curriculum PDF")
st.markdown("Upload a textbook or curriculum PDF to process it through the AI pipeline.")
st.markdown("---")

# ----- File Upload -----
uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"],
    help="Upload a curriculum or textbook PDF. The AI will extract, clean, chunk, and index the content.",
)

# ----- Processing Options -----
col1, col2 = st.columns(2)
with col1:
    use_llm_chunker = st.toggle(
        "Smart Chunking (LLM)",
        value=True,
        help="Use LLM to create intelligent chunks. Disable for faster basic splitting.",
    )
with col2:
    append_mode = st.toggle(
        "Append to existing curriculum",
        value=True if vectorstore_exists() else False,
        help="If ON, adds to existing content. If OFF, replaces everything.",
    )

# ----- Process Button -----
if uploaded_file is not None:
    st.markdown("---")
    st.markdown(f"**File:** `{uploaded_file.name}` ({uploaded_file.size / 1024:.1f} KB)")

    if st.button("🚀 Process PDF", type="primary", use_container_width=True):
        # Save the uploaded file
        with st.spinner("Saving file..."):
            file_path = save_pdf(uploaded_file)
            st.success(f"✅ File saved to `{file_path}`")

        # Processing pipeline with progress
        progress_bar = st.progress(0, text="Starting pipeline...")

        # Step 1: Extract & Clean & Chunk
        try:
            progress_bar.progress(10, text="📄 Extracting text from PDF...")

            with st.status("🔄 Processing PDF...", expanded=True) as status:
                st.write("📄 Extracting text from PDF...")
                progress_bar.progress(20, text="📄 Extracting text...")

                chunks = process_pdf(file_path, use_llm_chunker=use_llm_chunker)
                progress_bar.progress(60, text="✂️ Chunking complete...")

                if not chunks:
                    st.error("❌ No content could be extracted from the PDF.")
                    st.stop()

                st.write(f"✅ Created **{len(chunks)} chunks** from the PDF")

                # Step 2: Create/Update vector store
                st.write("📊 Creating embeddings and storing in vector database...")
                progress_bar.progress(70, text="📊 Building vector store...")

                if append_mode and vectorstore_exists():
                    add_to_vectorstore(chunks)
                    st.write("✅ Added to existing vector store")
                else:
                    create_vectorstore(chunks)
                    st.write("✅ Vector store created")

                progress_bar.progress(100, text="✅ Pipeline complete!")
                status.update(label="✅ Processing Complete!", state="complete")

            # Store chunks in session state for preview
            st.session_state["last_chunks"] = chunks

        except Exception as e:
            st.error(f"❌ Error during processing: {str(e)}")
            st.exception(e)

# ----- Chunk Preview -----
if "last_chunks" in st.session_state and st.session_state["last_chunks"]:
    st.markdown("---")
    st.markdown("### 📋 Processed Chunks Preview")

    chunks = st.session_state["last_chunks"]
    st.info(f"Showing {min(10, len(chunks))} of {len(chunks)} total chunks")

    for i, chunk in enumerate(chunks[:10]):
        with st.expander(f"📌 {chunk.get('title', f'Chunk {i+1}')}", expanded=(i == 0)):
            st.markdown(chunk.get("content", "No content"))
            st.caption(f"Length: {len(chunk.get('content', ''))} characters")

# ----- Existing Files -----
st.markdown("---")
st.markdown("### 📁 Uploaded Files")

upload_dir = "data/uploads"
if os.path.exists(upload_dir):
    files = [f for f in os.listdir(upload_dir) if f.endswith(".pdf")]
    if files:
        for f in files:
            file_size = os.path.getsize(os.path.join(upload_dir, f)) / 1024
            st.markdown(f"- 📄 `{f}` ({file_size:.1f} KB)")
    else:
        st.caption("No files uploaded yet.")
else:
    st.caption("No files uploaded yet.")
