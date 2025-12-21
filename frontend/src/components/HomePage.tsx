import { ArrowRight, FileText, Sparkles, Shield, Zap, CheckCircle2, Upload, Search, Download } from "lucide-react";

interface HomePageProps {
  onGetStarted: () => void;
}

export function HomePage({ onGetStarted }: HomePageProps) {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-background via-background to-primary/5 pt-16 pb-32">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center space-y-8">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium">
              <Sparkles className="h-4 w-4" />
              AI-Powered Resume Optimization
            </div>

            <h1 className="text-5xl md:text-7xl font-bold tracking-tight">
              Transform Your Resume,
              <br />
              <span className="bg-gradient-to-r from-[#2563eb] to-[#10b981] bg-clip-text text-transparent">
                Land Your Dream Job
              </span>
            </h1>

            <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
              Upload your CV and get instant AI-powered analysis, ATS compatibility checks,
              and professionally optimized resumes tailored to your target job.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <button
                onClick={onGetStarted}
                className="group px-8 py-4 bg-primary text-primary-foreground rounded-lg font-semibold text-lg hover:bg-primary/90 transition-all flex items-center gap-2 shadow-lg hover:shadow-xl"
              >
                Get Started Free
                <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </button>

              <button className="px-8 py-4 border border-border rounded-lg font-semibold text-lg hover:bg-accent transition-colors">
                See How It Works
              </button>
            </div>

            <div className="flex items-center justify-center gap-8 pt-8 text-sm text-muted-foreground">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-5 w-5 text-primary" />
                <span>100% Free</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-5 w-5 text-primary" />
                <span>No Sign-Up Required</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-5 w-5 text-primary" />
                <span>Secure & Private</span>
              </div>
            </div>
          </div>
        </div>

        {/* Decorative Elements */}
        <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none opacity-30">
          <div className="absolute top-20 left-10 w-72 h-72 bg-primary/20 rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-secondary/20 rounded-full blur-3xl"></div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-background">
        <div className="container mx-auto px-4">
          <div className="text-center space-y-4 mb-16">
            <h2 className="text-4xl font-bold tracking-tight">
              Why Choose <span className="text-[#2563eb]">CV</span>
              <span className="bg-gradient-to-r from-[#2563eb] to-[#10b981] bg-clip-text text-transparent">lize</span>?
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Powerful features designed to help you stand out from the competition
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {/* Feature 1 */}
            <div className="group p-8 rounded-2xl border border-border bg-card hover:shadow-xl transition-all hover:border-primary/50">
              <div className="inline-flex items-center justify-center w-14 h-14 bg-primary/10 rounded-xl mb-6 group-hover:bg-primary/20 transition-colors">
                <Shield className="h-7 w-7 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Security First</h3>
              <p className="text-muted-foreground leading-relaxed">
                Multi-layer validation with advanced malware scanning ensures your files are safe.
                Your privacy is our top priority.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="group p-8 rounded-2xl border border-border bg-card hover:shadow-xl transition-all hover:border-primary/50">
              <div className="inline-flex items-center justify-center w-14 h-14 bg-secondary/10 rounded-xl mb-6 group-hover:bg-secondary/20 transition-colors">
                <Sparkles className="h-7 w-7 text-secondary" />
              </div>
              <h3 className="text-xl font-semibold mb-3">AI-Powered Analysis</h3>
              <p className="text-muted-foreground leading-relaxed">
                Google Gemini AI analyzes your CV against job requirements and provides
                actionable insights to improve your chances.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="group p-8 rounded-2xl border border-border bg-card hover:shadow-xl transition-all hover:border-primary/50">
              <div className="inline-flex items-center justify-center w-14 h-14 bg-primary/10 rounded-xl mb-6 group-hover:bg-primary/20 transition-colors">
                <Zap className="h-7 w-7 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Instant Results</h3>
              <p className="text-muted-foreground leading-relaxed">
                Get your optimized CV and detailed analysis in under 30 seconds.
                No waiting, no hassle.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-24 bg-gradient-to-b from-background to-primary/5">
        <div className="container mx-auto px-4">
          <div className="text-center space-y-4 mb-16">
            <h2 className="text-4xl font-bold tracking-tight">How It Works</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Get your optimized resume in three simple steps
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 max-w-5xl mx-auto">
            {/* Step 1 */}
            <div className="relative text-center space-y-4">
              <div className="inline-flex items-center justify-center w-20 h-20 bg-primary rounded-2xl mb-4 shadow-lg">
                <Upload className="h-10 w-10 text-primary-foreground" />
              </div>
              <div className="absolute top-10 left-[60%] hidden md:block w-32 h-0.5 bg-gradient-to-r from-primary to-transparent"></div>
              <h3 className="text-2xl font-bold">Upload Your CV</h3>
              <p className="text-muted-foreground">
                Drag and drop your resume or paste a job description. We support PDF, DOC, and DOCX formats.
              </p>
            </div>

            {/* Step 2 */}
            <div className="relative text-center space-y-4">
              <div className="inline-flex items-center justify-center w-20 h-20 bg-secondary rounded-2xl mb-4 shadow-lg">
                <Search className="h-10 w-10 text-secondary-foreground" />
              </div>
              <div className="absolute top-10 left-[60%] hidden md:block w-32 h-0.5 bg-gradient-to-r from-secondary to-transparent"></div>
              <h3 className="text-2xl font-bold">AI Analysis</h3>
              <p className="text-muted-foreground">
                Our AI analyzes your CV, checks ATS compatibility, and identifies areas for improvement.
              </p>
            </div>

            {/* Step 3 */}
            <div className="text-center space-y-4">
              <div className="inline-flex items-center justify-center w-20 h-20 bg-primary rounded-2xl mb-4 shadow-lg">
                <Download className="h-10 w-10 text-primary-foreground" />
              </div>
              <h3 className="text-2xl font-bold">Get Your Resume</h3>
              <p className="text-muted-foreground">
                Download your professionally optimized resume and detailed feedback to land more interviews.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-primary text-primary-foreground">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 max-w-5xl mx-auto text-center">
            <div className="space-y-2">
              <div className="text-5xl font-bold">10K+</div>
              <div className="text-primary-foreground/80">CVs Optimized</div>
            </div>
            <div className="space-y-2">
              <div className="text-5xl font-bold">95%</div>
              <div className="text-primary-foreground/80">ATS Pass Rate</div>
            </div>
            <div className="space-y-2">
              <div className="text-5xl font-bold">30s</div>
              <div className="text-primary-foreground/80">Average Time</div>
            </div>
            <div className="space-y-2">
              <div className="text-5xl font-bold">100%</div>
              <div className="text-primary-foreground/80">Free Forever</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-gradient-to-b from-background to-secondary/5">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center space-y-8 p-12 rounded-3xl border border-border bg-card shadow-xl">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-primary/10 rounded-2xl">
              <FileText className="h-8 w-8 text-primary" />
            </div>

            <h2 className="text-4xl md:text-5xl font-bold tracking-tight">
              Ready to Optimize Your Resume?
            </h2>

            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Join thousands of job seekers who have improved their resumes with CV-lize.
              Start for free today, no credit card required.
            </p>

            <button
              onClick={onGetStarted}
              className="group px-10 py-5 bg-primary text-primary-foreground rounded-xl font-bold text-xl hover:bg-primary/90 transition-all flex items-center gap-2 mx-auto shadow-lg hover:shadow-2xl hover:scale-105"
            >
              Start Optimizing Now
              <ArrowRight className="h-6 w-6 group-hover:translate-x-1 transition-transform" />
            </button>

            <div className="flex items-center justify-center gap-6 pt-4 text-sm text-muted-foreground">
              <div className="flex items-center gap-2">
                <Shield className="h-4 w-4" />
                <span>Secure & Private</span>
              </div>
              <div className="flex items-center gap-2">
                <Zap className="h-4 w-4" />
                <span>Instant Results</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
