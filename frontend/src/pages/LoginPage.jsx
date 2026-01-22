import React from 'react';
import { User, HeartHandshake } from 'lucide-react';

const LoginPage = ({ onSelectRole }) => {
    return (
        <div className="login-container">

            <div className="bg-glow"></div>

            <div className="cards-wrapper">

                {/* Patient Card */}
                <div className="role-card patient-card" onClick={() => onSelectRole('patient')}>
                    <div className="icon-wrapper patient-icon">
                        <User size={48} color="white" />
                    </div>
                    <h2 className="role-title">I am a User</h2>
                    <p className="role-desc">Access your assistant, memory aid, and companion.</p>
                    <div className="role-btn-wrapper">
                        <span className="role-btn patient-btn">Enter Masthishq &rarr;</span>
                    </div>
                </div>

                {/* Caregiver Card */}
                <div className="role-card caregiver-card" onClick={() => onSelectRole('caregiver')}>
                    <div className="icon-wrapper caregiver-icon">
                        <HeartHandshake size={48} color="white" />
                    </div>
                    <h2 className="role-title">I am a Caregiver</h2>
                    <p className="role-desc">Enroll memories, manage settings, and helping loved ones.</p>
                    <div className="role-btn-wrapper">
                        <span className="role-btn caregiver-btn">Manage Care &rarr;</span>
                    </div>
                </div>

            </div>

            <style>{`
        .login-container {
            min-height: 100vh;
            background: #0f172a;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
            font-family: system-ui, sans-serif;
        }
        .bg-glow {
            position: absolute;
            width: 800px;
            height: 800px;
            background: rgba(124, 58, 237, 0.1);
            border-radius: 50%;
            filter: blur(100px);
            z-index: 0;
            pointer-events: none;
        }
        .cards-wrapper {
            position: relative;
            z-index: 10;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            width: 100%;
            max-width: 900px;
            padding: 20px;
        }
        .role-card {
            background: rgba(30, 41, 59, 0.5);
            border: 1px solid #334155;
            padding: 40px;
            border-radius: 24px;
            cursor: pointer;
            text-align: center;
            transition: 0.3s;
            backdrop-filter: blur(10px);
        }
        .role-card:hover { transform: translateY(-10px); }
        .patient-card:hover { border-color: #8b5cf6; background: rgba(30, 41, 59, 0.8); }
        .caregiver-card:hover { border-color: #10b981; background: rgba(30, 41, 59, 0.8); }

        .icon-wrapper {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            margin: 0 auto 25px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .patient-icon { background: linear-gradient(135deg, #8b5cf6, #3b82f6); }
        .caregiver-icon { background: linear-gradient(135deg, #10b981, #059669); }

        .role-title { color: white; margin: 0 0 10px; font-size: 2rem; }
        .role-desc { color: #94a3b8; font-size: 1.1rem; line-height: 1.5; }

        .role-btn-wrapper { margin-top: 30px; }
        .role-btn {
            padding: 10px 25px;
            border-radius: 30px;
            border: 1px solid rgba(255,255,255,0.2);
            color: white;
            transition: 0.2s;
            display: inline-block;
        }
        .patient-card:hover .patient-btn { background: #8b5cf6; border-color: #8b5cf6; }
        .caregiver-card:hover .caregiver-btn { background: #10b981; border-color: #10b981; }

        @media (max-width: 768px) {
            .cards-wrapper { grid-template-columns: 1fr; }
        }
      `}</style>
        </div>
    );
};

export default LoginPage;
