import { Card, CardContent, CardHeader, CardTitle } from "./ui/Card";
import { type CVSections } from "@/lib/api";
import { ChevronRight } from "lucide-react";

interface StructuredCVDisplayProps {
  sections: CVSections;
}

export function StructuredCVDisplay({ sections }: StructuredCVDisplayProps) {
  return (
    <div className="space-y-4">
      {sections.sections.map((section, sectionIndex) => (
        <Card key={sectionIndex} className="overflow-hidden">
          <CardHeader className="bg-primary/5 border-b">
            <CardTitle className="text-xl font-bold text-primary">
              {section.title}
            </CardTitle>
          </CardHeader>
          <CardContent className="p-6 space-y-4">
            {/* Section paragraphs (if no subsections) */}
            {section.paragraphs.length > 0 && (
              <div className="space-y-2">
                {section.paragraphs.map((paragraph, pIndex) => (
                  <p
                    key={pIndex}
                    className="text-sm text-foreground leading-relaxed"
                    dangerouslySetInnerHTML={{ __html: paragraph }}
                  />
                ))}
              </div>
            )}

            {/* Section bullets (if no subsections) */}
            {section.bullets.length > 0 && (
              <ul className="space-y-2 ml-4">
                {section.bullets.map((bullet, bIndex) => (
                  <li
                    key={bIndex}
                    className="text-sm text-foreground flex items-start gap-2"
                  >
                    <ChevronRight className="h-4 w-4 text-primary mt-0.5 flex-shrink-0" />
                    <span dangerouslySetInnerHTML={{ __html: bullet }} />
                  </li>
                ))}
              </ul>
            )}

            {/* Subsections */}
            {section.subsections.length > 0 && (
              <div className="space-y-6">
                {section.subsections.map((subsection, subIndex) => (
                  <div
                    key={subIndex}
                    className="border-l-2 border-primary/30 pl-4 space-y-2"
                  >
                    <div className="flex justify-between items-baseline">
                      <h3 className="text-base font-semibold text-foreground flex-1">
                        {subsection.title}
                      </h3>
                      {subsection.date && (
                        <span className="text-xs text-muted-foreground ml-4">
                          {subsection.date}
                        </span>
                      )}
                    </div>

                    {/* Subsection paragraphs */}
                    {subsection.paragraphs.length > 0 && (
                      <div className="space-y-2">
                        {subsection.paragraphs.map((paragraph, pIndex) => (
                          <p
                            key={pIndex}
                            className="text-sm text-muted-foreground leading-relaxed"
                            dangerouslySetInnerHTML={{ __html: paragraph }}
                          />
                        ))}
                      </div>
                    )}

                    {/* Subsection bullets */}
                    {subsection.bullets.length > 0 && (
                      <ul className="space-y-1.5 ml-2">
                        {subsection.bullets.map((bullet, bIndex) => (
                          <li
                            key={bIndex}
                            className="text-sm text-muted-foreground flex items-start gap-2"
                          >
                            <ChevronRight className="h-3.5 w-3.5 text-primary/60 mt-0.5 flex-shrink-0" />
                            <span
                              dangerouslySetInnerHTML={{ __html: bullet }}
                            />
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      ))}

      {sections.sections.length === 0 && (
        <Card>
          <CardContent className="p-6 text-center text-muted-foreground">
            <p>No sections found in the optimized CV.</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
