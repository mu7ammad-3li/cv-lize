import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { type ParsedResumeData, type CVSections } from "@/lib/api";
import { ProfessionalTemplate } from "./ProfessionalTemplate";
import { transformToTemplateData } from "@/lib/templateDataTransformer";

interface ProfessionalResumeDisplayProps {
  data: ParsedResumeData;
  sections?: CVSections;
  onDownload?: () => void;
}

export function ProfessionalResumeDisplay({
  data,
  sections,
  onDownload,
}: ProfessionalResumeDisplayProps) {
  const templateData = transformToTemplateData(data);

  return (
    <div className="w-full">
      <ProfessionalTemplate data={templateData} sections={sections} />

      {onDownload && (
        <div className="pt-6 flex justify-center print:hidden">
          <Button onClick={onDownload} className="gap-2">
            <Download className="h-4 w-4" />
            Download PDF
          </Button>
        </div>
      )}
    </div>
  );
}
