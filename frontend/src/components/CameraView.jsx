
import React, { useRef, useEffect, useState } from 'react';
import { Camera, RefreshCw } from 'lucide-react';

export default function CameraView({ onCapture, isProcessing, trigger, isActive = false }) {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const [stream, setStream] = useState(null);
    const [error, setError] = useState(null);

    // Watch for external trigger
    useEffect(() => {
        if (trigger && trigger > 0 && isActive) {
            capture();
        }
    }, [trigger, isActive]);

    useEffect(() => {
        if (isActive) {
            startCamera();
        } else {
            stopCamera();
        }
        return () => stopCamera();
    }, [isActive]);

    const startCamera = async () => {
        try {
            const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
            setStream(mediaStream);
            if (videoRef.current) {
                videoRef.current.srcObject = mediaStream;
            }
        } catch (err) {
            setError("Could not access camera. Please allow permissions.");
            console.error(err);
        }
    };

    const stopCamera = () => {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            setStream(null);
        }
    };

    const capture = () => {
        if (!videoRef.current || !canvasRef.current) return;

        // Ensure video is playing and has data
        if (videoRef.current.videoWidth === 0 || videoRef.current.videoHeight === 0) {
            console.warn("Camera not ready for capture yet.");
            return;
        }

        const context = canvasRef.current.getContext('2d');
        canvasRef.current.width = videoRef.current.videoWidth;
        canvasRef.current.height = videoRef.current.videoHeight;
        context.drawImage(videoRef.current, 0, 0);

        canvasRef.current.toBlob((blob) => {
            if (blob) {
                onCapture(blob);
            } else {
                console.error("Failed to create blob from canvas");
            }
        }, 'image/jpeg', 0.9);
    };

    return (
        <div className="camera-container">
            {error ? (
                <div className="errorbox">{error}</div>
            ) : (
                <div className="video-wrapper">
                    <video ref={videoRef} autoPlay playsInline className="video-feed" />
                    <canvas ref={canvasRef} style={{ display: 'none' }} />
                </div>
            )}

            <div className="controls">
                <button
                    onClick={capture}
                    disabled={isProcessing || !!error}
                    className="capture-btn"
                >
                    {isProcessing ? <RefreshCw className="spin" /> : <Camera size={32} />}
                </button>
            </div>

            <style>{`
                .camera-container {
                    position: relative;
                    width: 100%;
                    max-width: 600px;
                    margin: 0 auto;
                    border-radius: 12px;
                    overflow: hidden;
                    background: #000;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                }
                .video-feed {
                    width: 100%;
                    display: block;
                }
                .controls {
                    position: absolute;
                    bottom: 20px;
                    left: 0;
                    right: 0;
                    display: flex;
                    justify-content: center;
                    padding: 10px;
                }
                .capture-btn {
                    background: white;
                    border: 4px solid rgba(255,255,255,0.3);
                    width: 70px;
                    height: 70px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    transition: transform 0.1s;
                    color: black;
                }
                .capture-btn:active {
                    transform: scale(0.95);
                }
                .capture-btn:disabled {
                    opacity: 0.7;
                    cursor: not-allowed;
                }
                .spin {
                    animation: spin 1s linear infinite;
                }
                @keyframes spin { 
                    100% { transform: rotate(360deg); } 
                }
                .errorbox {
                    padding: 40px;
                    color: white;
                    text-align: center;
                }
            `}</style>
        </div>
    );
}
