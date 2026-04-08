"use client";

import { motion } from "framer-motion";
import { 
  Github, 
  TrendingUp, 
  Code, 
  Lightbulb, 
  CheckCircle2, 
  ArrowUpRight,
  User,
  Star,
  GitFork,
  ExternalLink,
  MessageSquareCode
} from "lucide-react";
import { 
  Radar, 
  RadarChart, 
  PolarGrid, 
  PolarAngleAxis, 
  ResponsiveContainer 
} from "recharts";
import { cn } from "@/lib/utils";

// Mock data for demonstration
const radarData = [
  { subject: 'Code Quality', A: 85, fullMark: 100 },
  { subject: 'Innovation', A: 70, fullMark: 100 },
  { subject: 'Documentation', A: 90, fullMark: 100 },
  { subject: 'Testing', A: 40, fullMark: 100 },
  { subject: 'Industry Fit', A: 75, fullMark: 100 },
  { subject: 'Deployment', A: 55, fullMark: 100 },
];

const repos = [
  { 
    name: "ai-fraud-detector", 
    stars: 124, 
    forks: 32, 
    score: 88, 
    tier: "Advanced", 
    tags: ["Python", "FastAPI", "ML"],
    description: "Real-time fraud detection pipeline using isolation forest and stream processing."
  },
  { 
    name: "react-ui-toolkit", 
    stars: 45, 
    forks: 12, 
    score: 72, 
    tier: "Intermediate", 
    tags: ["TS", "React", "Tailwind"],
    description: "A headless UI component library focused on accessibility and motion."
  },
  { 
    name: "simple-todo", 
    stars: 2, 
    forks: 0, 
    score: 34, 
    tier: "Beginner", 
    tags: ["JS", "HTML"],
    description: "A basic todo application."
  }
];

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 h-full w-20 border-r border-border/50 flex flex-col items-center py-8 gap-10 z-50 glass">
        <div className="w-12 h-12 bg-primary rounded-2xl flex items-center justify-center shadow-lg shadow-primary/20">
          <Github className="text-white w-7 h-7" />
        </div>
        <nav className="flex flex-col gap-6 text-muted-foreground">
          <button className="p-3 bg-primary/10 text-primary rounded-xl transition-all self-center">
            <TrendingUp className="w-6 h-6" />
          </button>
          <button className="p-3 hover:bg-secondary rounded-xl transition-all self-center">
            <Code className="w-6 h-6" />
          </button>
          <button className="p-3 hover:bg-secondary rounded-xl transition-all self-center">
            <User className="w-6 h-6" />
          </button>
        </nav>
      </aside>

      <main className="flex-1 ml-20 p-10 pb-20">
        <header className="flex justify-between items-end mb-12">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-3">
              Portfolio Overview
              <span className="bg-emerald-500/10 text-emerald-500 text-xs px-2 py-1 rounded border border-emerald-500/20">Active</span>
            </h1>
            <p className="text-muted-foreground mt-1">Analyzing github.com/johndoe</p>
          </div>
          <div className="flex gap-4">
            <button className="bg-secondary text-foreground px-6 py-2.5 rounded-xl font-medium flex items-center gap-2 hover:bg-secondary/80 transition-all">
              <ExternalLink className="w-4 h-4" />
              Public View
            </button>
            <button className="bg-primary text-white px-6 py-2.5 rounded-xl font-medium flex items-center gap-2 hover:scale-[1.02] transition-all shadow-lg shadow-primary/20">
              Refresh Analysis
            </button>
          </div>
        </header>

        <section className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Score Card */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="lg:col-span-2 glass rounded-[2.5rem] p-10 flex flex-col md:flex-row items-center gap-10"
          >
            <div className="relative w-48 h-48 flex items-center justify-center">
              <svg className="w-full h-full -rotate-90">
                <circle 
                  cx="96" cy="96" r="88" 
                  fill="none" 
                  stroke="currentColor" 
                  strokeWidth="12" 
                  className="text-secondary"
                />
                <circle 
                  cx="96" cy="96" r="88" 
                  fill="none" 
                  stroke="currentColor" 
                  strokeWidth="12" 
                  strokeDasharray={2 * Math.PI * 88}
                  strokeDashoffset={(1 - 0.76) * (2 * Math.PI * 88)}
                  className="text-primary"
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute flex flex-col items-center">
                <span className="text-5xl font-black">76</span>
                <span className="text-sm font-bold text-muted-foreground tracking-widest">GRADE B+</span>
              </div>
            </div>

            <div className="flex-1 space-y-6">
              <div>
                <h2 className="text-2xl font-bold">Strong Potential</h2>
                <p className="text-sm text-muted-foreground mt-1 leading-relaxed">
                Your profile is better than 82% of developers in your target role. 
                Focus on improving &quot;Testing&quot; and &quot;Deployment&quot; scores to reach A-tier.
              </p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-secondary/30 rounded-2xl p-4 border border-border/50">
                  <span className="text-xs font-bold text-muted-foreground block mb-1 uppercase tracking-wider">Top Repo</span>
                  <span className="font-bold">ai-fraud-detector</span>
                </div>
                <div className="bg-secondary/30 rounded-2xl p-4 border border-border/50">
                  <span className="text-xs font-bold text-muted-foreground block mb-1 uppercase tracking-wider">Rank</span>
                  <span className="font-bold">Top 18%</span>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Radar Chart */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
            className="glass rounded-[2.5rem] p-8 flex flex-col items-center justify-center"
          >
            <h3 className="text-sm font-bold text-muted-foreground uppercase tracking-widest mb-4">Competency Radar</h3>
            <div className="w-full h-64">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                  <PolarGrid stroke="#27272a" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 10 }} />
                  <Radar
                    name="Skills"
                    dataKey="A"
                    stroke="#3b82f6"
                    fill="#3b82f6"
                    fillOpacity={0.3}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </motion.div>

          {/* Repository List */}
          <div className="lg:col-span-2 space-y-6">
            <h3 className="text-xl font-bold flex items-center gap-2">
              Analyzed Repositories
              <span className="text-sm font-normal text-muted-foreground">({repos.length})</span>
            </h3>
            <div className="space-y-4">
              {repos.map((repo, i) => (
                <motion.div 
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.2 + i * 0.1 }}
                  key={repo.name}
                  className="glass group p-6 rounded-3xl flex flex-col md:flex-row md:items-center gap-6 glass-hover"
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-1">
                      <h4 className="text-lg font-bold group-hover:text-primary transition-colors">{repo.name}</h4>
                      <span className={cn(
                        "text-[10px] font-bold px-2 py-0.5 rounded-full border",
                        repo.tier === "Advanced" ? "bg-purple-500/10 text-purple-400 border-purple-500/20" :
                        repo.tier === "Intermediate" ? "bg-blue-500/10 text-blue-400 border-blue-500/20" :
                        "bg-gray-500/10 text-gray-400 border-gray-500/20"
                      )}>
                        {repo.tier}
                      </span>
                    </div>
                    <p className="text-sm text-muted-foreground mr-4 h-10 line-clamp-2">{repo.description}</p>
                    <div className="flex items-center gap-4 mt-3">
                      <div className="flex items-center gap-1.5 text-xs text-muted-foreground font-medium">
                        <Star className="w-3.5 h-3.5" /> {repo.stars}
                      </div>
                      <div className="flex items-center gap-1.5 text-xs text-muted-foreground font-medium">
                        <GitFork className="w-3.5 h-3.5" /> {repo.forks}
                      </div>
                      <div className="flex gap-2">
                        {repo.tags.map(tag => (
                          <span key={tag} className="text-[10px] text-muted-foreground bg-secondary/50 px-2 py-0.5 rounded-md">{tag}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-6">
                    <div className="text-right">
                      <div className="text-2xl font-black">{repo.score}</div>
                      <div className="text-[10px] font-bold text-muted-foreground uppercase">Repo Score</div>
                    </div>
                    <div className="w-12 h-12 rounded-2xl bg-secondary flex items-center justify-center group-hover:bg-primary transition-all">
                      <ArrowUpRight className="w-6 h-6 group-hover:text-white" />
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Recruiter Verdict Side Card */}
          <div className="space-y-6">
            <h3 className="text-xl font-bold">Recruiter Verdict</h3>
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="glass p-8 rounded-[2rem] border-l-4 border-l-emerald-500"
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-full bg-emerald-500/10 flex items-center justify-center">
                  <CheckCircle2 className="w-6 h-6 text-emerald-500" />
                </div>
                <div>
                  <div className="font-bold text-lg">Shortlist</div>
                  <div className="text-xs text-muted-foreground">Confidence: High</div>
                </div>
              </div>
              <p className="text-sm text-muted-foreground leading-relaxed mb-6 italic">
                &quot;Strong ML project shows production thinking. However, lack of unit testing across the portfolio 
                is a red flag for senior roles. Would reach out for an initial screening.&quot;
              </p>
              <div className="bg-secondary/30 rounded-2xl p-4 border border-border/50">
                <div className="text-xs font-bold text-primary flex items-center gap-2 mb-2">
                  <Lightbulb className="w-3 h-3" />
                  SINGLE BIGGEST FIX
                </div>
                <p className="text-sm font-medium">Add a /tests directory with at least 5 unit tests for your fraud detector.</p>
              </div>
            </motion.div>

            {/* Recommendation Card */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="bg-primary/10 border border-primary/20 p-8 rounded-[2rem]"
            >
              <h4 className="font-bold mb-2 flex items-center gap-2">
                <MessageSquareCode className="w-5 h-5 text-primary" />
                Next Recommended Build
              </h4>
              <p className="text-sm text-muted-foreground mb-4 font-medium">
                You&apos;re missing a <span className="text-white">Streaming Systems</span> project.
              </p>
              <div className="space-y-3">
                <div className="text-xs font-bold text-primary uppercase tracking-widest">Project Concept</div>
                <div className="text-sm font-bold">Real-time Log Analyzer via Kafka</div>
                <div className="flex gap-2">
                  <span className="text-[10px] bg-primary text-white px-2 py-0.5 rounded-full font-bold">+22 PTS</span>
                  <span className="text-[10px] bg-secondary text-foreground px-2 py-0.5 rounded-full font-bold">FAANG TIER</span>
                </div>
              </div>
            </motion.div>
          </div>
        </section>
      </main>
    </div>
  );
}
