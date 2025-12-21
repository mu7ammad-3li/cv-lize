import { useState } from "react";
import { HomePage } from "./components/HomePage";
import { FileUpload } from "./components/FileUpload";
import { CVAnalysis } from "./components/CVAnalysis";
import { type UploadResponse } from "./lib/api";
import { FileText, Github, Heart } from "lucide-react";

function App() {
  const [uploadData, setUploadData] = useState<UploadResponse | null>(null);
  const [showUpload, setShowUpload] = useState(false);

  const handleUploadSuccess = (data: UploadResponse) => {
    setUploadData(data);
  };

  const handleReset = () => {
    setUploadData(null);
    setShowUpload(false);
  };

  const handleGetStarted = () => {
    setShowUpload(true);
  };

  return (
    <div className="min-h-screen bg-linear-to-b from-background to-secondary/20">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-backdrop-filter:bg-background/60">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary/10 rounded-lg">
                <FileText className="h-6 w-6 text-primary" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">
                  <span className="text-[#2563eb]">CV</span>
                  <span className="bg-gradient-to-r from-[#2563eb] to-[#10b981] bg-clip-text text-transparent">
                    lize
                  </span>
                </h1>
                <p className="text-sm text-muted-foreground">
                  AI-Powered Resume Optimization
                </p>
              </div>
            </div>

            {(uploadData || showUpload) && (
              <button
                onClick={handleReset}
                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                {uploadData ? "Upload New CV" : "Back to Home"}
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main>
        {!showUpload && !uploadData ? (
          <HomePage onGetStarted={handleGetStarted} />
        ) : !uploadData ? (
          <div className="container mx-auto px-4 py-12">
            <div className="space-y-8">
              <div className="text-center space-y-4 mb-12">
                <h2 className="text-4xl font-bold tracking-tight">
                  Upload Your Resume
                </h2>
                <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                  Upload your CV and get instant AI-powered analysis, ATS
                  compatibility checks, and optimized resume tailored to your
                  target job.
                </p>
              </div>

              <FileUpload onUploadSuccess={handleUploadSuccess} />
            </div>
          </div>
        ) : (
          <div className="container mx-auto px-4 py-12">
            <div className="space-y-6">
              {/* Upload Success Message */}
              <div className="bg-green-50 border border-green-200 rounded-lg p-4 max-w-2xl mx-auto">
                <div className="flex items-start gap-3">
                  <svg
                    className="w-5 h-5 text-green-600 mt-0.5 shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <div className="flex-1">
                    <h3 className="font-semibold text-green-900 mb-1">
                      CV Uploaded Successfully!
                    </h3>
                    <p className="text-sm text-green-700">
                      <strong>{uploadData.filename}</strong> has been processed
                      and is ready for analysis. We extracted{" "}
                      {uploadData.parsed_data.skills.length} skills,{" "}
                      {uploadData.parsed_data.experience.length} work
                      experiences, and {uploadData.parsed_data.education.length}{" "}
                      education entries.
                    </p>
                  </div>
                </div>
              </div>

              {/* Analysis Component */}
              <CVAnalysis
                sessionId={uploadData.session_id}
                filename={uploadData.filename}
              />
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t mt-24">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <span>Built with</span>
              <Heart className="h-4 w-4 text-red-500 fill-red-500" />
              <span>by</span>
              <a
                href="https://github.com/mu7ammad-3li/"
                target="_blank"
                rel="noopener noreferrer"
                className="font-semibold text-foreground hover:text-primary transition-colors"
              >
                Muhammad Ali
              </a>
            </div>
            <a
              href="https://github.com/mu7ammad-3li/"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 hover:text-foreground transition-colors"
            >
              <Github className="h-4 w-4" />
              <span>View on GitHub</span>
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
