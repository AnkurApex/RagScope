import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { ArrowRight, Database, LineChart, ShieldCheck } from "lucide-react";

export default function Home() {
  return (
    <div className="flex-1 overflow-y-auto p-8">
      <div className="max-w-5xl mx-auto space-y-12 mt-10">
        <div className="text-center space-y-4">
          <h1 className="text-5xl font-extrabold tracking-tight text-white">
            Welcome to <span className="text-blue-500">RAGScope</span>
          </h1>
          <p className="text-xl text-neutral-400 max-w-2xl mx-auto">
            A production-grade Retrieval-Augmented Generation platform built with observability, 
            telemetry, and evaluation at its core.
          </p>
          <div className="pt-6 flex justify-center space-x-4">
            <Link href="/chat">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
                Start Chatting <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
            </Link>
            <Link href="/dashboard">
              <Button size="lg" variant="outline" className="border-neutral-700 text-neutral-800 hover:bg-neutral-800">
                View Telemetry
              </Button>
            </Link>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-6 pt-12">
          <Card className="bg-neutral-900 border-neutral-800">
            <CardHeader>
              <Database className="w-8 h-8 text-blue-400 mb-2" />
              <CardTitle className="text-white">Robust Ingestion</CardTitle>
              <CardDescription className="text-neutral-400">
                Upload PDFs and text documents. Automatically chunk, embed, and store in ChromaDB for high-performance semantic search.
              </CardDescription>
            </CardHeader>
          </Card>
          <Card className="bg-neutral-900 border-neutral-800">
            <CardHeader>
              <LineChart className="w-8 h-8 text-green-400 mb-2" />
              <CardTitle className="text-white">Full Observability</CardTitle>
              <CardDescription className="text-neutral-400">
                Track every token, measure latency, monitor retrieval accuracy, and visualize metrics on a comprehensive dashboard.
              </CardDescription>
            </CardHeader>
          </Card>
          <Card className="bg-neutral-900 border-neutral-800">
            <CardHeader>
              <ShieldCheck className="w-8 h-8 text-purple-400 mb-2" />
              <CardTitle className="text-white">Hallucination Detection</CardTitle>
              <CardDescription className="text-neutral-400">
                Built-in guardrails and evaluation pipelines (Ragas/DeepEval) to ensure the AI remains faithful to the context.
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </div>
    </div>
  );
}
