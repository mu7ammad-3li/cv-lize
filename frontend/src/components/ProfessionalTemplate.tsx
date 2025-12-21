import { Mail, Phone, MapPin, Globe, Linkedin } from "lucide-react";
import { type CVSections } from "@/lib/api";

interface ProfessionalTemplateData {
  name: string;
  title: string;
  email: string;
  phone: string;
  location: string;
  website: string;
  linkedin?: string;
  summary: string;
  experience: Array<{
    company: string;
    dates: string;
    role: string;
    bullets: string[];
  }>;
  skills_languages: string;
  skills_tools: string;
  education: {
    school: string;
    dates: string;
    degree: string;
  };
  certifications?: string[];
}

interface ProfessionalTemplateProps {
  data: ProfessionalTemplateData;
  sections?: CVSections;
}

export function ProfessionalTemplate({
  data,
  sections,
}: ProfessionalTemplateProps) {
  return (
    <div className="professional-resume-template">
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:ital,wght@0,400;0,500;0,700;1,400;1,500&display=swap');

        .professional-resume-template {
          font-family: 'Google Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
          color: #1a1a1a;
          line-height: 1.6;
          font-size: 10pt;
          margin: 0 auto;
          padding: 3rem 2.5rem;
          background: #fafafa;
          max-width: 210mm;
          min-height: 297mm;
          box-sizing: border-box;
        }

        /* Header Section */
        .professional-resume-template .header {
          text-align: center;
          margin-bottom: 1.5rem;
          padding-bottom: 1rem;
          border-bottom: 3px solid #000;
        }

        .professional-resume-template .name {
          font-size: 32pt;
          font-weight: 700;
          letter-spacing: -0.03em;
          margin-bottom: 0.3rem;
          color: #000;
        }

        .professional-resume-template .title {
          font-size: 10pt;
          text-transform: uppercase;
          letter-spacing: 0.15em;
          color: #666;
          font-weight: 400;
          margin-bottom: 0.5rem;
        }

        /* Contact Info Bar */
        .professional-resume-template .contact-info {
          display: flex;
          justify-content: center;
          align-items: center;
          flex-wrap: wrap;
          gap: 0.75rem 1.2rem;
          color: #555;
          font-size: 8.5pt;
          margin-top: 0.5rem;
        }

        .professional-resume-template .contact-item {
          display: flex;
          align-items: center;
          gap: 0.35rem;
        }

        .professional-resume-template .contact-icon {
          width: 12px;
          height: 12px;
          color: #666;
        }

        /* Section Styling */
        .professional-resume-template .section {
          margin-bottom: 1.75rem;
        }

        .professional-resume-template .section-title {
          font-size: 12pt;
          font-weight: 700;
          border-bottom: 2px solid #000;
          padding-bottom: 0.25rem;
          margin-bottom: 1rem;
          width: 100%;
          display: block;
        }

        /* Experience & Items */
        .professional-resume-template .experience-item {
          margin-bottom: 1.25rem;
          page-break-inside: avoid;
        }

        .professional-resume-template .item-header {
          display: flex;
          justify-content: space-between;
          align-items: baseline;
          margin-bottom: 0.15rem;
        }

        .professional-resume-template .subsection-header {
          display: flex;
          justify-content: space-between;
          align-items: baseline;
          margin-bottom: 0.15rem;
        }

        .professional-resume-template .company-name {
          font-weight: 700;
          font-size: 11pt;
          color: #000;
        }

        .professional-resume-template .subsection-title {
          font-weight: 700;
          font-size: 11pt;
          color: #000;
          flex: 1;
        }

        .professional-resume-template .date,
        .professional-resume-template .subsection-date {
          color: #666;
          font-weight: 400;
          font-size: 9pt;
          white-space: nowrap;
          margin-left: 1rem;
        }

        .professional-resume-template .item-sub {
          font-style: italic;
          color: #444;
          margin-bottom: 0.5rem;
          font-size: 10pt;
        }

        /* Bold text support */
        .professional-resume-template strong,
        .professional-resume-template b {
          font-weight: 700;
        }

        /* Lists */
        .professional-resume-template ul {
          margin: 0.5rem 0 0 0;
          padding-left: 1.25rem;
          list-style-type: disc;
        }

        .professional-resume-template li {
          margin-bottom: 0.35rem;
          line-height: 1.5;
          color: #333;
        }

        /* Skills Section */
        .professional-resume-template .skills-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 1rem;
          margin-top: 0.5rem;
        }

        .professional-resume-template .skill-category {
          margin-bottom: 0.75rem;
        }

        .professional-resume-template .skill-label {
          font-weight: 700;
          display: block;
          margin-bottom: 0.25rem;
          font-size: 10pt;
          color: #000;
        }

        .professional-resume-template .skill-items {
          color: #333;
          font-size: 9.5pt;
          line-height: 1.5;
        }

        /* Education Section */
        .professional-resume-template .education-item {
          page-break-inside: avoid;
        }

        .professional-resume-template .degree {
          font-size: 10pt;
          color: #333;
          margin-top: 0.15rem;
        }

        /* Certifications */
        .professional-resume-template .certifications-list {
          margin: 0.5rem 0 0 0;
          padding-left: 1.25rem;
          list-style-type: disc;
        }

        .professional-resume-template .certifications-list li {
          margin-bottom: 0.35rem;
          color: #333;
        }

        .professional-resume-template p {
          margin: 0.5rem 0 0 0;
          color: #333;
          line-height: 1.6;
          text-align: justify;
        }
      `}</style>

      <div className="header">
        <div className="name">{data.name}</div>
        <div className="title">{data.title}</div>
        <div className="contact-info">
          {data.email && (
            <span className="contact-item">
              <Mail className="contact-icon" />
              <span>{data.email}</span>
            </span>
          )}
          {data.phone && (
            <span className="contact-item">
              <Phone className="contact-icon" />
              <span>{data.phone}</span>
            </span>
          )}
          {data.location && (
            <span className="contact-item">
              <MapPin className="contact-icon" />
              <span>{data.location}</span>
            </span>
          )}
          {data.linkedin && (
            <span className="contact-item">
              <Linkedin className="contact-icon" />
              <span>{data.linkedin}</span>
            </span>
          )}
          {data.website && (
            <span className="contact-item">
              <Globe className="contact-icon" />
              <span>{data.website}</span>
            </span>
          )}
        </div>
      </div>

      {data.summary && (
        <div className="section">
          <div className="section-title">Professional Summary</div>
          <p>{data.summary}</p>
        </div>
      )}

      {/* Use structured sections if available */}
      {sections && sections.sections && sections.sections.length > 0 ? (
        <>
          {sections.sections
            .filter((section) => {
              const title = section.title.toLowerCase();
              return (
                title !== "professional summary" &&
                title !== "software developer" &&
                title !== "software engineer" &&
                title !== "full stack developer" &&
                title !== "full stack engineer" &&
                title !== "contact information"
              );
            })
            .map((section, sectionIndex) => (
              <div key={sectionIndex} className="section">
                <div className="section-title">{section.title}</div>

                {/* Section-level paragraphs (if no subsections) */}
                {section.paragraphs && section.paragraphs.length > 0 && (
                  <>
                    {section.paragraphs.map((paragraph, pIndex) => (
                      <p
                        key={pIndex}
                        dangerouslySetInnerHTML={{ __html: paragraph }}
                      />
                    ))}
                  </>
                )}

                {/* Section-level bullets (if no subsections) */}
                {section.bullets && section.bullets.length > 0 && (
                  <ul>
                    {section.bullets.map((bullet, bIndex) => (
                      <li
                        key={bIndex}
                        dangerouslySetInnerHTML={{ __html: bullet }}
                      />
                    ))}
                  </ul>
                )}

                {/* Subsections */}
                {section.subsections && section.subsections.length > 0 && (
                  <>
                    {section.subsections.map((subsection, subIndex) => (
                      <div key={subIndex} className="experience-item">
                        <div className="subsection-header">
                          <div className="subsection-title">
                            {subsection.title}
                          </div>
                          {subsection.date && (
                            <div className="subsection-date">
                              {subsection.date}
                            </div>
                          )}
                        </div>

                        {/* Subsection paragraphs */}
                        {subsection.paragraphs &&
                          subsection.paragraphs.length > 0 && (
                            <>
                              {subsection.paragraphs.map(
                                (paragraph, pIndex) => (
                                  <p
                                    key={pIndex}
                                    dangerouslySetInnerHTML={{
                                      __html: paragraph,
                                    }}
                                  />
                                ),
                              )}
                            </>
                          )}

                        {/* Subsection bullets */}
                        {subsection.bullets &&
                          subsection.bullets.length > 0 && (
                            <ul>
                              {subsection.bullets.map((bullet, bIndex) => (
                                <li
                                  key={bIndex}
                                  dangerouslySetInnerHTML={{ __html: bullet }}
                                />
                              ))}
                            </ul>
                          )}
                      </div>
                    ))}
                  </>
                )}
              </div>
            ))}
        </>
      ) : (
        <>
          {/* Fallback to traditional structure */}
          {data.experience && data.experience.length > 0 && (
            <div className="section">
              <div className="section-title">Experience</div>
              {data.experience.map((exp, index) => (
                <div key={index} className="experience-item">
                  <div className="item-header">
                    <span className="company-name">{exp.company}</span>
                    <span className="date">{exp.dates}</span>
                  </div>
                  <div className="item-sub">{exp.role}</div>
                  {exp.bullets && exp.bullets.length > 0 && (
                    <ul>
                      {exp.bullets.map((bullet, bulletIndex) => (
                        <li key={bulletIndex}>{bullet}</li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          )}

          {(data.skills_languages || data.skills_tools) && (
            <div className="section">
              <div className="section-title">Technical Skills</div>
              <div className="skills-grid">
                {data.skills_languages && (
                  <div className="skill-category">
                    <span className="skill-label">Languages & Frameworks:</span>
                    <div className="skill-items">{data.skills_languages}</div>
                  </div>
                )}
                {data.skills_tools && (
                  <div className="skill-category">
                    <span className="skill-label">Tools & Platforms:</span>
                    <div className="skill-items">{data.skills_tools}</div>
                  </div>
                )}
              </div>
            </div>
          )}

          {data.education && data.education.school && (
            <div className="section">
              <div className="section-title">Education</div>
              <div className="education-item">
                <div className="item-header">
                  <span className="company-name">{data.education.school}</span>
                  <span className="date">{data.education.dates}</span>
                </div>
                <div className="degree">{data.education.degree}</div>
              </div>
            </div>
          )}

          {data.certifications && data.certifications.length > 0 && (
            <div className="section">
              <div className="section-title">Certifications</div>
              <ul className="certifications-list">
                {data.certifications.map((cert, index) => (
                  <li key={index}>{cert}</li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}
    </div>
  );
}
