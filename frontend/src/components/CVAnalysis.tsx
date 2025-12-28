import { useState, useMemo } from "react";
import {
  CheckCircle,
  XCircle,
  Lightbulb,
  Download,
  FileText,
  Eye,
  List,
  ChevronDown,
  ChevronUp,
  Plus,
  Minus,
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
  type SectionRecommendation,
  downloadMarkdown,
  downloadPDF,
  downloadDOCX,
} from "@/lib/api";
import ReactMarkdown from "react-markdown";
import { ProfessionalResumeDisplay } from "./ProfessionalResumeDisplay";

interface CVAnalysisProps {
  sessionId: string;
  filename: string;
}

interface ParsedSection {
  title: string;
  content: string;
  rawContent: string[];
}

export function CVAnalysis({ sessionId, filename }: CVAnalysisProps) {
  const [jobDescription, setJobDescription] = useState("");
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<"recommendations" | "preview">(
    "recommendations",
  );
  const [expandedSections, setExpandedSections] = useState<Set<string>>(
    new Set(),
  );
  const [includedSections, setIncludedSections] = useState<Set<string>>(
    new Set(),
  );
  const [downloading, setDownloading] = useState(false);
  const [selectedFont, setSelectedFont] = useState<string>("Arial");

  // Available ATS-safe fonts
  const availableFonts = [
    { value: "Arial", label: "Arial (Sans-Serif)", category: "sans-serif" },
    { value: "Calibri", label: "Calibri (Sans-Serif)", category: "sans-serif" },
    {
      value: "Helvetica",
      label: "Helvetica (Sans-Serif)",
      category: "sans-serif",
    },
    {
      value: "Times New Roman",
      label: "Times New Roman (Serif)",
      category: "serif",
    },
    { value: "Georgia", label: "Georgia (Serif)", category: "serif" },
    { value: "Garamond", label: "Garamond (Serif)", category: "serif" },
  ];

  // Parse sections from markdown
  const parseSectionsFromMarkdown = (markdown: string): ParsedSection[] => {
    const lines = markdown.split("\n");
    const sections: ParsedSection[] = [];
    let currentSection: ParsedSection | null = null;
    let currentContent: string[] = [];

    for (const line of lines) {
      // Check for section headers (## Section Name)
      const sectionMatch = line.match(/^##\s+(.+)$/);

      if (sectionMatch) {
        // Save previous section if exists
        if (currentSection) {
          currentSection.rawContent = [...currentContent];
          currentSection.content = currentContent.join("\n").trim();
          sections.push(currentSection);
        }

        // Start new section
        const title = sectionMatch[1].trim();
        currentSection = {
          title,
          content: "",
          rawContent: [],
        };
        currentContent = [];
      } else if (currentSection && line.trim()) {
        // Add content to current section (skip empty lines at start)
        if (currentContent.length > 0 || line.trim()) {
          currentContent.push(line);
        }
      }
    }

    // Save last section
    if (currentSection) {
      currentSection.rawContent = [...currentContent];
      currentSection.content = currentContent.join("\n").trim();
      sections.push(currentSection);
    }

    return sections;
  };

  // Memoize parsed sections
  const parsedSections = useMemo(() => {
    if (!result?.optimized_cv.markdown) return [];
    return parseSectionsFromMarkdown(result.optimized_cv.markdown);
  }, [result?.optimized_cv.markdown]);

  // Get recommendations for a specific section
  const getRecommendationsForSection = (sectionTitle: string): string[] => {
    if (!result?.analysis.section_recommendations) return [];

    const matchingRec = result.analysis.section_recommendations.find(
      (rec) =>
        rec.section.toLowerCase().includes(sectionTitle.toLowerCase()) ||
        sectionTitle.toLowerCase().includes(rec.section.toLowerCase()),
    );

    return matchingRec?.recommendations || [];
  };

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

      // Parse sections will happen automatically via useMemo
      // Initialize all sections as included by default
      setTimeout(() => {
        const sections = parseSectionsFromMarkdown(
          response.optimized_cv.markdown,
        );
        const allSectionTitles = new Set(sections.map((s) => s.title));
        setIncludedSections(allSectionTitles);
      }, 100);
    } catch (err: any) {
      console.error("Analysis error:", err);
      setError(
        err.response?.data?.detail || "Failed to analyze CV. Please try again.",
      );
    } finally {
      setAnalyzing(false);
    }
  };

  const toggleSection = (section: string) => {
    setExpandedSections((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(section)) {
        newSet.delete(section);
      } else {
        newSet.add(section);
      }
      return newSet;
    });
  };

  const toggleIncludeSection = (section: string) => {
    setIncludedSections((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(section)) {
        newSet.delete(section);
      } else {
        newSet.add(section);
      }
      return newSet;
    });
  };

  const handleDownload = async (format: "markdown" | "pdf" | "docx") => {
    setDownloading(true);
    try {
      const sectionsArray = Array.from(includedSections);
      let blob: Blob;
      let filename_suffix: string;
      let extension: string;

      switch (format) {
        case "markdown":
          blob = await downloadMarkdown(sessionId, sectionsArray, selectedFont);
          filename_suffix = "_optimized";
          extension = "md";
          break;
        case "pdf":
          blob = await downloadPDF(sessionId, sectionsArray, selectedFont);
          filename_suffix = "_optimized";
          extension = "pdf";
          break;
        case "docx":
          blob = await downloadDOCX(sessionId, sectionsArray, selectedFont);
          filename_suffix = "_ATS_optimized";
          extension = "docx";
          break;
      }

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `${filename.replace(/\.[^/.]+$/, "")}${filename_suffix}.${extension}`;
      document.body.appendChild(link);
      link.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(link);
    } catch (err) {
      console.error(`Download ${format} error:`, err);
      alert(`Failed to download ${format.toUpperCase()}. Please try again.`);
    } finally {
      setDownloading(false);
    }
  };

  const handleDownloadAll = async () => {
    setDownloading(true);
    try {
      const sectionsArray = Array.from(includedSections);

      // Download Markdown
      const mdBlob = await downloadMarkdown(
        sessionId,
        sectionsArray,
        selectedFont,
      );
      const mdUrl = window.URL.createObjectURL(mdBlob);
      const mdLink = document.createElement("a");
      mdLink.href = mdUrl;
      mdLink.download = `${filename.replace(/\.[^/.]+$/, "")}_optimized.md`;
      document.body.appendChild(mdLink);
      mdLink.click();
      window.URL.revokeObjectURL(mdUrl);
      document.body.removeChild(mdLink);

      await new Promise((resolve) => setTimeout(resolve, 500));

      // Download PDF
      const pdfBlob = await downloadPDF(sessionId, sectionsArray, selectedFont);
      const pdfUrl = window.URL.createObjectURL(pdfBlob);
      const pdfLink = document.createElement("a");
      pdfLink.href = pdfUrl;
      pdfLink.download = `${filename.replace(/\.[^/.]+$/, "")}_optimized.pdf`;
      document.body.appendChild(pdfLink);
      pdfLink.click();
      window.URL.revokeObjectURL(pdfUrl);
      document.body.removeChild(pdfLink);

      await new Promise((resolve) => setTimeout(resolve, 500));

      // Download DOCX
      const docxBlob = await downloadDOCX(
        sessionId,
        sectionsArray,
        selectedFont,
      );
      const docxUrl = window.URL.createObjectURL(docxBlob);
      const docxLink = document.createElement("a");
      docxLink.href = docxUrl;
      docxLink.download = `${filename.replace(/\.[^/.]+$/, "")}_ATS_optimized.docx`;
      document.body.appendChild(docxLink);
      docxLink.click();
      window.URL.revokeObjectURL(docxUrl);
      document.body.removeChild(docxLink);
    } catch (err) {
      console.error("Download error:", err);
      alert("Failed to download some files. Please try again.");
    } finally {
      setDownloading(false);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case "critical":
      case "high":
        return "text-red-600 bg-red-50 border-red-200";
      case "medium":
        return "text-yellow-600 bg-yellow-50 border-yellow-200";
      case "low":
        return "text-blue-600 bg-blue-50 border-blue-200";
      default:
        return "text-gray-600 bg-gray-50 border-gray-200";
    }
  };

  const getFilteredMarkdown = (): string => {
    if (!result || !result.optimized_cv.markdown) return "";

    const markdown = result.optimized_cv.markdown;
    const lines = markdown.split("\n");
    const filteredLines: string[] = [];
    let currentSection = "";
    let includeCurrentSection = true;
    let inHeader = true;

    for (const line of lines) {
      // Check for section headers (## Section Name)
      const sectionMatch = line.match(/^##\s+(.+)$/);

      if (sectionMatch) {
        inHeader = false;
        const sectionName = sectionMatch[1].trim();
        currentSection = sectionName;

        // Check if this section is included
        includeCurrentSection = Array.from(includedSections).some(
          (included) =>
            included.toLowerCase().includes(sectionName.toLowerCase()) ||
            sectionName.toLowerCase().includes(included.toLowerCase()),
        );

        if (includeCurrentSection) {
          filteredLines.push(line);
        }
      } else if (inHeader) {
        // Always include header (name, contact info)
        filteredLines.push(line);
      } else if (includeCurrentSection) {
        // Include content of included sections
        filteredLines.push(line);
      }
    }

    return filteredLines.join("\n");
  };

  return (
    <div className="w-full max-w-7xl mx-auto space-y-6">
      {/* Job Description Input */}
      <Card>
        <CardHeader>
          <CardTitle>Analyze CV Against Job Description</CardTitle>
          <CardDescription>
            Enter the job description to get AI-powered analysis and
            optimization
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Job Description *
            </label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              className="w-full min-h-[200px] p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent resize-y"
              placeholder="Paste the job description here..."
              disabled={analyzing}
            />
          </div>

          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}

          <Button
            onClick={handleAnalyze}
            disabled={analyzing || !jobDescription.trim()}
            className="w-full"
          >
            {analyzing ? (
              <>
                <span className="animate-spin mr-2">⏳</span>
                Analyzing CV...
              </>
            ) : (
              <>
                <Lightbulb className="w-4 h-4 mr-2" />
                Analyze CV
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Analysis Results */}
      {result && (
        <>
          {/* Score Overview */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-4xl font-bold text-primary mb-2">
                    {result.analysis.score}/100
                  </div>
                  <div className="text-sm text-gray-600">Overall Score</div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-4xl font-bold text-green-600 mb-2">
                    {result.analysis.ats_compatibility}/100
                  </div>
                  <div className="text-sm text-gray-600">ATS Compatibility</div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-4xl font-bold text-blue-600 mb-2">
                    {result.analysis.match_percentage}%
                  </div>
                  <div className="text-sm text-gray-600">Match Percentage</div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* View Mode Toggle */}
          <div className="flex gap-2 border-b border-gray-200">
            <button
              onClick={() => setViewMode("recommendations")}
              className={`px-4 py-2 font-medium border-b-2 transition-colors ${
                viewMode === "recommendations"
                  ? "border-primary text-primary"
                  : "border-transparent text-gray-600 hover:text-gray-900"
              }`}
            >
              <List className="w-4 h-4 inline mr-2" />
              Recommendations by Section
            </button>
            <button
              onClick={() => setViewMode("preview")}
              className={`px-4 py-2 font-medium border-b-2 transition-colors ${
                viewMode === "preview"
                  ? "border-primary text-primary"
                  : "border-transparent text-gray-600 hover:text-gray-900"
              }`}
            >
              <Eye className="w-4 h-4 inline mr-2" />
              Optimized Resume Preview
            </button>
          </div>

          {/* Recommendations View */}
          {viewMode === "recommendations" && (
            <div className="space-y-6">
              {/* General Insights */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2">
                      <CheckCircle className="w-5 h-5 text-green-600" />
                      Strengths
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {result.analysis.strengths.map((strength, idx) => (
                        <li
                          key={idx}
                          className="flex items-start gap-2 text-sm"
                        >
                          <span className="text-green-600 mt-1">✓</span>
                          <span>{strength}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2">
                      <XCircle className="w-5 h-5 text-red-600" />
                      Areas to Improve
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {result.analysis.weaknesses.map((weakness, idx) => (
                        <li
                          key={idx}
                          className="flex items-start gap-2 text-sm"
                        >
                          <span className="text-red-600 mt-1">!</span>
                          <span>{weakness}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              </div>

              {/* Section-Specific Recommendations - Parsed from Resume */}
              {parsedSections.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <List className="w-5 h-5 text-blue-600" />
                      Resume Sections
                    </CardTitle>
                    <CardDescription>
                      Review each section from your resume. Toggle sections
                      on/off to customize your final output.
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {parsedSections.map((section, idx) => {
                      const recommendations = getRecommendationsForSection(
                        section.title,
                      );
                      const hasRecommendations = recommendations.length > 0;

                      return (
                        <div
                          key={idx}
                          className={`border rounded-lg overflow-hidden ${
                            hasRecommendations
                              ? "bg-yellow-50 border-yellow-200"
                              : "bg-gray-50 border-gray-200"
                          }`}
                        >
                          <div className="flex items-center justify-between p-4">
                            <div className="flex items-center gap-3 flex-1">
                              <button
                                onClick={() => toggleSection(section.title)}
                                className="hover:bg-white/50 rounded p-1 transition-colors"
                              >
                                {expandedSections.has(section.title) ? (
                                  <ChevronUp className="w-5 h-5" />
                                ) : (
                                  <ChevronDown className="w-5 h-5" />
                                )}
                              </button>
                              <div className="flex-1">
                                <h4 className="font-semibold text-gray-900">
                                  {section.title}
                                </h4>
                                {hasRecommendations && (
                                  <p className="text-xs text-yellow-700">
                                    {recommendations.length} recommendation
                                    {recommendations.length > 1 ? "s" : ""}{" "}
                                    available
                                  </p>
                                )}
                              </div>
                            </div>
                            <button
                              onClick={() =>
                                toggleIncludeSection(section.title)
                              }
                              className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                                includedSections.has(section.title)
                                  ? "bg-green-600 text-white hover:bg-green-700"
                                  : "bg-gray-400 text-white hover:bg-gray-500"
                              }`}
                            >
                              {includedSections.has(section.title) ? (
                                <>
                                  <Minus className="w-4 h-4 inline mr-1" />
                                  Included
                                </>
                              ) : (
                                <>
                                  <Plus className="w-4 h-4 inline mr-1" />
                                  Add Section
                                </>
                              )}
                            </button>
                          </div>

                          {expandedSections.has(section.title) && (
                            <div className="px-4 pb-4 pt-2 bg-white border-t">
                              {/* Section Content */}
                              <div className="mb-4">
                                <h5 className="text-sm font-semibold text-gray-700 mb-2">
                                  Section Content:
                                </h5>
                                <div className="prose prose-sm max-w-none text-gray-600 bg-gray-50 p-3 rounded border border-gray-200">
                                  <ReactMarkdown>
                                    {section.content}
                                  </ReactMarkdown>
                                </div>
                              </div>

                              {/* Recommendations if available */}
                              {hasRecommendations && (
                                <div>
                                  <h5 className="text-sm font-semibold text-yellow-700 mb-2 flex items-center gap-2">
                                    <Lightbulb className="w-4 h-4" />
                                    Recommendations:
                                  </h5>
                                  <ul className="space-y-2 bg-yellow-50 p-3 rounded border border-yellow-200">
                                    {recommendations.map((rec, recIdx) => (
                                      <li
                                        key={recIdx}
                                        className="flex items-start gap-2 text-sm text-gray-700"
                                      >
                                        <span className="text-yellow-600 mt-1">
                                          •
                                        </span>
                                        <span>{rec}</span>
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </CardContent>
                </Card>
              )}

              {/* General Suggestions */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Lightbulb className="w-5 h-5 text-yellow-600" />
                    General Suggestions
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {result.analysis.suggestions.map((suggestion, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm">
                        <span className="text-yellow-600 mt-1">💡</span>
                        <span>{suggestion}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Preview View */}
          {viewMode === "preview" && (
            <div className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Optimized Resume Preview</CardTitle>
                  <CardDescription>
                    Preview updates automatically based on your section
                    selections
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="prose max-w-none">
                    <ReactMarkdown>{getFilteredMarkdown()}</ReactMarkdown>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Download Buttons */}
          <Card className="bg-gradient-to-r from-primary/10 to-blue-500/10 border-primary/20">
            <CardContent className="pt-6">
              <div className="space-y-4">
                <div className="text-center">
                  <h3 className="font-semibold text-lg mb-1">
                    Ready to Download?
                  </h3>
                  <p className="text-sm text-gray-600">
                    Get your optimized resume in your preferred format
                  </p>
                </div>

                {/* Font Selection */}
                <div className="bg-white rounded-lg p-4 border border-gray-200">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Select Resume Font (ATS-Safe)
                  </label>
                  <select
                    value={selectedFont}
                    onChange={(e) => setSelectedFont(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary focus:border-transparent"
                  >
                    {availableFonts.map((font) => (
                      <option key={font.value} value={font.value}>
                        {font.label}
                      </option>
                    ))}
                  </select>
                  <p className="text-xs text-gray-500 mt-2">
                    All fonts are ATS-friendly and will be applied to PDF and
                    DOCX formats
                  </p>
                </div>

                {/* Individual Download Buttons */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  <Button
                    onClick={() => handleDownload("markdown")}
                    disabled={downloading}
                    variant="outline"
                    className="border-2 hover:bg-primary/5"
                  >
                    {downloading ? (
                      <span className="animate-spin mr-2">⏳</span>
                    ) : (
                      <FileText className="w-4 h-4 mr-2" />
                    )}
                    Markdown (.md)
                  </Button>

                  <Button
                    onClick={() => handleDownload("pdf")}
                    disabled={downloading}
                    variant="outline"
                    className="border-2 hover:bg-primary/5"
                  >
                    {downloading ? (
                      <span className="animate-spin mr-2">⏳</span>
                    ) : (
                      <FileText className="w-4 h-4 mr-2" />
                    )}
                    PDF (.pdf)
                  </Button>

                  <Button
                    onClick={() => handleDownload("docx")}
                    disabled={downloading}
                    variant="outline"
                    className="border-2 hover:bg-primary/5"
                  >
                    {downloading ? (
                      <span className="animate-spin mr-2">⏳</span>
                    ) : (
                      <FileText className="w-4 h-4 mr-2" />
                    )}
                    Word (.docx)
                  </Button>
                </div>

                {/* Download All Button */}
                <div className="pt-2 border-t border-gray-200">
                  <Button
                    onClick={handleDownloadAll}
                    disabled={downloading}
                    size="lg"
                    className="w-full bg-primary hover:bg-primary/90"
                  >
                    {downloading ? (
                      <>
                        <span className="animate-spin mr-2">⏳</span>
                        Downloading...
                      </>
                    ) : (
                      <>
                        <Download className="w-5 h-5 mr-2" />
                        Download All Formats
                      </>
                    )}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}
