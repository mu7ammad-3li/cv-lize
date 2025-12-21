import { useState } from "react";
import {
  CheckCircle,
  XCircle,
  Lightbulb,
  Download,
  FileText,
  Eye,
  List,
} from "lucide-react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "./ui/Card";
import { Button } from "./ui/Button";
import {
  analyzeCV,
  type AnalyzeResponse,
  downloadMarkdown,
  downloadPDF,
} from "@/lib/api";
import ReactMarkdown from "react-markdown";
import { ProfessionalResumeDisplay } from "./ProfessionalResumeDisplay";
import { StructuredCVDisplay } from "./StructuredCVDisplay";

interface CVAnalysisProps {
  sessionId: string;
  filename: string;
}

export function CVAnalysis({ sessionId, filename }: CVAnalysisProps) {
  const [jobDescription, setJobDescription] = useState("");
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<
    "structured" | "markdown" | "professional"
  >("structured");

  const handleAnalyze = async () => {
    if (!jobDescription.trim()) {
      setError("Please enter a job description");
      return;
    }

    setAnalyzing(true);
    setError(null);

    try {
      const response = await analyzeCV(sessionId, jobDescription);
      setResult(response);
    } catch (err: any) {
      console.error("Analysis error:", err);
      setError(
        err.response?.data?.detail || "Failed to analyze CV. Please try again.",
      );
    } finally {
      setAnalyzing(false);
    }
  };

  const handleDownloadMarkdown = async () => {
    try {
      const blob = await downloadMarkdown(sessionId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${filename.replace(/\.[^/.]+$/, "")}_optimized.md`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error("Download error:", err);
      alert("Failed to download optimized CV as Markdown");
    }
  };

  const handleDownloadPDF = async () => {
    try {
      const blob = await downloadPDF(sessionId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${filename.replace(/\.[^/.]+$/, "")}_optimized.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error("Download PDF error:", err);
      alert("Failed to download optimized CV as PDF");
    }
  };

  return (
    <div className="w-full max-w-6xl mx-auto space-y-6">
      {/* Job Description Input */}
      {!result && (
        <Card>
          <CardHeader>
            <CardTitle>Analyze Against Job Description</CardTitle>
            <CardDescription>
              Paste the job description to get AI-powered CV optimization
              suggestions
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">
                Job Description
              </label>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the full job description here..."
                className="w-full min-h-[200px] p-3 border rounded-lg resize-y focus:outline-none focus:ring-2 focus:ring-primary"
                disabled={analyzing}
              />
            </div>

            {error && (
              <div className="p-3 bg-destructive/10 border border-destructive/20 rounded-lg text-sm text-destructive">
                {error}
              </div>
            )}

            <Button
              onClick={handleAnalyze}
              disabled={analyzing || !jobDescription.trim()}
              className="w-full"
              size="lg"
            >
              {analyzing ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Analyzing with AI...
                </>
              ) : (
                "Analyze CV"
              )}
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Analysis Results */}
      {result && (
        <div className="space-y-6">
          {/* Score Summary */}
          <Card>
            <CardHeader>
              <CardTitle>Analysis Results</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-4xl font-bold text-primary mb-2">
                    {result.analysis.score}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    Overall Score
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-4xl font-bold text-green-600 mb-2">
                    {result.analysis.ats_compatibility}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    ATS Compatible
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-4xl font-bold text-blue-600 mb-2">
                    {result.analysis.match_percentage}%
                  </div>
                  <div className="text-sm text-muted-foreground">Job Match</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Strengths */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle className="h-5 w-5 text-green-600" />
                Strengths
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {result.analysis.strengths.map((strength, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                    <span className="text-sm">{strength}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          {/* Weaknesses */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <XCircle className="h-5 w-5 text-yellow-600" />
                Areas for Improvement
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {result.analysis.weaknesses.map((weakness, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <XCircle className="h-4 w-4 text-yellow-600 mt-0.5 flex-shrink-0" />
                    <span className="text-sm">{weakness}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          {/* Suggestions */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Lightbulb className="h-5 w-5 text-blue-600" />
                Actionable Suggestions
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {result.analysis.suggestions.map((suggestion, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <Lightbulb className="h-4 w-4 text-blue-600 mt-0.5 flex-shrink-0" />
                    <span className="text-sm">{suggestion}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          {/* Optimized CV Preview */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Optimized CV</CardTitle>
                  <CardDescription>
                    AI-generated resume optimized for this job description
                  </CardDescription>
                </div>
                <div className="flex gap-2">
                  <Button
                    variant={viewMode === "structured" ? "default" : "outline"}
                    size="sm"
                    onClick={() => setViewMode("structured")}
                  >
                    <List className="h-4 w-4 mr-2" />
                    Structured View
                  </Button>
                  <Button
                    variant={
                      viewMode === "professional" ? "default" : "outline"
                    }
                    size="sm"
                    onClick={() => setViewMode("professional")}
                  >
                    <Eye className="h-4 w-4 mr-2" />
                    Professional View
                  </Button>
                  <Button
                    variant={viewMode === "markdown" ? "default" : "outline"}
                    size="sm"
                    onClick={() => setViewMode("markdown")}
                  >
                    <FileText className="h-4 w-4 mr-2" />
                    Markdown View
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              {viewMode === "structured" ? (
                <div>
                  {result.optimized_cv.sections ? (
                    <StructuredCVDisplay
                      sections={result.optimized_cv.sections}
                    />
                  ) : (
                    <div className="p-6 text-center text-muted-foreground bg-secondary/30 rounded-lg border">
                      <p>Structured sections are not available.</p>
                      <p className="text-sm mt-2">
                        Please use Markdown or Professional view instead.
                      </p>
                    </div>
                  )}
                </div>
              ) : viewMode === "professional" ? (
                <div className="bg-white rounded-lg border">
                  {result.parsed_resume ? (
                    <ProfessionalResumeDisplay
                      data={result.parsed_resume}
                      sections={result.optimized_cv.sections}
                      onDownload={handleDownloadPDF}
                    />
                  ) : (
                    <div className="p-6 text-center text-muted-foreground">
                      <p>Unable to parse resume for professional view.</p>
                      <p className="text-sm mt-2">
                        Please use Markdown view instead.
                      </p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="prose prose-sm max-w-none bg-secondary/30 p-6 rounded-lg border">
                  <ReactMarkdown>{result.optimized_cv.markdown}</ReactMarkdown>
                </div>
              )}

              <div className="mt-6 flex gap-3">
                <Button onClick={handleDownloadPDF} className="flex-1">
                  <Download className="h-4 w-4 mr-2" />
                  Download as PDF
                </Button>
                <Button
                  variant="outline"
                  className="flex-1"
                  onClick={handleDownloadMarkdown}
                >
                  <FileText className="h-4 w-4 mr-2" />
                  Download as Markdown
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
