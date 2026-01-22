import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { ArrowRight, Check, Camera, Mic, UploadCloud } from 'lucide-react';
import AudioRecorder from '../components/AudioRecorder';

/*
  Caregiver Dashboard - Typeform Style
*/

const API_BASE = import.meta.env.VITE_API_URL || "/api/v1";

const CaregiverDashboard = () => {
    const [step, setStep] = useState(0);
    const [formData, setFormData] = useState({ name: '', relation: '', notes: '', age: '' });
    const [file, setFile] = useState(null);
    const [filePreview, setFilePreview] = useState(null);
    const [audioBlob, setAudioBlob] = useState(null);
    const [status, setStatus] = useState(null); // 'submitting', 'success', 'error'

    const inputRef = useRef(null);

    useEffect(() => {
        if (inputRef.current) inputRef.current.focus();
    }, [step]);

    const handleNext = () => {
        if (step === 0 && !formData.name) return alert("Please enter a name.");
        if (step === 2 && !file) return alert("Please upload a photo.");
        setStep(prev => prev + 1);
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && step !== 3) handleNext(); // Step 3 is Notes (TextArea)
    };

    const handleSubmit = async () => {
        setStatus('submitting');
        const data = new FormData();
        data.append('name', formData.name);
        data.append('relation', formData.relation || 'Acquaintance');
        data.append('notes', formData.notes);
        data.append('file', file);
        if (audioBlob) data.append('audio_file', audioBlob, 'voice.webm');

        try {
            const res = await axios.post(`${API_BASE}/remember/person`, data, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            if (res.data.status === 'stored') {
                setStatus('success');
                setTimeout(() => {
                    setStep(0);
                    setFormData({ name: '', relation: '', notes: '', age: '' });
                    setFile(null);
                    setFilePreview(null);
                    setAudioBlob(null);
                    setStatus(null);
                }, 3000);
            }
        } catch (e) {
            console.error(e);
            setStatus('error');
        }
    };

    const renderStep = () => {
        switch (step) {
            case 0:
                return (
                    <div className="step-content">
                        <h2 className="step-number">1 <span className="arrow">→</span></h2>
                        <h1 className="question">What is the person's name?</h1>
                        <p className="sub-text">We'll use this to identify them.</p>
                        <input
                            ref={inputRef}
                            className="big-input"
                            placeholder="Type name..."
                            value={formData.name}
                            onChange={e => setFormData({ ...formData, name: e.target.value })}
                            onKeyDown={handleKeyDown}
                        />
                        <button className="btn-next" onClick={handleNext}>OK <Check size={18} /></button>
                    </div>
                );
            case 1:
                return (
                    <div className="step-content">
                        <h2 className="step-number">2 <span className="arrow">→</span></h2>
                        <h1 className="question">How are they related?</h1>
                        <p className="sub-text">Sister, Doctor, Old Friend...</p>
                        <input
                            ref={inputRef}
                            className="big-input"
                            placeholder="Type relationship..."
                            value={formData.relation}
                            onChange={e => setFormData({ ...formData, relation: e.target.value })}
                            onKeyDown={handleKeyDown}
                        />
                        <button className="btn-next" onClick={handleNext}>OK <Check size={18} /></button>
                    </div>
                );
            case 2:
                return (
                    <div className="step-content">
                        <h2 className="step-number">3 <span className="arrow">→</span></h2>
                        <h1 className="question">Upload a photo.</h1>
                        <p className="sub-text">A clear face photo works best.</p>

                        <div className="upload-box" onClick={() => document.getElementById('file-upload').click()}>
                            {filePreview ? (
                                <img src={filePreview} className="preview-img" alt="Preview" />
                            ) : (
                                <div className="upload-placeholder">
                                    <Camera size={48} className="icon-pulse" />
                                    <span>Click to Upload</span>
                                </div>
                            )}
                            <input id="file-upload" type="file" accept="image/*" onChange={e => {
                                const f = e.target.files[0];
                                if (f) { setFile(f); setFilePreview(URL.createObjectURL(f)); }
                            }} hidden />
                        </div>

                        {file && <button className="btn-next" onClick={handleNext}>OK <Check size={18} /></button>}
                    </div>
                );
            case 3:
                return (
                    <div className="step-content">
                        <h2 className="step-number">4 <span className="arrow">→</span></h2>
                        <h1 className="question">Any context or notes?</h1>
                        <p className="sub-text">"She likes coffee", "He is your neighbor"...</p>
                        <textarea
                            ref={inputRef}
                            className="big-input textarea"
                            placeholder="Type here..."
                            value={formData.notes}
                            onChange={e => setFormData({ ...formData, notes: e.target.value })}
                        />

                        <div className="voice-opt">
                            <span style={{ opacity: 0.7, marginRight: 10 }}>Voice Sample (Optional):</span>
                            <AudioRecorder onRecordingComplete={setAudioBlob} />
                        </div>

                        <button className="btn-submit" onClick={handleSubmit}>
                            {status === 'submitting' ? 'Saving...' : 'Submit'}
                        </button>
                    </div>
                );
            default: return null;
        }
    };

    if (status === 'success') {
        return (
            <div className="success-screen">
                <h1>All done! 🎉</h1>
                <p>Memory has been securely stored.</p>
            </div>
        );
    }

    return (
        <div className="tf-container">
            {/* Progress Bar */}
            <div className="progress-bar" style={{ width: `${(step + 1) * 25}%` }}></div>

            <div className="tf-wrapper">
                {renderStep()}
            </div>

            <style>{`
        .tf-container {
            min-height: 100vh;
            background: #0f172a;
            color: white;
            font-family: 'Inter', system-ui, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        .progress-bar {
            position: absolute;
            top: 0;
            left: 0;
            height: 4px;
            background: #8b5cf6;
            transition: width 0.5s ease;
        }
        .tf-wrapper {
            width: 100%;
            max-width: 700px;
            padding: 20px;
            animation: fadeIn 0.5s ease-out;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

        .step-number { font-size: 1.2rem; color: #8b5cf6; margin-bottom: 10px; display: flex; align-items: center; gap: 10px; }
        .arrow { font-size: 1.5rem; }
        
        .question { font-size: 2.5rem; margin-bottom: 15px; font-weight: 300; line-height: 1.2; }
        .sub-text { font-size: 1.2rem; color: #94a3b8; margin-bottom: 40px; }

        .big-input {
            width: 100%;
            background: transparent;
            border: none;
            border-bottom: 2px solid rgba(255,255,255,0.2);
            color: #a78bfa;
            font-size: 2rem;
            padding: 10px 0;
            outline: none;
            transition: 0.3s;
            display: block;
            margin-bottom: 30px;
        }
        .big-input:focus { border-color: #8b5cf6; }
        .big-input::placeholder { color: rgba(255,255,255,0.1); }
        .textarea { height: 100px; resize: none; font-size: 1.5rem; }

        .btn-next {
            background: #8b5cf6;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 4px;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            transition: 0.2s;
        }
        .btn-next:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(139, 92, 246, 0.4); }

        .upload-box {
            border: 2px dashed #475569;
            border-radius: 12px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: 0.2s;
            margin-bottom: 30px;
        }
        .upload-box:hover { border-color: #8b5cf6; background: rgba(139, 92, 246, 0.05); }
        .upload-placeholder { color: #94a3b8; display: flex; flex-direction: column; align-items: center; gap: 10px; }
        .preview-img { max-height: 300px; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        
        .btn-submit {
            background: #10b981;
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 30px;
            font-size: 1.5rem;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
            display: block;
            margin-top: 20px;
        }
        .btn-submit:hover { transform: scale(1.05); box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4); }

        .success-screen {
            height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; 
            background: #0f172a; color: white; text-align: center;
        }
        .success-screen h1 { font-size: 4rem; margin-bottom: 20px; color: #10b981; }
        
        .voice-opt { margin-bottom: 30px; display: flex; align-items: center; }
      `}</style>
        </div>
    );
};

export default CaregiverDashboard;
