import React from 'react';
import { ArrowRight, Brain, Shield, Heart } from 'lucide-react';

const LandingPage = ({ onGetStarted }) => {
    return (
        <div className="landing-container">

            {/* Background Gradients */}
            <div className="bg-blob blob-1"></div>
            <div className="bg-blob blob-2"></div>



            {/* Hero Section */}
            <main className="hero-section">
                <div className="hero-content">
                    <div className="badge">🚀 Revolutionizing Alzheimer's Care</div>
                    <h1 className="hero-title">
                        Your External <br />
                        <span className="gradient-text">Second Brain</span>
                    </h1>
                    <p className="hero-desc">
                        Masthishq empowers patients with AI-driven memory recall, object recognition, and a friendly companion that never forgets.
                    </p>

                    <div className="hero-buttons">
                        <button onClick={onGetStarted} className="btn-primary">
                            Get Started Now <ArrowRight size={20} />
                        </button>
                    </div>
                </div>

                {/* Visual/Hero Image */}
                <div className="hero-visual">
                    <div className="chat-card">
                        <div className="chat-header">
                            <img src="/assets/speaking.gif" alt="Avatar" className="avatar-img" />
                            <div>
                                <div style={{ fontWeight: 'bold' }}>Masthishq Assistant</div>
                                <div style={{ fontSize: '0.8rem', color: '#4ade80' }}>● Online</div>
                            </div>
                        </div>
                        <div className="chat-bubble bot">Hello! I noticed Aunt May visited.</div>
                        <div className="chat-bubble user">Show me her photo.</div>
                        <div className="chat-bubble bot">Here is Aunt May.</div>
                    </div>
                </div>
            </main>

            {/* Features Grid */}
            <section id="features" className="features-section">
                <h2 className="section-title">Why Masthishq?</h2>
                <div className="features-grid">
                    <FeatureCard
                        icon={<Brain color="#a78bfa" size={40} />}
                        title="Memory Recall"
                        desc="Instantly identify faces and objects using advanced AI vision."
                    />
                    <FeatureCard
                        icon={<Shield color="#60a5fa" size={40} />}
                        title="Safe & Secure"
                        desc="All memories are stored locally on your device for maximum privacy."
                    />
                    <FeatureCard
                        icon={<Heart color="#f472b6" size={40} />}
                        title="Family Connected"
                        desc="Caregivers can update memories remotely to keep you supported."
                    />
                </div>
            </section>

            <footer className="footer">
                © 2026 Masthishq Project. All rights reserved.
            </footer>

            <style>{`
        .landing-container {
            min-height: 100vh;
            background: #0f172a;
            color: white;
            font-family: system-ui, sans-serif;
            position: relative;
            overflow-x: hidden;
        }
        .bg-blob {
            position: absolute;
            width: 50vw;
            height: 50vw;
            border-radius: 50%;
            filter: blur(120px);
            opacity: 0.3;
            z-index: 0;
            pointer-events: none;
        }
        .blob-1 { background: #7c3aed; top: -10%; left: -10%; }
        .blob-2 { background: #2563eb; bottom: -10%; right: -10%; }

        .navbar {
            position: relative;
            z-index: 10;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 40px;
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        .logo { display: flex; align-items: center; gap: 10px; }
        .brand-name {
            font-size: 1.5rem;
            font-weight: 800;
            background: linear-gradient(90deg, #a78bfa, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .nav-links { display: flex; gap: 30px; }
        .nav-links a { color: #cbd5e1; text-decoration: none; transition: 0.2s; }
        .nav-links a:hover { color: white; }
        .btn-login {
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            padding: 8px 20px;
            border-radius: 20px;
            color: white;
            cursor: pointer;
            transition: 0.2s;
        }
        .btn-login:hover { background: rgba(255,255,255,0.2); }

        .hero-section {
            position: relative;
            z-index: 10;
            display: flex;
            align-items: center;
            justify-content: space-between;
            max-width: 1200px;
            margin: 0 auto;
            padding: 80px 20px;
            gap: 50px;
        }
        .hero-content { flex: 1; }
        .badge {
            display: inline-block;
            padding: 6px 12px;
            background: rgba(124, 58, 237, 0.1);
            border: 1px solid rgba(124, 58, 237, 0.3);
            color: #c4b5fd;
            border-radius: 20px;
            font-size: 0.9rem;
            margin-bottom: 20px;
        }
        .hero-title {
            font-size: 4rem;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 20px;
        }
        .gradient-text {
            background: linear-gradient(90deg, #a78bfa, #f472b6, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-desc {
            font-size: 1.2rem;
            color: #94a3b8;
            margin-bottom: 40px;
            max-width: 500px;
            line-height: 1.6;
        }
        .btn-primary {
            background: linear-gradient(90deg, #7c3aed, #2563eb);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: transform 0.2s;
        }
        .btn-primary:hover { transform: scale(1.05); }

        .hero-visual { flex: 1; display: flex; justify-content: center; }
        .chat-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 20px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        }
        .chat-header { display: flex; items-center; gap: 15px; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px; }
        .avatar-img { width: 50px; height: 50px; border-radius: 50%; object-fit: cover; background: #334155; }
        .chat-bubble {
            padding: 10px 15px;
            border-radius: 12px;
            margin-bottom: 10px;
            font-size: 0.9rem;
            max-width: 80%;
        }
        .bot { background: rgba(30, 41, 59, 0.8); color: #cbd5e1; border-top-left-radius: 0; }
        .user { background: rgba(124, 58, 237, 0.2); color: white; margin-left: auto; border-top-right-radius: 0; border: 1px solid rgba(124, 58, 237, 0.3); }

        .features-section {
            background: rgba(15, 23, 42, 0.5);
            padding: 80px 20px;
            border-top: 1px solid rgba(255,255,255,0.05);
        }
        .section-title { text-align: center; font-size: 2.5rem; margin-bottom: 60px; }
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .feature-card {
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 20px;
            transition: 0.3s;
        }
        .feature-card:hover { transform: translateY(-5px); border-color: #a78bfa; }
        .feature-icon {
            background: #0f172a;
            padding: 15px;
            border-radius: 12px;
            display: inline-block;
            margin-bottom: 20px;
        }
        .feature-title { font-size: 1.25rem; font-weight: bold; margin-bottom: 10px; }
        .feature-desc { color: #94a3b8; line-height: 1.6; }
        
        .footer { background: #020617; padding: 40px; text-align: center; color: #64748b; font-size: 0.9rem; }
        
        @media (max-width: 768px) {
            .hero-section { flex-direction: column; text-align: center; }
            .hero-buttons { justify-content: center; }
            .nav-links { display: none; }
        }
      `}</style>
        </div>
    );
};

const FeatureCard = ({ icon, title, desc }) => (
    <div className="feature-card">
        <div className="feature-icon">{icon}</div>
        <h3 className="feature-title">{title}</h3>
        <p className="feature-desc">{desc}</p>
    </div>
);

export default LandingPage;
