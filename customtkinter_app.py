"""
customtkinter_app.py
"""

import threading
import importlib
import customtkinter as ctk

mod_docs = importlib.import_module("documents")
load_documents = mod_docs.load_documents

mod_prep = importlib.import_module("preprocessing")
preprocess_documents = mod_prep.preprocess_documents

mod_chunk = importlib.import_module("chunking")
build_chunks = mod_chunk.build_chunks

mod_vec = importlib.import_module("vector_representation")
hybrid_search = mod_vec.hybrid_search

mod_ret = importlib.import_module("retrieve_context")
build_context = mod_ret.build_context

rag_prompt = importlib.import_module("prompting")

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class CampusRAGDesktopApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Campus RAG Knowledge Assistant - Desktop Edition")
        self.geometry("1000x750")
        self.minsize(850, 600)

        raw_docs = load_documents()
        clean_docs = preprocess_documents(raw_docs)
        self.chunks = build_chunks(clean_docs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # -------------------------------------------------------------
        # 1. شريط التحكم العلوي (Header & Controls)
        # -------------------------------------------------------------
        self.control_frame = ctk.CTkFrame(self, corner_radius=12)
        self.control_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.control_frame.grid_columnconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(
            self.control_frame,
            text="🎓 Campus RAG Assistant",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=15, pady=12, sticky="w")

        self.slider_label = ctk.CTkLabel(
            self.control_frame,
            text="Alpha (BM25 vs Dense): 0.50",
            font=ctk.CTkFont(size=12)
        )
        self.slider_label.grid(row=0, column=2, padx=(10, 5), pady=12)

        self.alpha_slider = ctk.CTkSlider(
            self.control_frame,
            from_=0.0,
            to=1.0,
            number_of_steps=20,
            command=self.update_slider_label,
            width=150
        )
        self.alpha_slider.set(0.50)
        self.alpha_slider.grid(row=0, column=3, padx=(0, 15), pady=12)

        # -------------------------------------------------------------
        # 2. منطقة الإدخال وزر الاستعلام (Input Area)
        # -------------------------------------------------------------
        self.input_frame = ctk.CTkFrame(self, corner_radius=12)
        self.input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.query_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Ask a question (e.g., How much does it cost to print black and white or color pages?)...",
            height=45,
            font=ctk.CTkFont(size=13)
        )
        self.query_entry.grid(row=0, column=0, padx=(15, 10), pady=15, sticky="ew")
        self.query_entry.bind("<Return>", lambda event: self.start_rag_pipeline())

        self.ask_btn = ctk.CTkButton(
            self.input_frame,
            text="Run RAG Search",
            height=45,
            width=150,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.start_rag_pipeline
        )
        self.ask_btn.grid(row=0, column=1, padx=(0, 15), pady=15)

        # -------------------------------------------------------------
        # 3. صندوق عرض النتائج والشرح المفصل (Detailed Results Box)
        # -------------------------------------------------------------
        self.result_box = ctk.CTkTextbox(
            self,
            wrap="word",
            font=ctk.CTkFont(size=13, family="Consolas"),
            corner_radius=12
        )
        self.result_box.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        welcome_text = (
            f"Ready.\n"
            f"Loaded {len(self.chunks)} knowledge base chunks.\n"
            f"Architecture: Hybrid BM25 + all-MiniLM-L6-v2 Embeddings + Grounded Citations.\n"
            f"Type your query above and press Enter."
        )
        self.result_box.insert("0.0", welcome_text)

        # -------------------------------------------------------------
        # 4. شريط الحالة بالأسفل (Status Bar)
        # -------------------------------------------------------------
        self.status_bar = ctk.CTkLabel(
            self,
            text="Status: Ready",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.status_bar.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="w")

    def update_slider_label(self, val):
        self.slider_label.configure(text=f"Alpha (BM25 vs Dense): {val:.2f}")

    def start_rag_pipeline(self):
        query = self.query_entry.get().strip()
        if not query:
            return

        self.ask_btn.configure(state="disabled")
        self.status_bar.configure(text="Status: Retrieving context, filtering outdated sources, and generating grounded answer...")
        self.result_box.delete("0.0", "end")
        self.result_box.insert("0.0", "Processing query through RAG pipeline, please wait...")

        threading.Thread(target=self._run_inference, args=(query,), daemon=True).start()

    def _run_inference(self, query):
        alpha_val = float(self.alpha_slider.get())
        try:
            candidates = hybrid_search(query, self.chunks, alpha=alpha_val, top_k=4)

            context, surviving, dropped = build_context(candidates)

            answer = rag_prompt.answer_question(query, context)

            output = []
            output.append("=" * 85)
            output.append("💡 GENERATED GROUNDED ANSWER")
            output.append("=" * 85)
            output.append(f"{answer}\n")

            output.append("-" * 85)
            output.append("📑 RETAINED CONTEXT SOURCES (Passed to LLM)")
            output.append("-" * 85)
            for idx, s in enumerate(surviving, start=1):
                output.append(
                    f"[Source {idx}] ID: {s['chunk_id']} | Title: {s['title']} | Status: {s['status']}\n"
                    f"Hybrid Score: {s['hybrid_score']:.4f} (BM25: {s['bm25_score']:.2f}, Dense: {s['embedding_score']:.4f})\n"
                    f"Excerpt: {s['chunk_text']}\n"
                )

            output.append("-" * 85)
            output.append("🚫 DROPPED / FILTERED SOURCES (Outdated Policy Prevention)")
            output.append("-" * 85)
            if dropped:
                for d in dropped:
                    output.append(f"- Chunk: {d['chunk_id']} | Title: {d['title']} -> Reason: {d['reason']}")
            else:
                output.append("No candidates were filtered out.")

            final_text = "\n".join(output)

            self.result_box.delete("0.0", "end")
            self.result_box.insert("0.0", final_text)
            self.status_bar.configure(text=f"Status: Success | Completed query: '{query[:35]}...'")

        except Exception as e:
            self.result_box.delete("0.0", "end")
            self.result_box.insert("0.0", f"Error encountered during RAG execution:\n{e}")
            self.status_bar.configure(text="Status: Execution Error")

        finally:
            self.ask_btn.configure(state="normal")


if __name__ == "__main__":
    app = CampusRAGDesktopApp()
    app.mainloop()