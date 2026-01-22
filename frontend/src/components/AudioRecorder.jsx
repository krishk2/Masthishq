
import React, { useState, useRef } from 'react';
import { Mic, Square, Play } from 'lucide-react';

export default function AudioRecorder({ onRecordingComplete }) {
    const [isRecording, setIsRecording] = useState(false);
    const [audioBlob, setAudioBlob] = useState(null);
    const [audioUrl, setAudioUrl] = useState(null);
    const mediaRecorderRef = useRef(null);
    const chunksRef = useRef([]);

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorderRef.current = new MediaRecorder(stream);
            chunksRef.current = [];

            mediaRecorderRef.current.ondataavailable = (e) => {
                if (e.data.size > 0) chunksRef.current.push(e.data);
            };

            mediaRecorderRef.current.onstop = () => {
                const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
                setAudioBlob(blob);
                const url = URL.createObjectURL(blob);
                setAudioUrl(url);
                onRecordingComplete(blob);

                // Stop tracks
                stream.getTracks().forEach(track => track.stop());
            };

            mediaRecorderRef.current.start();
            setIsRecording(true);
        } catch (err) {
            console.error("Mic access denied", err);
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
            setIsRecording(false);
        }
    };

    return (
        <div className="audio-recorder">
            {!isRecording && !audioBlob && (
                <button type="button" onClick={startRecording} className="rec-btn start">
                    <Mic size={20} /> Record Voice
                </button>
            )}

            {isRecording && (
                <button type="button" onClick={stopRecording} className="rec-btn stop">
                    <Square size={20} /> Stop
                </button>
            )}

            {audioBlob && (
                <div className="audio-preview">
                    <audio src={audioUrl} controls className="audio-player" />
                    <button type="button" onClick={() => {
                        setAudioBlob(null);
                        setAudioUrl(null);
                        onRecordingComplete(null);
                    }} className="rec-btn reset">
                        Reset
                    </button>
                </div>
            )}

            <style>{`
                .audio-recorder {
                    margin-bottom: 15px;
                }
                .rec-btn {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    padding: 8px 16px;
                    border-radius: 20px;
                    border: none;
                    font-weight: 600;
                    cursor: pointer;
                    width: 100%;
                    justify-content: center;
                }
                .start {
                    background: #3b82f6;
                    color: white;
                }
                .stop {
                    background: #ef4444;
                    color: white;
                    animation: pulse 1s infinite;
                }
                .reset {
                    background: #64748b;
                    color: white;
                    margin-top: 5px;
                }
                .audio-player {
                    width: 100%;
                    height: 32px;
                    margin-bottom: 5px;
                }
                @keyframes pulse {
                    0% { opacity: 1; }
                    50% { opacity: 0.7; }
                    100% { opacity: 1; }
                }
            `}</style>
        </div>
    );
}
