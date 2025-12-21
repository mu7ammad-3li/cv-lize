import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, FileText, AlertCircle } from "lucide-react";
import { Card, CardContent } from "./ui/Card";
import { Button } from "./ui/Button";
import { uploadCV, type UploadResponse } from "@/lib/api";

interface FileUploadProps {
  onUploadSuccess: (data: UploadResponse) => void;
}

export function FileUpload({ onUploadSuccess }: FileUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      const file = acceptedFiles[0];
      if (!file) return;

      // Validate file size (5MB)
      const maxSize = 5 * 1024 * 1024;
      if (file.size > maxSize) {
        setError("File size exceeds 5MB limit");
        return;
      }

      // Validate file type
      const validTypes = [".pdf", ".md", ".markdown", ".txt"];
      const fileExt = file.name
        .toLowerCase()
        .substring(file.name.lastIndexOf("."));
      if (!validTypes.includes(fileExt)) {
        setError(
          "Invalid file type. Please upload PDF, Markdown, or Text files.",
        );
        return;
      }

      setUploadedFile(file);
      setError(null);
      setUploading(true);

      try {
        const response = await uploadCV(file);
        onUploadSuccess(response);
      } catch (err: any) {
        console.error("Upload error:", err);

        // Handle security validation errors
        if (
          err.response?.status === 400 &&
          err.response?.data?.detail?.issues
        ) {
          const issues = err.response.data.detail.issues;
          setError(
            `Security validation failed: ${issues.map((i: any) => i.message).join(", ")}`,
          );
        } else if (err.response?.data?.detail) {
          setError(err.response.data.detail);
        } else {
          setError("Failed to upload CV. Please try again.");
        }
      } finally {
        setUploading(false);
      }
    },
    [onUploadSuccess],
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "text/markdown": [".md", ".markdown"],
      "text/plain": [".txt"],
    },
    maxFiles: 1,
    disabled: uploading,
  });

  return (
    <div className="w-full max-w-2xl mx-auto">
      <Card>
        <CardContent className="p-6">
          <div
            {...getRootProps()}
            className={`
              border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
              transition-colors duration-200
              ${isDragActive ? "border-primary bg-primary/5" : "border-border hover:border-primary/50"}
              ${uploading ? "opacity-50 cursor-not-allowed" : ""}
            `}
          >
            <input {...getInputProps()} />

            <div className="flex flex-col items-center gap-4">
              {uploading ? (
                <>
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
                  <p className="text-sm text-muted-foreground">
                    Uploading and analyzing...
                  </p>
                </>
              ) : (
                <>
                  <Upload className="h-12 w-12 text-muted-foreground" />

                  {isDragActive ? (
                    <p className="text-lg font-medium">Drop your CV here</p>
                  ) : (
                    <>
                      <div>
                        <p className="text-lg font-medium mb-2">
                          Drag & drop your CV here
                        </p>
                        <p className="text-sm text-muted-foreground">
                          or click to browse
                        </p>
                      </div>

                      <div className="flex gap-2 text-xs">
                        <span className="px-2 py-1 bg-secondary rounded text-foreground font-medium">
                          PDF
                        </span>
                        <span className="px-2 py-1 bg-secondary rounded text-foreground font-medium">
                          Markdown
                        </span>
                        <span className="px-2 py-1 bg-secondary rounded text-foreground font-medium">
                          Text
                        </span>
                      </div>

                      <p className="text-xs text-muted-foreground">
                        Max file size: 5MB • Scanned for security
                      </p>
                    </>
                  )}
                </>
              )}
            </div>
          </div>

          {uploadedFile && !error && (
            <div className="mt-4 flex items-center gap-2 text-sm text-muted-foreground">
              <FileText className="h-4 w-4" />
              <span>{uploadedFile.name}</span>
              <span className="text-xs">
                ({(uploadedFile.size / 1024).toFixed(1)} KB)
              </span>
            </div>
          )}

          {error && (
            <div className="mt-4 flex items-start gap-2 p-4 bg-destructive/10 border border-destructive/20 rounded-lg">
              <AlertCircle className="h-5 w-5 text-destructive flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm font-medium text-destructive">
                  Upload Failed
                </p>
                <p className="text-sm text-destructive/80 mt-1">{error}</p>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setError(null)}
                className="text-destructive hover:text-destructive/80"
              >
                Dismiss
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
