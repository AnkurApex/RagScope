"use client";

import { useState } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { UploadCloud, CheckCircle2, FileText } from "lucide-react";

export default function IngestPage() {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [result, setResult] = useState<{ docId: string; chunks: number } | null>(null);

  const handleUpload = async () => {
    if (!file) return;
    setIsUploading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:8000/api/ingest/", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setResult({ docId: res.data.document_id, chunks: res.data.chunks_indexed });
    } catch (e) {
      console.error(e);
      alert("Failed to upload document.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="p-8 max-w-3xl mx-auto w-full">
      <h1 className="text-3xl font-bold text-white mb-8">Document Ingestion Pipeline</h1>
      
      <Card className="bg-neutral-900 border-neutral-800">
        <CardHeader>
          <CardTitle className="text-white flex items-center gap-2">
            <UploadCloud className="text-blue-400" />
            Upload Knowledge Base
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="border-2 border-dashed border-neutral-700 rounded-xl p-10 flex flex-col items-center justify-center text-center hover:bg-neutral-800/50 transition-colors">
            <input 
              type="file" 
              id="file-upload" 
              className="hidden" 
              accept=".txt,.pdf"
              onChange={(e) => e.target.files && setFile(e.target.files[0])}
            />
            <label htmlFor="file-upload" className="cursor-pointer flex flex-col items-center">
              <FileText className="w-12 h-12 text-neutral-500 mb-4" />
              <span className="text-lg font-medium text-white mb-2">
                {file ? file.name : "Click to select a document"}
              </span>
              <span className="text-sm text-neutral-500">Supports PDF, TXT (Max 10MB)</span>
            </label>
          </div>
          
          <Button 
            onClick={handleUpload} 
            disabled={!file || isUploading} 
            className="w-full bg-blue-600 hover:bg-blue-700"
            size="lg"
          >
            {isUploading ? "Processing Document & Generating Embeddings..." : "Ingest Document"}
          </Button>

          {result && (
            <div className="mt-4 p-4 bg-green-950/30 border border-green-900 rounded-lg flex items-center gap-3">
              <CheckCircle2 className="text-green-500 w-6 h-6" />
              <div>
                <p className="text-green-400 font-medium">Ingestion Complete!</p>
                <p className="text-neutral-400 text-sm">Indexed {result.chunks} chunks into ChromaDB.</p>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
