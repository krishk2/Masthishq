import React, { useState, useEffect, useRef } from 'react';
import { Send, Volume2, User, Package, UserPlus, PackagePlus, Sparkles, Camera, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import CameraView from './CameraView'; // Import CameraView

function ChatInterface({
    messages,
    onSendMessage,
    suggestions = [],
    onSuggestionClick,
    onPlayAudio,
    onCapture,
    onScanFace,
    onScanObject,
    onEnroll,
    onEnrollObject,
    isTyping,
    typingStatus
}) {
    const [input, setInput] = useState("");
    const [showCamera, setShowCamera] = useState(false);
    const [cameraMode, setCameraMode] = useState('person');
    const endRef = useRef(null);
    const containerRef = useRef(null);

    useEffect(() => {
        endRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, isTyping, showCamera]);

    const handleSend = () => {
        if (!input.trim()) return;
        onSendMessage(input);
        setInput("");
    };

    const handleCameraCapture = (blob) => {
        onCapture(blob);
        setShowCamera(false);
    };

    const openCamera = (mode) => {
        if (mode === 'person') onScanFace();
        else onScanObject();
        setCameraMode(mode);
        setShowCamera(true);
    };

    return (
        <div className="flex flex-col h-full bg-slate-900/50 backdrop-blur-xl border-l border-white/5 relative">
            {/* Header */}
            <div className="p-4 border-b border-white/5 flex items-center gap-2 bg-slate-900/80 sticky top-0 z-10">
                <Sparkles className="text-purple-400" size={20} />
                <h2 className="font-semibold text-slate-200 text-sm tracking-wide uppercase">Convolve Memory</h2>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-6 scrollbar-hide" ref={containerRef}>
                {messages.length === 0 && !showCamera && (
                    <div className="h-full flex flex-col items-center justify-center text-slate-500 space-y-4 opacity-60">
                        <div className="p-4 bg-slate-800 rounded-full mb-2 animate-pulse">
                            <Sparkles size={40} className="text-purple-500" />
                        </div>
                        <h2 className="text-lg font-medium">How can I help you?</h2>
                    </div>
                )}

                <AnimatePresence mode="popLayout">
                    {messages.map((msg, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 20, scale: 0.95 }}
                            animate={{ opacity: 1, y: 0, scale: 1 }}
                            transition={{ duration: 0.3 }}
                            className={`flex w-full ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div className={`flex max-w-[85%] md:max-w-[75%] gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                                {/* Avatar */}
                                <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 shadow-lg ${msg.role === 'user'
                                    ? 'bg-gradient-to-br from-indigo-500 to-purple-600'
                                    : 'bg-gradient-to-br from-emerald-500 to-teal-600'
                                    }`}>
                                    {msg.role === 'user' ? <User size={14} className="text-white" /> : <Sparkles size={14} className="text-white" />}
                                </div>

                                {/* Content Bubble */}
                                <div className={`flex flex-col space-y-2 p-4 shadow-xl backdrop-blur-sm border border-white/5 ${msg.role === 'user'
                                    ? 'bg-indigo-600/90 text-white rounded-2xl rounded-tr-none'
                                    : 'bg-slate-800/90 text-slate-200 rounded-2xl rounded-tl-none'
                                    }`}>
                                    <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.text}</p>
                                    {msg.image && (
                                        <motion.img
                                            initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                                            src={msg.image.startsWith('data:') ? msg.image : `data:image/jpeg;base64,${msg.image}`}
                                            alt="Visual Memory"
                                            className="rounded-lg max-h-64 w-full object-contain border border-white/10 bg-black/40"
                                        />
                                    )}
                                    {msg.gallery && msg.gallery.length > 0 && (
                                        <div className="flex gap-2 overflow-x-auto py-2 scroll-smooth no-scrollbar">
                                            {msg.gallery.map((img, idx) => (
                                                <img
                                                    key={idx}
                                                    src={img.startsWith('data:') ? img : `data:image/jpeg;base64,${img}`}
                                                    className="w-16 h-16 rounded-md object-cover border border-white/10 hover:scale-110 transition-transform cursor-pointer"
                                                />
                                            ))}
                                        </div>
                                    )}
                                    {msg.audioUrl && (
                                        <button
                                            onClick={() => onPlayAudio(msg.audioUrl)}
                                            className="flex items-center gap-2 bg-black/20 hover:bg-black/40 text-xs px-3 py-2 rounded-lg w-fit transition-colors"
                                        >
                                            <Volume2 size={14} />
                                            <span>Play Audio</span>
                                        </button>
                                    )}
                                </div>
                            </div>
                        </motion.div>
                    ))}

                    {/* Inline Camera View */}
                    {showCamera && (
                        <motion.div
                            key="camera-view"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: 20 }}
                            className="flex justify-end w-full"
                        >
                            <div className="bg-slate-900 border border-purple-500/50 p-2 rounded-2xl shadow-2xl relative max-w-sm">
                                <div className="flex justify-between items-center mb-2 px-1">
                                    <span className="text-xs text-purple-300 font-bold uppercase tracking-wider">{cameraMode} SCAN</span>
                                    <button onClick={() => setShowCamera(false)} className="text-slate-400 hover:text-white">
                                        <X size={16} />
                                    </button>
                                </div>
                                <div className="rounded-xl overflow-hidden aspect-video bg-black relative">
                                    <CameraView
                                        isActive={true}
                                        onCapture={handleCameraCapture}
                                        trigger={0}
                                        isProcessing={false}
                                    />
                                </div>
                            </div>
                        </motion.div>
                    )}

                    {/* Typing Indicator (TEXT ONLY NO DOTS) */}
                    {isTyping && (
                        <motion.div
                            key="typing-indicator"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="flex justify-start w-full"
                        >
                            <div className="flex flex-row gap-3 items-center">
                                <div className="w-8 h-8 rounded-full bg-emerald-600 flex items-center justify-center animate-pulse">
                                    <Sparkles size={14} className="text-white" />
                                </div>
                                <div className="bg-slate-800/80 p-3 rounded-2xl rounded-tl-none flex items-center border border-emerald-500/20">
                                    <span className="text-xs font-semibold text-emerald-400 tracking-wide uppercase animate-pulse">
                                        {typingStatus || "Thinking..."}
                                    </span>
                                </div>
                            </div>
                        </motion.div>
                    )}
                    <div ref={endRef} />
                </AnimatePresence>
            </div>

            {/* Input Footer */}
            <div className="p-4 bg-slate-900 border-t border-white/5 space-y-3 z-20">
                {/* Suggestions */}
                {suggestions.length > 0 && !showCamera && (
                    <div className="flex gap-2 overflow-x-auto pb-2 noscroll">
                        {suggestions.map((s, i) => (
                            <button
                                key={i}
                                onClick={() => onSuggestionClick(s)}
                                className="whitespace-nowrap px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs rounded-full border border-slate-700 transition-colors"
                            >
                                {s}
                            </button>
                        ))}
                    </div>
                )}
                {/* Input Bar */}
                <div className="relative group">
                    {/* Tools (Moved Up) */}
                    <div className="absolute -top-16 left-0 flex gap-1 opacity-0 group-hover:opacity-100 group-focus-within:opacity-100 transition-opacity duration-300 bg-slate-900/90 p-2 rounded-lg border border-slate-700 shadow-xl backdrop-blur-md">
                        <ActionButton icon={<User size={16} />} label="Scan Face" onClick={() => openCamera('person')} />
                        <ActionButton icon={<Package size={16} />} label="Scan Object" onClick={() => openCamera('object')} />
                        <div className="w-px h-6 bg-slate-700 mx-1"></div>
                        <ActionButton icon={<UserPlus size={16} />} label="Enroll Person" onClick={onEnroll} color="text-purple-400" />
                        <ActionButton icon={<PackagePlus size={16} />} label="Enroll Item" onClick={onEnrollObject} color="text-orange-400" />
                    </div>

                    <div className="flex items-center gap-2 bg-slate-800 rounded-2xl p-2 border border-slate-700 focus-within:border-purple-500/50 focus-within:ring-2 focus-within:ring-purple-500/20 transition-all shadow-lg">
                        <input
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                            placeholder="Ask Convolve..."
                            disabled={showCamera}
                            className="flex-1 bg-transparent text-white px-3 py-2 text-sm outline-none placeholder:text-slate-500 disabled:opacity-50"
                        />
                        <button
                            onClick={handleSend}
                            disabled={!input.trim()}
                            className="p-2 bg-purple-600 hover:bg-purple-500 text-white rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        >
                            <Send size={18} />
                        </button>
                    </div>
                </div>
                <div className="text-center">
                    <p className="text-[10px] text-slate-600 font-medium">Convolve AI Memory Assistant</p>
                </div>
            </div>
        </div>
    );
}

const ActionButton = ({ icon, onClick, color = "text-slate-300", label }) => (
    <button
        onClick={onClick}
        title={label}
        className={`p-2 hover:bg-white/10 rounded-md transition-colors ${color}`}
    >
        {icon}
    </button>
);

export default ChatInterface;
