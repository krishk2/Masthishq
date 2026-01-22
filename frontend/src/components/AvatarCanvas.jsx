import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const AvatarCanvas = ({ isSpeaking, isProcessing, message, processingStatus }) => {
    // Logic:
    // Idle/Loading (No Text) -> idle.gif (Phone)
    // Speaking (Text Loaded) -> speaking.gif (Mic)

    const avatarSrc = isSpeaking
        ? "/assets/speaking.gif"
        : "/assets/idle.gif";

    return (
        <div className="flex flex-col justify-center items-center h-full w-full bg-gray-900 overflow-hidden relative border-r border-white/5">
            {/* Background Gradient */}
            <div className="absolute inset-0 bg-gradient-to-b from-indigo-900/20 to-black/80 z-0 pointer-events-none" />

            {/* Avatar GIF */}
            <div className="relative z-10 flex flex-col items-center justify-center h-full w-full p-6">
                {/* Image Container */}
                <div className="relative w-full max-w-lg aspect-square flex items-center justify-center">
                    <img
                        src={avatarSrc}
                        alt="Avatar"
                        className="max-h-full object-contain filter drop-shadow-[0_0_30px_rgba(124,58,237,0.3)] transition-all duration-500"
                    />
                </div>

                {/* Dynamic Status / Caption */}
                <div className="mt-8 relative w-full flex flex-col items-center space-y-4 min-h-[100px]">

                    {/* Status Badge */}
                    {isSpeaking ? (
                        <div className="px-4 py-1.5 bg-green-500/20 border border-green-500/50 rounded-full backdrop-blur-sm shadow-[0_0_15px_rgba(34,197,94,0.3)] flex items-center gap-2">
                            <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                            <span className="text-green-400 text-xs font-bold tracking-widest uppercase">Speaking</span>
                        </div>
                    ) : isProcessing ? (
                        <div className="px-4 py-1.5 bg-purple-500/20 border border-purple-500/50 rounded-full backdrop-blur-sm shadow-[0_0_15px_rgba(168,85,247,0.3)] flex items-center gap-2">
                            <div className="flex gap-1">
                                <span className="w-1.5 h-1.5 bg-purple-400 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                                <span className="w-1.5 h-1.5 bg-purple-400 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                                <span className="w-1.5 h-1.5 bg-purple-400 rounded-full animate-bounce"></span>
                            </div>
                            <span className="text-purple-400 text-xs font-bold tracking-widest uppercase ml-1">Thinking</span>
                        </div>
                    ) : (
                        <div className="px-4 py-1.5 bg-blue-500/20 border border-blue-500/50 rounded-full backdrop-blur-sm shadow-[0_0_15px_rgba(59,130,246,0.3)] flex items-center gap-2">
                            <span className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></span>
                            <span className="text-blue-400 text-xs font-bold tracking-widest uppercase">Listening</span>
                        </div>
                    )}

                    {/* Dynamic Caption (Tooltip style) */}
                    <AnimatePresence mode='wait'>
                        {message && (
                            <motion.div
                                key={message}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -10 }}
                                className="bg-black/60 backdrop-blur-md text-white text-center px-6 py-3 rounded-2xl border border-white/10 shadow-xl max-w-md"
                            >
                                <p className="text-sm font-medium leading-relaxed italic text-indigo-100">
                                    "{message}"
                                </p>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </div>
        </div>
    );
};

export default AvatarCanvas;
