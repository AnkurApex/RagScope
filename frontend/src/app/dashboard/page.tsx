"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Activity, Clock, FileText, AlertTriangle, ThumbsUp, ThumbsDown } from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function DashboardPage() {
  const [metrics, setMetrics] = useState<any>(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/analytics/metrics").then((res) => {
      setMetrics(res.data);
    });
  }, []);

  if (!metrics) return <div className="p-8 text-neutral-400">Loading metrics...</div>;

  const mockChartData = [
    { name: "Mon", queries: 12 },
    { name: "Tue", queries: 19 },
    { name: "Wed", queries: 15 },
    { name: "Thu", queries: metrics.total_queries || 22 },
  ];

  return (
    <div className="p-8 overflow-y-auto w-full">
      <h1 className="text-3xl font-bold text-white mb-8">Telemetry & Observability</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <MetricCard title="Total Queries" value={metrics.total_queries} icon={<Activity />} color="text-blue-400" />
        <MetricCard title="Avg Latency" value={`${metrics.avg_latency_ms} ms`} icon={<Clock />} color="text-yellow-400" />
        <MetricCard title="Documents" value={metrics.total_documents} icon={<FileText />} color="text-green-400" />
        <MetricCard title="Hallucination Rate" value={`${(metrics.hallucination_rate * 100).toFixed(1)}%`} icon={<AlertTriangle />} color="text-red-400" />
      </div>

      <div className="grid lg:grid-cols-2 gap-8 mb-8">
        <Card className="bg-neutral-900 border-neutral-800">
          <CardHeader>
            <CardTitle className="text-white">Query Volume (Weekly)</CardTitle>
          </CardHeader>
          <CardContent className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={mockChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="name" stroke="#888" />
                <YAxis stroke="#888" />
                <Tooltip contentStyle={{ backgroundColor: "#171717", border: "1px solid #333" }} />
                <Line type="monotone" dataKey="queries" stroke="#3b82f6" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="bg-neutral-900 border-neutral-800">
          <CardHeader>
            <CardTitle className="text-white">User Feedback</CardTitle>
          </CardHeader>
          <CardContent className="flex items-center justify-around h-72">
            <div className="text-center">
              <ThumbsUp className="w-16 h-16 text-green-500 mx-auto mb-4" />
              <p className="text-4xl font-bold text-white">{metrics.positive_feedback}</p>
              <p className="text-neutral-400">Positive</p>
            </div>
            <div className="text-center">
              <ThumbsDown className="w-16 h-16 text-red-500 mx-auto mb-4" />
              <p className="text-4xl font-bold text-white">{metrics.negative_feedback}</p>
              <p className="text-neutral-400">Negative</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function MetricCard({ title, value, icon, color }: { title: string, value: string | number, icon: React.ReactNode, color: string }) {
  return (
    <Card className="bg-neutral-900 border-neutral-800">
      <CardContent className="p-6 flex items-center gap-4">
        <div className={`p-3 rounded-lg bg-neutral-800 ${color}`}>
          {icon}
        </div>
        <div>
          <p className="text-sm text-neutral-400">{title}</p>
          <p className="text-2xl font-bold text-white">{value}</p>
        </div>
      </CardContent>
    </Card>
  );
}
