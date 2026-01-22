import React from 'react';
import { Home, Users, Settings, Menu, Brain } from 'lucide-react';

const NavBar = ({ onViewChange, currentView }) => {
    return (
        <>
            <div className="topnav">
                <div className="nav-brand">
                    <Brain size={28} color="#a78bfa" />
                    <span className="brand-text">Masthishq</span>
                </div>

                <div className="nav-links">
                    <div className={`nav-item ${currentView === 'landing' ? 'active' : ''}`} onClick={() => onViewChange('landing')}>
                        <Home size={20} />
                        <span>Home</span>
                    </div>

                    <div className={`nav-item ${currentView === 'patient' ? 'active' : ''}`} onClick={() => onViewChange('patient')}>
                        <Users size={20} />
                        <span>Patient</span>
                    </div>

                    <div className={`nav-item ${currentView === 'caregiver' ? 'active' : ''}`} onClick={() => onViewChange('caregiver')}>
                        <Settings size={20} />
                        <span>Caregiver</span>
                    </div>
                </div>
            </div>

            <style>{`
        .topnav {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 70px;
            background: rgba(15, 23, 42, 0.9);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255,255,255,0.1);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 40px;
            z-index: 1000;
        }
        .nav-brand {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .brand-text {
            font-size: 1.5rem;
            font-weight: 800;
            background: linear-gradient(90deg, #a78bfa, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .nav-links {
            display: flex;
            gap: 10px;
        }
        .nav-item {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            color: #94a3b8;
            font-weight: 500;
            transition: 0.2s;
        }
        .nav-item:hover {
            background: rgba(255,255,255,0.05);
            color: white;
        }
        .nav-item.active {
            background: linear-gradient(90deg, #7c3aed, #4f46e5);
            color: white;
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
        }
      `}</style>
        </>
    );
};

export default NavBar;
