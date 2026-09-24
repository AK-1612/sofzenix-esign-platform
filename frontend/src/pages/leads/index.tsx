import { useCallback, useEffect, useRef, useState } from "react";
import {
  CallResult,
  Lead,
  leadCallingService,
} from "@/services/leadCallingService";

const STATUS_STYLES: Record<string, string> = {
  "Not Called": "bg-slate-100 text-slate-600",
  Calling: "bg-blue-100 text-blue-700",
  Connected: "bg-cyan-100 text-cyan-700",
  "No Answer": "bg-amber-100 text-amber-700",
  Busy: "bg-amber-100 text-amber-700",
  Failed: "bg-red-100 text-red-700",
  Interested: "bg-green-100 text-green-700",
  "Not Interested": "bg-red-100 text-red-700",
  "Follow-up": "bg-purple-100 text-purple-700",
  Appointment: "bg-indigo-100 text-indigo-700",
  Converted: "bg-emerald-100 text-emerald-800",
};

function StatusBadge({ status }: { status: string }) {
  const style = STATUS_STYLES[status] || "bg-slate-100 text-slate-600";
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${style}`}>
      {status}
    </span>
  );
}

function formatDuration(seconds: number): string {
  const m = Math.floor(seconds / 60)
    .toString()
    .padStart(2, "0");
  const s = Math.floor(seconds % 60)
    .toString()
    .padStart(2, "0");
  return `${m}:${s}`;
}

export default function LeadsDashboardPage() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [results, setResults] = useState<CallResult[]>([]);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);
  const [callingIds, setCallingIds] = useState<Set<string>>(new Set());
  const fileInputRef = useRef<HTMLInputElement>(null);

  const refresh = useCallback(async () => {
    const [leadRows, resultRows] = await Promise.all([
      leadCallingService.listLeads(),
      leadCallingService.listResults(),
    ]);
    setLeads(leadRows);
    setResults(resultRows);
  }, []);

  useEffect(() => {
    refresh().catch((err) => console.error(err));
    // Light polling so "Calling" rows flip to their final status automatically.
    const interval = setInterval(() => refresh().catch(() => {}), 5000);
    return () => clearInterval(interval);
  }, [refresh]);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setUploadMessage(null);
    try {
      const summary = await leadCallingService.uploadLeads(file);
      setUploadMessage(
        `Imported ${summary.imported} of ${summary.total_rows} rows` +
          (summary.errors.length ? ` (${summary.errors.length} errors)` : "")
      );
      await refresh();
    } catch (err) {
      setUploadMessage(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  const handleCall = async (leadId: string) => {
    setCallingIds((prev) => new Set(prev).add(leadId));
    try {
      await leadCallingService.startCall(leadId);
      await refresh();
    } finally {
      setCallingIds((prev) => {
        const next = new Set(prev);
        next.delete(leadId);
        return next;
      });
    }
  };

  const resultByLeadId = new Map(results.map((r) => [r.lead_id, r]));

  return (
    <main className="min-h-screen bg-slate-50 p-6 md:p-10">
      <div className="max-w-6xl mx-auto space-y-6">
        <header className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-semibold text-slate-900">
              AI Call Automation — Leads
            </h1>
            <p className="text-slate-500 text-sm mt-1">
              Upload an Excel sheet of leads, let the AI agent call them with a
              personalised script, and see results saved here automatically.
            </p>
          </div>
          <div className="flex gap-3">
            <label className="cursor-pointer inline-flex items-center gap-2 bg-slate-900 text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-slate-800 transition">
              {uploading ? "Uploading…" : "Upload Excel"}
              <input
                ref={fileInputRef}
                type="file"
                accept=".xlsx,.xlsm"
                className="hidden"
                onChange={handleFileChange}
                disabled={uploading}
              />
            </label>
            <a
              href={leadCallingService.exportResultsUrl()}
              className="inline-flex items-center gap-2 border border-slate-300 text-slate-700 text-sm font-medium px-4 py-2 rounded-lg hover:bg-slate-100 transition"
            >
              Export Results
            </a>
          </div>
        </header>

        {uploadMessage && (
          <div className="text-sm text-slate-600 bg-white border border-slate-200 rounded-lg px-4 py-2">
            {uploadMessage}
          </div>
        )}

        <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-slate-50 text-slate-500 text-left">
              <tr>
                <th className="px-4 py-3 font-medium">Name</th>
                <th className="px-4 py-3 font-medium">Mobile</th>
                <th className="px-4 py-3 font-medium">Service</th>
                <th className="px-4 py-3 font-medium">Call Status</th>
                <th className="px-4 py-3 font-medium">Duration</th>
                <th className="px-4 py-3 font-medium">Interest</th>
                <th className="px-4 py-3 font-medium">Score</th>
                <th className="px-4 py-3 font-medium">Next Action</th>
                <th className="px-4 py-3 font-medium"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {leads.length === 0 && (
                <tr>
                  <td colSpan={9} className="px-4 py-10 text-center text-slate-400">
                    No leads yet — upload an Excel file to get started.
                  </td>
                </tr>
              )}
              {leads.map((lead) => {
                const result = resultByLeadId.get(lead.id);
                const isCalling =
                  callingIds.has(lead.id) || result?.call_status === "Calling";
                return (
                  <tr key={lead.id} className="hover:bg-slate-50">
                    <td className="px-4 py-3 font-medium text-slate-900">
                      {lead.name}
                    </td>
                    <td className="px-4 py-3 text-slate-600">{lead.mobile}</td>
                    <td className="px-4 py-3 text-slate-600">
                      {lead.service || "—"}
                    </td>
                    <td className="px-4 py-3">
                      <StatusBadge status={result?.call_status || "Not Called"} />
                    </td>
                    <td className="px-4 py-3 text-slate-600">
                      {result ? formatDuration(result.duration_seconds) : "00:00"}
                    </td>
                    <td className="px-4 py-3 text-slate-600">
                      {result?.interest ?? "—"}
                    </td>
                    <td className="px-4 py-3 text-slate-600">
                      {result?.score ?? "—"}
                    </td>
                    <td className="px-4 py-3 text-slate-600">
                      {result?.next_action ?? "Call Lead"}
                    </td>
                    <td className="px-4 py-3 text-right">
                      <button
                        onClick={() => handleCall(lead.id)}
                        disabled={isCalling}
                        className="text-xs font-medium px-3 py-1.5 rounded-lg border border-slate-300 hover:bg-slate-100 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {isCalling ? "Calling…" : "Call Now"}
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}
