
import React, { useState } from 'react';
import AudioRecorder from './AudioRecorder';
import { UserPlus, Save, X } from 'lucide-react';

function EnrollmentForm({ onCancel, onSave }) {
    const [name, setName] = useState("");
    const [relation, setRelation] = useState("Acquaintance");
    const [age, setAge] = useState("");
    const [notes, setNotes] = useState("");
    const [audioBlob, setAudioBlob] = useState(null);
    const [avatarUrl, setAvatarUrl] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        // Pass parent wrapper call
        const result = await onSave({ name, relation, age, notes, audioBlob });
        if (result && result.avatar_url) {
            setAvatarUrl(result.avatar_url);
        }
    };

    return (
        <div className="enrollment-container">
            <div className="enrollment-header">
                <h3>New Person Entry {avatarUrl && "✅"}</h3>
                <button onClick={onCancel} className="close-btn"><X size={20} /></button>
            </div>

            {!avatarUrl ? (
                <form onSubmit={handleSubmit} className="enroll-form">
                    <div className="form-group">
                        <label>Name</label>
                        <input value={name} onChange={(e) => setName(e.target.value)} required placeholder="e.g. Aunt May" />
                    </div>

                    <div className="form-group">
                        <label>Age</label>
                        <input type="number" value={age} onChange={(e) => setAge(e.target.value)} placeholder="Age (Optional)" />
                    </div>

                    <div className="form-group">
                        <label>Relation</label>
                        <select value={relation} onChange={(e) => setRelation(e.target.value)}>
                            <option>Family</option>
                            <option>Friend</option>
                            <option>Caregiver</option>
                            <option>Doctor</option>
                            <option>Acquaintance</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label>Memory Notes</label>
                        <textarea value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Lives in New York..." />
                    </div>

                    <div className="form-group">
                        <label>Voice Sample</label>
                        <AudioRecorder onRecordingComplete={setAudioBlob} />
                    </div>

                    <button type="submit" className="save-btn">
                        <Save size={18} /> Save & Generate Avatar
                    </button>
                </form>
            ) : (
                <div className="avatar-result">
                    <h4>Avatar Created!</h4>
                    <img src={avatarUrl} alt="Generated Avatar" className="avatar-large" />
                    <button onClick={onCancel} className="save-btn">Done</button>
                </div>
            )}

            <style>{`
                .enrollment-container {
                    background: linear-gradient(145deg, #1e293b, #0f172a);
                    border-radius: 20px;
                    padding: 30px;
                    border: 1px solid rgba(139, 92, 246, 0.2);
                    color: white;
                    height: 100%;
                    overflow-y: auto;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                }
                .enrollment-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 25px;
                    border-bottom: 1px solid rgba(255,255,255,0.08);
                    padding-bottom: 15px;
                }
                .enrollment-header h3 {
                    margin: 0;
                    font-size: 1.5rem;
                    background: linear-gradient(90deg, #fff, #a78bfa);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }
                .close-btn { 
                    background: rgba(255,255,255,0.05); 
                    border: none; 
                    color: #94a3b8; 
                    cursor: pointer; 
                    padding: 8px;
                    border-radius: 50%;
                    transition: 0.2s;
                }
                .close-btn:hover { background: rgba(255,255,255,0.1); color: white; transform: rotate(90deg); }
                
                .form-group { margin-bottom: 20px; }
                .form-group label { 
                    display: block; 
                    margin-bottom: 8px; 
                    font-size: 0.9rem; 
                    color: #94a3b8; 
                    font-weight: 500;
                    letter-spacing: 0.5px;
                }
                .form-group input, .form-group select, .form-group textarea {
                    width: 100%;
                    background: rgba(0,0,0,0.2);
                    border: 1px solid rgba(255,255,255,0.08);
                    padding: 12px 15px;
                    border-radius: 10px;
                    color: white;
                    font-size: 1rem;
                    transition: 0.2s;
                    font-family: inherit;
                }
                .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
                    border-color: #8b5cf6;
                    background: rgba(139, 92, 246, 0.05);
                    outline: none;
                    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
                }
                .save-btn {
                    width: 100%;
                    background: linear-gradient(90deg, #10b981, #059669);
                    border: none;
                    padding: 14px;
                    border-radius: 12px;
                    color: white;
                    font-weight: 600;
                    letter-spacing: 0.5px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                    cursor: pointer;
                    margin-top: 20px;
                    transition: all 0.2s;
                    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
                }
                .save-btn:hover { 
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3);
                }
                .avatar-result {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    animation: fadeIn 0.5s ease-out;
                }
                .avatar-large {
                    width: 250px;
                    height: 250px;
                    border-radius: 50%;
                    object-fit: cover;
                    border: 4px solid #10b981;
                    margin: 30px 0;
                    box-shadow: 0 0 30px rgba(16, 185, 129, 0.2);
                }
                @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            `}</style>
        </div>
    );
}

export default EnrollmentForm;
