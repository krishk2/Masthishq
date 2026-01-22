import React, { useState, useEffect } from 'react';
import AudioRecorder from './AudioRecorder';
import { UserPlus, PackagePlus, Save, X, Mic, Image as ImageIcon } from 'lucide-react';

function EnrollmentForm({ type = 'person', onCancel, onSave }) {
    const [name, setName] = useState("");
    const [relation, setRelation] = useState("Acquaintance");
    const [age, setAge] = useState("");
    const [notes, setNotes] = useState("");
    const [audioBlob, setAudioBlob] = useState(null);
    const [avatarUrl, setAvatarUrl] = useState(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const isPerson = type === 'person';

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);
        // Pass parent wrapper call
        const result = await onSave({ name, relation, age, notes, audioBlob });
        if (result && result.avatar_url) {
            setAvatarUrl(result.avatar_url);
        }
        setIsSubmitting(false);
    };

    return (
        <div className="enrollment-container">
            <div className="enrollment-header">
                <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-lg ${isPerson ? 'bg-purple-500/20 text-purple-400' : 'bg-orange-500/20 text-orange-400'}`}>
                        {isPerson ? <UserPlus size={24} /> : <PackagePlus size={24} />}
                    </div>
                    <div>
                        <h3 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
                            {avatarUrl ? "Enrollment Complete" : (isPerson ? "New Person" : "New Object")}
                        </h3>
                        <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold">
                            {isPerson ? "Social Memory" : "Personal Belonging"}
                        </p>
                    </div>
                </div>
                <button onClick={onCancel} className="close-btn"><X size={20} /></button>
            </div>

            {!avatarUrl ? (
                <form onSubmit={handleSubmit} className="enroll-form space-y-5">
                    {/* Name Field */}
                    <div className="form-group">
                        <label className="text-sm font-medium text-slate-400 mb-1 block">
                            {isPerson ? "Who is this?" : "What is this object?"}
                        </label>
                        <input
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                            className="w-full bg-slate-800/50 border border-slate-700 rounded-xl p-3 text-white focus:ring-2 focus:ring-purple-500/50 outline-none transition-all placeholder:text-slate-600"
                            placeholder={isPerson ? "e.g. Aunt May" : "e.g. Medicine Box"}
                        />
                    </div>

                    {/* Person Specific Fields */}
                    {isPerson && (
                        <div className="grid grid-cols-2 gap-4">
                            <div className="form-group">
                                <label className="text-sm font-medium text-slate-400 mb-1 block">Relation</label>
                                <select
                                    value={relation}
                                    onChange={(e) => setRelation(e.target.value)}
                                    className="w-full bg-slate-800/50 border border-slate-700 rounded-xl p-3 text-white focus:ring-2 focus:ring-purple-500/50 outline-none appearance-none"
                                >
                                    <option>Family</option>
                                    <option>Friend</option>
                                    <option>Caregiver</option>
                                    <option>Doctor</option>
                                    <option>Acquaintance</option>
                                    <option>Other</option>
                                </select>
                            </div>
                            <div className="form-group">
                                <label className="text-sm font-medium text-slate-400 mb-1 block">Age (Opt)</label>
                                <input
                                    type="number"
                                    value={age}
                                    onChange={(e) => setAge(e.target.value)}
                                    className="w-full bg-slate-800/50 border border-slate-700 rounded-xl p-3 text-white focus:ring-2 focus:ring-purple-500/50 outline-none"
                                    placeholder="e.g. 64"
                                />
                            </div>
                        </div>
                    )}

                    {/* Notes Field */}
                    <div className="form-group">
                        <label className="text-sm font-medium text-slate-400 mb-1 block">Memory Notes</label>
                        <textarea
                            value={notes}
                            onChange={(e) => setNotes(e.target.value)}
                            className="w-full bg-slate-800/50 border border-slate-700 rounded-xl p-3 text-white focus:ring-2 focus:ring-purple-500/50 outline-none resize-none h-24 placeholder:text-slate-600"
                            placeholder={isPerson ? "Lives in New Jersey, likes knitting..." : "Usually kept on the dining table..."}
                        />
                    </div>

                    {/* Voice Sample (Person Only) */}
                    {isPerson && (
                        <div className="bg-slate-800/30 border border-slate-700/50 p-4 rounded-xl">
                            <label className="text-sm font-medium text-purple-300 mb-3 flex items-center gap-2">
                                <Mic size={16} /> Voice Verification Sample
                            </label>
                            <AudioRecorder onRecordingComplete={setAudioBlob} />
                        </div>
                    )}

                    {/* Footer Actions */}
                    <div className="pt-4 border-t border-white/5">
                        <button
                            type="submit"
                            disabled={isSubmitting}
                            className={`w-full py-4 rounded-xl font-bold text-white shadow-lg flex items-center justify-center gap-2 transition-transform active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed
                                ${isPerson
                                    ? 'bg-gradient-to-r from-purple-600 to-indigo-600 hover:shadow-purple-500/25'
                                    : 'bg-gradient-to-r from-orange-500 to-red-500 hover:shadow-orange-500/25'
                                }`}
                        >
                            {isSubmitting ? (
                                <span className="animate-pulse">Creating Memory...</span>
                            ) : (
                                <>
                                    <Save size={20} />
                                    {isPerson ? "Save Person & Create Avatar" : "Save Object"}
                                </>
                            )}
                        </button>
                    </div>
                </form>
            ) : (
                <div className="avatar-result flex flex-col items-center justify-center h-[400px] animate-in fade-in zoom-in duration-300">
                    <div className="relative">
                        <div className="absolute inset-0 bg-green-500/20 blur-xl rounded-full"></div>
                        <img
                            src={avatarUrl}
                            alt="Generated Avatar"
                            className="w-48 h-48 rounded-full object-cover border-4 border-green-500 shadow-2xl relative z-10"
                        />
                        <div className="absolute -bottom-2 -right-2 bg-green-500 text-white p-2 rounded-full z-20 shadow-lg">
                            <ImageIcon size={20} />
                        </div>
                    </div>
                    <h4 className="text-2xl font-bold text-white mt-6 mb-2">Success!</h4>
                    <p className="text-slate-400 text-center mb-8 max-w-xs">
                        {isPerson
                            ? `${name} has been added to your social circle.`
                            : `${name} is now tracked in your inventory.`
                        }
                    </p>
                    <button onClick={onCancel} className="bg-slate-700 hover:bg-slate-600 text-white px-8 py-3 rounded-xl font-semibold transition-colors w-full">
                        Return to Chat
                    </button>
                </div>
            )}

            <style>{`
                .enrollment-container {
                    background: #0f172a; /* Slate 900 */
                    height: 100%;
                    padding: 24px;
                    display: flex;
                    flex-direction: column;
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
                
                /* Custom Scrollbar for form if needed */
                .enrollment-container::-webkit-scrollbar { width: 4px; }
                .enrollment-container::-webkit-scrollbar-thumb { background: #334155; border-radius: 2px; }
            `}</style>
        </div>
    );
}

export default EnrollmentForm;
