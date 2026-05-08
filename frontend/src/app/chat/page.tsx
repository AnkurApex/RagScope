"use client";

import { useState } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Send, ThumbsUp, ThumbsDown, Bot, User } from "lucide-react";

export default function ChatPage() {
  const [messages, setMessages] = useState<{ role: string; content: string; telemetryId?: number }[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = input.trim();
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/api/chat/", { query: userMsg });
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: res.data.answer, telemetryId: res.data.telemetry_id }
      ]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, I encountered an error. Please try again." }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const submitFeedback = async (telemetryId: number, score: number) => {
    try {
      await axios.post("http://127.0.0.1:8000/api/feedback/", { telemetry_id: telemetryId, score });
      alert("Feedback submitted!");
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="flex flex-col h-full bg-neutral-950 p-4">
      <div className="flex-1 max-w-4xl w-full mx-auto bg-neutral-900 rounded-xl border border-neutral-800 flex flex-col overflow-hidden">
        <div className="p-4 border-b border-neutral-800 bg-neutral-900 flex justify-between items-center">
          <h2 className="text-lg font-semibold text-white">RAG Chat</h2>
          <span className="text-xs px-2 py-1 bg-blue-900 text-blue-300 rounded-full">Strict Grounding Active</span>
        </div>
        
        <ScrollArea className="flex-1 p-4">
          <div className="space-y-4">
            {messages.length === 0 && (
              <div className="text-center text-neutral-500 mt-20">
                Ask a question based on the ingested documents.
              </div>
            )}
            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                <div className={`max-w-[80%] rounded-2xl p-4 flex gap-3 ${msg.role === "user" ? "bg-blue-600 text-white" : "bg-neutral-800 text-neutral-200 border border-neutral-700"}`}>
                  <div className="mt-1">
                    {msg.role === "user" ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5 text-blue-400" />}
                  </div>
                  <div className="flex-1">
                    <p className="whitespace-pre-wrap">{msg.content}</p>
                    {msg.role === "assistant" && msg.telemetryId && (
                      <div className="flex gap-2 mt-3 pt-3 border-t border-neutral-700">
                        <button onClick={() => submitFeedback(msg.telemetryId!, 1)} className="text-neutral-400 hover:text-green-400">
                          <ThumbsUp className="w-4 h-4" />
                        </button>
                        <button onClick={() => submitFeedback(msg.telemetryId!, -1)} className="text-neutral-400 hover:text-red-400">
                          <ThumbsDown className="w-4 h-4" />
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-neutral-800 text-neutral-200 border border-neutral-700 rounded-2xl p-4 flex gap-3 items-center">
                  <Bot className="w-5 h-5 text-blue-400 animate-pulse" />
                  <span className="animate-pulse">Retrieving context & generating answer...</span>
                </div>
              </div>
            )}
          </div>
        </ScrollArea>

        <div className="p-4 bg-neutral-900 border-t border-neutral-800">
          <form 
            onSubmit={(e) => { e.preventDefault(); sendMessage(); }}
            className="flex gap-2"
          >
            <Input 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything..."
              className="flex-1 bg-neutral-950 border-neutral-800 text-white"
            />
            <Button type="submit" disabled={isLoading} className="bg-blue-600 hover:bg-blue-700">
              <Send className="w-4 h-4" />
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
