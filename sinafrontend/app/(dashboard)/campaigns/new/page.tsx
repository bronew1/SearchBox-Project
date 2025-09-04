"use client";

import { useEffect, useRef, useState } from "react";

declare global {
  interface Window {
    unlayer: any;
  }
}

export default function CreateTemplatePage() {
  const [title, setTitle] = useState("");
  const editorRef = useRef<HTMLDivElement>(null);
  const unlayerRef = useRef<any>(null);

  useEffect(() => {
    if (typeof window !== "undefined" && window.unlayer && editorRef.current) {
      // Container içini temizle
      editorRef.current.innerHTML = "";

      // Yeni bir div oluştur
      const newDiv = document.createElement("div");
      newDiv.id = "editor";
      newDiv.style.height = "100%";
      newDiv.style.width = "100%";

      editorRef.current.appendChild(newDiv);

      // Init
      window.unlayer.init({
        id: "editor",
        displayMode: "email",
        source: undefined,
      });

      unlayerRef.current = window.unlayer;
    }
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!unlayerRef.current) {
      alert("Editor yüklenmedi!");
      return;
    }

    let finalHtmlContent = "";
    let designJson = null;

    await new Promise<void>((resolve) => {
      unlayerRef.current.exportHtml((data: any) => {
        finalHtmlContent = data.html;

        unlayerRef.current.saveDesign((design: any) => {
          designJson = design;
          resolve();
        });
      });
    });

    await fetch("https://searchprojectdemo.com/api/campains/create/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        html_content: finalHtmlContent,
        design_json: designJson,
        is_template: true,
      }),
    });

    alert("Şablon başarıyla kaydedildi!");
  };

  return (
    <div className="p-6 flex flex-col h-screen">
      <h1 className="text-2xl font-bold mb-4">Yeni Şablon Oluştur</h1>

      <form onSubmit={handleSubmit} className="flex flex-col flex-1 overflow-hidden">
        <input
          name="title"
          placeholder="Şablon Adı"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="border border-pink-300 p-2 rounded w-full mb-4"
          required
        />

        <div
          ref={editorRef}
          className="flex-1 overflow-hidden border border-pink-300 rounded"
          style={{
            minHeight: "500px",
          }}
        ></div>

        <button
          type="submit"
          className="bg-pink-500 text-white px-4 py-2 rounded self-start mt-4"
        >
          Kaydet
        </button>
      </form>
    </div>
  );
}
