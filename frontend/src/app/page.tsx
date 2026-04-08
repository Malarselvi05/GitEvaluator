"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Github, Search, TrendingUp, ShieldCheck, Zap, Briefcase, ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";

export default function LandingPage() {
  const [githubUrl, setGithubUrl] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleAnalyze = (e: React.FormEvent) => {
    e.preventDefault();
    if (!githubUrl) return;
    setIsAnalyzing(true);
    // Simulate navigation to dashboard
    setTimeout(() => {
      window.location.href = `/dashboard?user=${githubUrl.split("/").pop()}`;
    }, 2000);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 relative overflow-hidden">
      {/* Background elements */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-600/10 blur-[120px] rounded-full" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-indigo-600/10 blur-[120px] rounded-full" />

      <header className="fixed top-0 w-full p-6 flex justify-between items-center z-50 px-12">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center shadow-lg shadow-primary/20">
            <Github className="text-white w-6 h-6" />
          </div>
          <span className="text-xl font-bold tracking-tight">GitEval<span className="text-primary">.ai</span></span>
        </div>
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-muted-foreground">
          <a href="#" className="hover:text-foreground transition-colors">Features</a>
          <a href="#" className="hover:text-foreground transition-colors">Pricing</a>
          <a href="#" className="hover:text-foreground transition-colors">API</a>
          <button className="bg-secondary px-5 py-2.5 rounded-full text-foreground hover:bg-secondary/80 transition-all">Sign In</button>
        </nav>
      </header>

      <main className="w-full max-w-6xl flex flex-col items-center pt-24 gap-20">
        <section className="text-center flex flex-col items-center gap-6 max-w-3xl">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 bg-primary/10 px-4 py-1.5 rounded-full border border-primary/20 text-primary text-sm font-medium"
          >
            <Zap className="w-4 h-4" />
            <span>AI-Powered Portfolio Analysis</span>
          </motion.div>
          
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-5xl md:text-7xl font-bold tracking-tight leading-[1.1]"
          >
            Bridge the gap between <span className="text-gradient">Code</span> and <span className="text-gradient">Career</span>
          </motion.h1>

          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-lg text-muted-foreground max-w-2xl"
          >
            Evaluate your GitHub profile like a recruiter would. Get AI-driven insights, 
            actionable feedback, and a project roadmaps to maximize your hiring potential.
          </motion.p>

          <motion.form 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            onSubmit={handleAnalyze}
            className="w-full max-w-xl mt-4 relative group"
          >
            <div className="absolute inset-0 bg-primary/20 blur-xl opacity-0 group-focus-within:opacity-100 transition-opacity rounded-full" />
            <div className="relative flex items-center bg-card border border-border rounded-full p-2 pl-6 focus-within:border-primary/50 transition-all shadow-2xl">
              <Search className="w-5 h-5 text-muted-foreground" />
              <input 
                type="text" 
                placeholder="github.com/username" 
                className="flex-1 bg-transparent border-none focus:ring-0 px-4 text-lg outline-none"
                value={githubUrl}
                onChange={(e) => setGithubUrl(e.target.value)}
              />
              <button 
                type="submit"
                disabled={isAnalyzing}
                className={cn(
                  "bg-primary text-white px-8 py-3 rounded-full font-semibold transition-all hover:scale-[1.02] active:scale-95 flex items-center gap-2",
                  isAnalyzing && "opacity-50 cursor-not-allowed"
                )}
              >
                {isAnalyzing ? "Analyzing..." : "Evaluate Profile"}
                {!isAnalyzing && <ChevronRight className="w-4 h-4" />}
              </button>
            </div>
          </motion.form>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full px-6">
          <FeatureCard 
            icon={<TrendingUp className="w-6 h-6 text-blue-400" />}
            title="Portfolio Scoring"
            description="Deep analysis of your code quality, innovation, and industry relevance across all repositories."
          />
          <FeatureCard 
            icon={<ShieldCheck className="w-6 h-6 text-emerald-400" />}
            title="Recruiter Verdict"
            description="Simulate a real-time hiring manager review to see if you'd pass the initial technical screen."
          />
          <FeatureCard 
            icon={<Briefcase className="w-6 h-6 text-purple-400" />}
            title="Career Roadmap"
            description="AI identifies skill gaps and suggests the exact projects you need to build next to get hired."
          />
        </section>
      </main>

      <footer className="mt-auto pt-20 pb-10 text-muted-foreground text-sm">
        © 2026 GitEval.ai — Built for the next generation of engineers.
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) {
  return (
    <motion.div 
      whileHover={{ y: -5 }}
      className="glass p-8 rounded-3xl flex flex-col gap-4 border border-border/50 hover:border-primary/30 transition-colors"
    >
      <div className="w-12 h-12 rounded-2xl bg-secondary flex items-center justify-center">
        {icon}
      </div>
      <h3 className="text-xl font-bold">{title}</h3>
      <p className="text-muted-foreground leading-relaxed">
        {description}
      </p>
    </motion.div>
  );
}
